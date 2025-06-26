from .input_data import InputData
from .. import do
from ..utils import file, field
from ..context import Context
import pandas as pd
import logging

input_data = InputData()


class DataLoader:
    def __init__(
            self,
            param_file_dict: dict = None
    ):
        self.param_file_dict = param_file_dict


    def generate_global_parameter(self, context: Context):
        gph = field.GlobalParamHeader
        gpf = field.GlobalParameterField

        if context.config.load_from_file:
            global_param_df = pd.read_csv("{}{}".format(context.config.input_folder, file.GLOBAL_PARAM_FILE),
                                      dtype={gph.name: str, gph.value: float})
        else:
            global_param_df = self.param_file_dict[file.GLOBAL_PARAM_FILE]

        global_param_dict = dict(zip(global_param_df[gph.name], global_param_df[gph.value]))
        global_parameter = do.GlobalParameter(
            transport_cost_rate=global_param_dict[gpf.transport_rate_cost],
            stock_cost_rate=global_param_dict[gpf.stock_cost_rate],
            lack_cost=global_param_dict[gpf.lack_cost],
            fund_rate=global_param_dict[gpf.fund_rate] / 100,
            produce_cost=global_param_dict[gpf.produce_cost],
            min_warehouse_num=global_param_dict[gpf.min_warehouse_num],
            max_warehouse_num=global_param_dict[gpf.max_warehouse_num],
            min_stock=global_param_dict[gpf.min_stock],
            max_stock=global_param_dict[gpf.max_stock],
            transport_limit=global_param_dict[gpf.transport_limit]
        )
        input_data.global_parameter = global_parameter
        logging.info("successfully loaded global parameter.")


    def generate_demand_city_dict(self, context: Context):
        ddh = field.DemandDistributionHeader

        if context.config.load_from_file:
            demand_city_df = pd.read_csv("{}{}".format(context.config.input_folder, file.DEMAND_FILE),
                                         dtype={ddh.demand_city: str, ddh.demand_qty: float})
        else:
            demand_city_df = self.param_file_dict[file.DEMAND_FILE]

        demand_city_dict = dict()
        for idx, row in demand_city_df.iterrows():
            demand_city = do.DemandCity(city_name=row[ddh.demand_city], demand_qty=row[ddh.demand_qty])
            demand_city_dict[demand_city.city_name] = demand_city

        input_data.demand_city_dict = demand_city_dict
        logging.info("successfully loaded demand_city_dict: {}".format(len(input_data.demand_city_dict)))

    def generate_distance_info(self, context: Context):
        dh = field.DistanceHeader

        if context.config.load_from_file:
            distance_df = pd.read_csv("{}{}".format(context.config.input_folder, file.DISTANCE_FILE),
                                  dtype={dh.demand_city: str, dh.supply_city: str, dh.distance: float, dh.time: float})
        else:
            distance_df = self.param_file_dict[file.DISTANCE_FILE]

        distance_dict = dict()
        supply_city_dict = dict()
        for idx, row in distance_df.iterrows():
            distance = do.Distance(demand_city=row[dh.demand_city],
                                   supply_city=row[dh.supply_city],
                                   mile=row[dh.distance],
                                   transport_hour=row[dh.time])
            distance_dict[(distance.demand_city, distance.supply_city)] = distance

            supply_city = do.SupplyCity(city_name=row[dh.supply_city])
            supply_city_dict[supply_city.city_name] = supply_city

        input_data.distance_dict = distance_dict
        input_data.supply_city_dict = supply_city_dict
        logging.info("successfully loaded supply_city_dict: {}".format(len(input_data.supply_city_dict)))
        logging.info("successfully loaded distance_dict: {}".format(len(input_data.distance_dict)))

    def generate_data(self, context: Context):
        self.generate_global_parameter(context=context)
        self.generate_demand_city_dict(context=context)
        self.generate_distance_info(context=context)
        context.input_data = input_data

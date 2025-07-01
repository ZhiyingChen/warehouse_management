from typing import Dict
import copy
import logging
from ..context import Context
from .storage import ResultStorage
from ..utils.field import VarName
from .. import do

result_storage = ResultStorage()


class ResultProcessor:
    def __init__(self, sol_dict: Dict[str, dict]):
        self.sol_dict = sol_dict

    def generate_supply_city_out_dict(self):
        build_city_dict = {city_name: whether_build_storage
                           for city_name, whether_build_storage in
                           self.sol_dict[VarName.y_whether_use_supply_city_var].items()
                           if whether_build_storage > 0.1 and self.sol_dict[VarName.x_supply_city_stock_var][
                               city_name] > 0.1}

        supply_city_out_dict = dict()
        for city_name, whether_build_storage in build_city_dict.items():
            supply_city_out = do.SupplyCity(city_name=city_name)
            supply_city_out.whether_build_warehouse = True
            supply_city_out.stock_level = self.sol_dict[VarName.x_supply_city_stock_var][city_name]
            supply_city_out.to_demand_city_dict = {demand_city_name: round(supply_qty, 4)
                                                   for (demand_city_name, supply_city_name), supply_qty in
                                                   self.sol_dict[
                                                       VarName.z_demand_from_supply_qty_var].items()
                                                   if supply_city_name == city_name
                                                   }
            supply_city_out.out_rate = sum(supply_qty for demand_city_name, supply_qty in
                                           supply_city_out.to_demand_city_dict.items()) / supply_city_out.stock_level
            supply_city_out_dict[city_name] = supply_city_out

        result_storage.supply_city_out_dict = supply_city_out_dict
        logging.info("generated supply city out dict: {}".format(len(supply_city_out_dict)))

    def generate_demand_city_out_dict(self, context: Context):
        demand_city_out_dict = copy.deepcopy(context.input_data.demand_city_dict)

        for (demand_city_name, supply_city_name), supply_qty in self.sol_dict[
            VarName.z_demand_from_supply_qty_var].items():
            if supply_qty < 1e-3:
                continue

            demand_city_out = demand_city_out_dict[demand_city_name]
            demand_city_out.from_supply_city_dict[supply_city_name] = round(supply_qty, 4)

        for demand_city_name, demand_city_out in demand_city_out_dict.items():
            demand_city_out.satisfied_rate = sum(
                v for k, v in demand_city_out.from_supply_city_dict.items()) / demand_city_out.demand_qty

        result_storage.demand_city_out_dict = demand_city_out_dict
        logging.info("generated demand city out dict: {}".format(len(demand_city_out_dict)))

    def generate_kpi(self, context: Context):
        input_data = context.input_data
        # demand_cover_rate
        result_storage.total_demand_qty = sum(demand_city_out.demand_qty for demand_city_name, demand_city_out in
                                              result_storage.demand_city_out_dict.items())
        result_storage.demand_cover_rate = 1 - (result_storage.total_demand_qty -
                                                sum(supply_qty for supply_city_name, supply_city_out in
                                                    result_storage.supply_city_out_dict.items()
                                                    for demand_city_name, supply_qty in
                                                    supply_city_out.to_demand_city_dict.items())) / \
                                           result_storage.total_demand_qty
        result_storage.warehouse_cost = sum(supply_city_out.stock_level for supply_city_name, supply_city_out in
                                            result_storage.supply_city_out_dict.items()) * input_data.global_parameter.stock_cost_rate
        result_storage.transport_cost = sum(
            supply_qty * input_data.distance_dict[(demand_city_name, supply_city_name)].mile
            for supply_city_name, supply_city_out in
            result_storage.supply_city_out_dict.items()
            for demand_city_name, supply_qty in
            supply_city_out.to_demand_city_dict.items()) * input_data.global_parameter.transport_cost_rate

        result_storage.lack_cost = (1 - result_storage.demand_cover_rate) * result_storage.total_demand_qty * \
                                   input_data.global_parameter.lack_cost

        result_storage.fund_cost = sum(supply_city_out.stock_level for supply_city_name, supply_city_out in
                                       result_storage.supply_city_out_dict.items()) * input_data.global_parameter.produce_cost * input_data.global_parameter.fund_rate

        result_storage.total_cost = result_storage.fund_cost + \
                                    result_storage.warehouse_cost + \
                                    result_storage.transport_cost + \
                                    result_storage.lack_cost

    def generate_results(self, context: Context):
        self.generate_supply_city_out_dict()
        self.generate_demand_city_out_dict(context=context)
        self.generate_kpi(context=context)

        context.result_storage = result_storage

from ..context import Context
from ..utils import field, file
import pandas as pd


class ResultDumper:
    def __init__(self):
        pass

    @staticmethod
    def generate_supply_city_out_file(context: Context):
        osch = field.OutSupplyCityHeader
        col = [
                  osch.city_name,
                  osch.stock_level,
                  osch.out_rate,
              ] + [dmd_city_name for dmd_city_name in context.result_storage.demand_city_out_dict]

        record_lt = []
        for supply_city_name, supply_city_out in context.result_storage.supply_city_out_dict.items():
            record = {
                osch.city_name: supply_city_name,
                osch.stock_level: supply_city_out.stock_level,
                osch.out_rate: '{}%'.format(round(supply_city_out.out_rate, 4) * 100)
            }
            for dmd_city_name in context.result_storage.demand_city_out_dict:
                supply_qty = supply_city_out.to_demand_city_qty(demand_city_name=dmd_city_name)
                record[dmd_city_name] = round(supply_qty, 3)
            record_lt.append(record)

        supply_city_out_df = pd.DataFrame(record_lt, columns=col)

        if context.config.load_from_file:
            supply_city_out_df.to_csv('{}{}'.format(context.config.output_folder, file.OUT_SUPPLY_CITY_FILE),
                                      index=False,
                                      encoding='gbk')
        return supply_city_out_df

    @staticmethod
    def generate_demand_city_out_file(context: Context):
        odch = field.OutDemandCityHeader
        col = [odch.demand_city,
               odch.demand_qty,
               odch.satisfied_rate
               ] + [supply_city_name for supply_city_name in context.result_storage.supply_city_out_dict]

        record_lt = []
        for demand_city_name, demand_city_out in context.result_storage.demand_city_out_dict.items():
            record = {
                odch.demand_city: demand_city_name,
                odch.demand_qty: demand_city_out.demand_qty,
                odch.satisfied_rate: "{}%".format(round(demand_city_out.satisfied_rate, 4) * 100)
            }
            for supply_city_name in context.result_storage.supply_city_out_dict:
                supply_qty = demand_city_out.from_supply_city_qty(supply_city_name=supply_city_name)
                record[supply_city_name] = round(supply_qty, 3)
            record_lt.append(record)

        demand_city_out_df = pd.DataFrame(record_lt, columns=col)

        if context.config.load_from_file:
            demand_city_out_df.to_csv("{}{}".format(context.config.output_folder, file.OUT_DEMAND_CITY_FILE), index=False,
                                      encoding="gbk")
        return demand_city_out_df

    @staticmethod
    def generate_kpi_file(context: Context):
        okh = field.OutKpiHeader
        okf = field.OutKpiField
        col = [okh.name, okh.value]

        record_lt = []
        record = {
            okh.name: okf.total_demand_qty,
            okh.value: round(context.result_storage.total_demand_qty, 3)
        }
        record_lt.append(record)

        record = {
            okh.name: okf.demand_cover_rate,
            okh.value: "{}%".format(round(context.result_storage.demand_cover_rate, 4) * 100)
        }
        record_lt.append(record)

        record = {
            okh.name: okf.total_cost,
            okh.value: round(context.result_storage.total_cost, 3)
        }
        record_lt.append(record)

        record = {
            okh.name: okf.warehouse_cost,
            okh.value: round(context.result_storage.warehouse_cost, 3)
        }
        record_lt.append(record)

        record = {
            okh.name: okf.transport_cost,
            okh.value: round(context.result_storage.transport_cost, 3)
        }
        record_lt.append(record)

        record = {
            okh.name: okf.lack_cost,
            okh.value: round(context.result_storage.lack_cost, 3)
        }
        record_lt.append(record)

        record = {
            okh.name: okf.fund_cost,
            okh.value: round(context.result_storage.fund_cost, 3)
        }
        record_lt.append(record)

        kpi_df = pd.DataFrame(record_lt, columns=col)

        if context.config.load_from_file:
            kpi_df.to_csv("{}{}".format(context.config.output_folder, file.OUT_KPI_FILE), index=False, encoding="gbk")
        return kpi_df

    def generate_all_files(self, context: Context):
        demand_city_out_df = self.generate_demand_city_out_file(context=context)
        supply_city_out_df = self.generate_supply_city_out_file(context=context)
        kpi_df = self.generate_kpi_file(context=context)

        result_dict = {
            file.OUT_SUPPLY_CITY_FILE: supply_city_out_df,
            file.OUT_DEMAND_CITY_FILE: demand_city_out_df,
            file.OUT_KPI_FILE: kpi_df
        }
        return result_dict

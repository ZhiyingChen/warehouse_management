from typing import Dict


class SupplyCity:
    def __init__(self, city_name):
        self.city_name = city_name
        self.whether_build_warehouse: bool = False
        self.stock_level: float = 0
        self.to_demand_city_dict: Dict[str, float] = dict()
        self.out_rate: float = 0

    def __str__(self):
        return "SupplyCity({})".format(self.city_name)

    def to_demand_city_qty(self, demand_city_name: str):
        return self.to_demand_city_dict.get(demand_city_name, 0)

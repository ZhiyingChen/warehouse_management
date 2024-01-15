from typing import Dict


class DemandCity:
    def __init__(self, city_name: str, demand_qty: float):
        self.city_name = city_name
        self.demand_qty = demand_qty
        self.from_supply_city_dict: Dict[str, float] = dict()
        self.satisfied_rate: float = 0

    def __str__(self):
        return "DemandCity({}, {})".format(self.city_name, self.demand_qty)

    def from_supply_city_qty(self, supply_city_name: str):
        return self.from_supply_city_dict.get(supply_city_name, 0)

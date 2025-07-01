from typing import Dict
from .. import do


class ResultStorage:
    def __init__(self):
        self.supply_city_out_dict = Dict[str, do.SupplyCity]
        self.demand_city_out_dict = Dict[str, do.DemandCity]
        self.demand_cover_rate: float = 0
        self.total_cost: float = 0
        self.warehouse_cost: float = 0
        self.transport_cost: float = 0
        self.lack_cost: float = 0
        self.fund_cost: float = 0
        self.total_demand_qty: float = 0

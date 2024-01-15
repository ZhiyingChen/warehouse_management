from .. import do
from typing import Dict


class InputData:
    def __init__(self):
        self.supply_city_dict: Dict[str: do.SupplyCity]
        self.demand_city_dict: Dict[str: do.DemandCity]
        self.distance_dict: Dict[(str, str): do.Distance]
        self.global_parameter: do.GlobalParameter

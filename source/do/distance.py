class Distance:
    def __init__(self, demand_city: str, supply_city: str, mile: float, transport_hour: float):
        self.demand_city = demand_city
        self.supply_city = supply_city
        self.mile = mile
        self.transport_hour = transport_hour

    def __str__(self):
        return "Distance({}, {}, {}, {})".format(self.demand_city, self.supply_city, self.mile, self.transport_hour)
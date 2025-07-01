class GlobalParameter:
    def __init__(self, transport_cost_rate: float,
                 stock_cost_rate: float,
                 lack_cost: float,
                 fund_rate: float,
                 produce_cost: float,
                 min_warehouse_num: int,
                 max_warehouse_num: int,
                 min_stock: float,
                 max_stock: float,
                 transport_limit: float):
        self.transport_cost_rate = transport_cost_rate
        self.stock_cost_rate = stock_cost_rate
        self.lack_cost = lack_cost
        self.fund_rate = fund_rate
        self.produce_cost = produce_cost
        self.min_warehouse_num = min_warehouse_num
        self.max_warehouse_num = max_warehouse_num
        self.min_stock = min_stock
        self.max_stock = max_stock
        self.transport_limit = transport_limit

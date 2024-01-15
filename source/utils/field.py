# region header
class GlobalParamHeader:
    name = '名称'
    value = '数量'


class DistanceHeader:
    demand_city = '城市1'
    supply_city = '城市2'
    distance = '距离（公里）'
    time = '时间（小时）'


class DemandDistributionHeader:
    demand_city = '城市'
    demand_qty = '需求量'


class OutSupplyCityHeader:
    city_name = "城市"
    stock_level = "库存水平"
    out_rate = '供给率'


class OutDemandCityHeader:
    demand_city = '城市'
    demand_qty = '需求量'
    satisfied_rate = "满足率"


class OutKpiHeader:
    name = "指标名称"
    value = "指标值"


# endregion


class VarName:
    x_supply_city_stock_var = 'x_supply_city_stock_var'
    y_whether_use_supply_city_var = 'y_whether_use_supply_city_var'
    z_demand_from_supply_qty_var = 'z_demand_from_supply_qty_var'


class GlobalParameterField:
    transport_rate_cost = '运输费率'
    stock_cost_rate = '仓储费率'
    lack_cost = '缺货成本'
    fund_rate = '资金利率'
    produce_cost = '生产成本'
    min_warehouse_num = '仓库数量下限'
    max_warehouse_num = '仓库数量上限'
    min_stock = '仓库库存下限'
    max_stock = '仓库库存上限'
    transport_limit = '运输时间上限'


class OutKpiField:
    total_demand_qty = "总需求量"
    demand_cover_rate = "需求覆盖率"
    total_cost = "总成本"
    warehouse_cost = "仓储成本"
    transport_cost = "运输成本"
    lack_cost = "缺货成本"
    fund_cost = "资金占用成本"

from ..context import Context
from ..utils import model_parameter as mp
from ..utils.field import VarName
from collections import defaultdict
import pyomo.environ as pe
import logging
import os


class ModelManager:
    def __init__(self):
        self.generated_vars = set()
        self.model = pe.ConcreteModel("Warehouse Management")
        self.opt = pe.SolverFactory("glpk")
        self.api_mode = False
        self.output_lp_file = False

    def create_sets(self, context: Context):
        input_data = context.input_data

        self.model.supply_city_set = pe.Set(initialize=[
            i for i in input_data.supply_city_dict
        ])
        logging.info("created supply city set: {}".format(len(self.model.supply_city_set)))

        self.model.demand_city_set = pe.Set(initialize=[
            j for j in input_data.demand_city_dict
        ])
        logging.info("created demand city set: {}".format(len(self.model.demand_city_set)))

        self.model.demand_supply_pair_set = pe.Set(initialize=[
            (j, i) for (j, i), distance in input_data.distance_dict.items()
            if distance.transport_hour <= input_data.global_parameter.transport_limit
        ])
        logging.info("created demand_supply_pair_set: {}".format(len(self.model.demand_supply_pair_set)))

        self.model.supply_city_set_by_demand = defaultdict(set)
        self.model.demand_city_set_by_supply = defaultdict(set)
        for (j, i) in self.model.demand_supply_pair_set:
            self.model.supply_city_set_by_demand[j].add(i)
            self.model.demand_city_set_by_supply[i].add(j)
        logging.info("created supply_city_set_by_demand: {}".format(len(self.model.supply_city_set_by_demand)))
        logging.info("created demand_city_set_by_supply: {}".format(len(self.model.demand_city_set_by_supply)))

    # region create vars
    def create_x_supply_city_stock_var(self):
        if VarName.x_supply_city_stock_var in self.generated_vars:
            return

        self.model.x_supply_city_stock_var = pe.Var(self.model.supply_city_set,
                                                    domain=pe.NonNegativeIntegers)
        logging.info("created x_supply_city_stock_var: {}".format(len(self.model.x_supply_city_stock_var)))
        self.generated_vars.add(VarName.x_supply_city_stock_var)

    def create_y_whether_use_supply_city_var(self):
        if VarName.y_whether_use_supply_city_var in self.generated_vars:
            return

        self.model.y_whether_use_supply_city_var = pe.Var(self.model.supply_city_set,
                                                          domain=pe.Binary)
        logging.info("created y_whether_use_supply_city_var: {}".format(len(self.model.y_whether_use_supply_city_var)))
        self.generated_vars.add(VarName.y_whether_use_supply_city_var)

    def create_z_demand_from_supply_qty_var(self):
        if VarName.z_demand_from_supply_qty_var in self.generated_vars:
            return

        self.model.z_demand_from_supply_qty_var = pe.Var(self.model.demand_supply_pair_set,
                                                         domain=pe.NonNegativeReals)
        logging.info("created z_demand_from_supply_qty_var: {}".format(len(self.model.z_demand_from_supply_qty_var)))
        self.generated_vars.add(VarName.z_demand_from_supply_qty_var)

    # endregion

    # region create constraints
    def create_no_warehouse_no_stock_constr(self, context: Context):
        self.create_x_supply_city_stock_var()
        self.create_y_whether_use_supply_city_var()

        input_data = context.input_data

        def no_warehouse_no_stock_rule_v1(model, i):
            return model.x_supply_city_stock_var[i] <= input_data.global_parameter.max_stock * \
                   model.y_whether_use_supply_city_var[i]

        self.model.no_warehouse_no_stock_constr_v1 = pe.Constraint(self.model.supply_city_set,
                                                                   rule=no_warehouse_no_stock_rule_v1)
        logging.info(
            "created no_warehouse_no_stock_constr_v1: {}".format(len(self.model.no_warehouse_no_stock_constr_v1)))

        # def no_warehouse_no_stock_rule_v2(model, i):
        #     return input_data.global_parameter.min_stock * \
        #            model.y_whether_use_supply_city_var[i] <= model.x_supply_city_stock_var[i]
        #
        # self.model.no_warehouse_no_stock_constr_v2 = pe.Constraint(self.model.supply_city_set,
        #                                                            rule=no_warehouse_no_stock_rule_v2)
        # logging.info(
        #     "created no_warehouse_no_stock_constr_v2: {}".format(len(self.model.no_warehouse_no_stock_constr_v2)))

    def create_warehouse_stock_limit_constr(self, context: Context):
        self.create_x_supply_city_stock_var()

        input_data = context.input_data

        self.model.warehouse_stock_upper_limit_constr = pe.Constraint(
            expr=sum(v for k, v in self.model.x_supply_city_stock_var.items()) <= input_data.global_parameter.max_stock
        )
        logging.info(
            "created warehouse_stock_upper_limit_constr: {}".format(len(self.model.warehouse_stock_upper_limit_constr)))

        self.model.warehouse_stock_lower_limit_constr = pe.Constraint(
            expr=sum(v for k, v in self.model.x_supply_city_stock_var.items()) >= input_data.global_parameter.min_stock
        )
        logging.info(
            "created warehouse_stock_lower_limit_constr: {}".format(len(self.model.warehouse_stock_lower_limit_constr)))

    def create_warehouse_num_limit_constr(self, context: Context):
        self.create_y_whether_use_supply_city_var()
        input_data = context.input_data

        self.model.warehouse_limit_constr = pe.Constraint(
            expr=(sum(self.model.y_whether_use_supply_city_var[i] for i in
                      self.model.supply_city_set) <= input_data.global_parameter.max_warehouse_num)
        )

        logging.info("created warehouse_limit_constr: {}".format(len(self.model.warehouse_limit_constr)))

        self.model.warehouse_limit_constr_v2 = pe.Constraint(
            expr=(sum(self.model.y_whether_use_supply_city_var[i] for i in
                      self.model.supply_city_set) >= input_data.global_parameter.min_warehouse_num)
        )

        logging.info("created warehouse_limit_constr_v2: {}".format(len(self.model.warehouse_limit_constr_v2)))

    def create_not_exceed_demand_constr(self, context: Context):
        self.create_z_demand_from_supply_qty_var()
        input_data = context.input_data

        def not_exceed_demand_rule(model, j):
            supply_city_set = self.model.supply_city_set_by_demand[j]
            if len(supply_city_set) == 0:
                return pe.Constraint.Skip
            demand_city = input_data.demand_city_dict[j]

            return sum(model.z_demand_from_supply_qty_var[j, i]
                       for i in supply_city_set) <= demand_city.demand_qty

        self.model.not_exceed_demand_constr = pe.Constraint(
            self.model.demand_city_set, rule=not_exceed_demand_rule
        )
        logging.info("created not_exceed_demand_constr: {}".format(len(self.model.not_exceed_demand_constr)))

    def create_not_exceed_stock_constr(self):
        self.create_x_supply_city_stock_var()
        self.create_z_demand_from_supply_qty_var()

        def not_exceed_stock_rule(model, i):
            demand_city_set = self.model.demand_city_set_by_supply[i]
            if len(demand_city_set) == 0:
                return pe.Constraint.Skip

            return sum(model.z_demand_from_supply_qty_var[j, i] for j in demand_city_set) <= \
                   model.x_supply_city_stock_var[i]

        self.model.not_exceed_stock_constrs = pe.Constraint(self.model.supply_city_set, rule=not_exceed_stock_rule)
        logging.info("created not_exceed_stock_constrs: {}".format(len(self.model.not_exceed_stock_constrs)))

    # endregion

    @staticmethod
    def log_opt_solve_info(log_file):
        if os.path.exists(log_file):
            f = open(log_file)
            lines = f.readlines()
            for l in lines:
                logging.info(l.strip("\n"))
            f.close()
            os.remove(log_file)

    def solve_obj(self, context: Context):
        """求解单个目标

        Args:
            objective: 目标
            context: 上下文

        Returns:
            是否求解成功
        """

        log_file = '{}log_{}.log'.format(
            context.config.output_folder, self.model.obj_name)

        if self.output_lp_file:
            self.model.write("{}.lp".format(self.model.obj_name), io_options={
                "symbolic_solver_labels": True})

        if self.api_mode:
            self.opt.set_objective(self.model.obj)
            res = self.opt.solve(self.model, tee=True, logfile=log_file, warmstart=True,
                                 options=self.model.options)

        else:
            res = self.opt.solve(self.model, tee=True, logfile=log_file, options=self.model.options)

        self.log_opt_solve_info(log_file=log_file)
        if res.solver.status in [pe.SolverStatus.ok, pe.SolverStatus.aborted]:
            return True
        else:
            return False

    def solve_cost_obj(self, context: Context):
        logging.info("start solving cost obj...")
        input_data = context.input_data

        obj_expr = sum(v for k, v in self.model.x_supply_city_stock_var.items()) * \
                   input_data.global_parameter.produce_cost * \
                   input_data.global_parameter.fund_rate + \
                   sum(v for k, v in
                       self.model.x_supply_city_stock_var.items()) * input_data.global_parameter.stock_cost_rate + \
                   sum(v * input_data.distance_dict[(j, i)].mile for (j, i), v in
                       self.model.z_demand_from_supply_qty_var.items()) * \
                   input_data.global_parameter.transport_cost_rate + \
                   (sum(input_data.demand_city_dict[j].demand_qty for j in self.model.demand_city_set) -
                    sum(v for (j, i), v in self.model.z_demand_from_supply_qty_var.items())) * \
                   input_data.global_parameter.lack_cost

        if isinstance(obj_expr, float):
            return True

        self.model.obj_name = "cost_obj"
        self.model.obj = pe.Objective(expr=obj_expr, sense=pe.minimize)
        self.model.options = mp.COST_OBJ_CPLEX_PARAM

        solved = self.solve_obj(context=context)

        if solved:
            self.model.cost_fix_constraint = pe.Constraint(
                expr=obj_expr <= pe.value(obj_expr) + mp.COST_OBJ_CPLEX_SLACK)

            if self.api_mode:
                self.opt.add_constraint(
                    self.model.cost_fix_constraint)

            logging.info(
                'finished minimize_cost_obj: {}'.format(pe.value(self.model.obj)))

        return solved

    def create_constraints(self, context: Context):
        self.create_sets(context=context)
        self.create_warehouse_num_limit_constr(context=context)
        self.create_no_warehouse_no_stock_constr(context=context)
        self.create_warehouse_stock_limit_constr(context=context)
        self.create_not_exceed_demand_constr(context=context)
        self.create_not_exceed_stock_constr()

        if self.api_mode:
            self.opt.set_instance(self.model)

    def solve_all_objectives(self, context: Context):
        self.solve_cost_obj(context=context)

    def get_solution(self):
        """获取解集

        Returns:
            解集
        """
        sol_dict = {}
        for k, v in self.model.component_map(ctype=pe.Var).items():
            sol_dict[v.getname()] = {kk: vv() for kk, vv in v.items()}
        return sol_dict

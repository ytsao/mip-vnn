import sys
from typing import List, Tuple, Dict, Any

try:
    import gurobipy as gp
    from gurobipy import GRB
except ImportError:
    print("no gurobi installed!!!!!!!!!!!!!!!!!!!!!!!")
    # sys.exit(1)

from .mip_modeling import Model
from .mip_modeling import MIPOptimizer

class GurobiModel(MIPOptimizer):
    def __init__(self, solver: Model) -> None:
        self.solver: Model = solver
        self.solver.model = gp.Model()
        
        return

    def add_variable(self, lb: int, ub: int, vtype: str, name: str) -> None:
        """
        create single decision variable in MIP model.
        """
        if vtype == "B":
            vtype = GRB.BINARY
        elif vtype == "I":
            vtype = GRB.INTEGER
        elif vtype == "C":
            vtype = GRB.CONTINUOUS
        
        self.solver.addVar(lb=lb, ub=ub, vtype=vtype, name=name)

        return 
    
    def add_objective_function(self, express: Any, sense: str) -> None:
        """
        create objective function in MIP model.
        """
        if type(express) == type(None): return 

        if sense == "minimize":
            sense = GRB.MINIMIZE
        elif sense == "maximize":
            sense = GRB.MAXIMIZE
        
        self.solver.setObjective(express, sense=sense)

        return

    def add_constraint(self, express: Any, name: str) -> None:
        """
        create single constraint in MIP model.
        """
        self.solver.addConstr(express, name=name)

        return

    def change_variable_lb(self, variable: Any, lb: int) -> None:
        """
        change the lower bound for specific decision variable.
        """
        self.solver.model.setAttr("LB", variable, lb)

        return
    
    def change_variable_ub(self, variable: Any, ub: int) -> None:
        """
        change the upper bound for specific decision variable.
        """
        self.solver.model.setAttr("UB", variable, ub)

        return
    
    def export_lp_file(self, name: str) -> None:
        """
        export model to lp file.
        """
        self.solver.model.write(f"{name}.lp")

        return 

    def optimize(self) -> None:
        """
        optimize the model.
        """
        self.solver.model.optimize()

        return
    
    def get_constraints(self) -> Any:
        """
        after building MIP model, we can retrive all of constraints from MIP model object.
        """
        self.solver.model.getConstrs()

        return 

    def get_constraint_name(self, constraint: Any) -> str:
        """
        after building MIP model, we can retrive the name of specific constraint from MIP model object.
        """

        return constraint.ConstrName
    
    def get_primal_solution(self, variable: Any) -> float:
        """
        after solving MIP model, we can retrive the primal solution of specific decision variable from MIP model object.
        """

        return variable.X
    
    def get_dual_solution(self, constraint: Any) -> float:
        """
        after solving MIP model, we can retrive the dual solution of specific constraint from MIP model object.
        """

        return constraint.Pi
    
    def get_solution_status(self) -> str:
        """
        after solving, we can use this function to check the solution status.
        if the solution status is infeasible or unbounded, you might not get the primal/dual solutions.
        """  
        msgdict: dict = {GRB.LOADED: "Loaded", GRB.OPTIMAL: "Optimal", GRB.INFEASIBLE: "Infeasible", GRB.INF_OR_UNBD: "Infeasible or Unbounded", GRB.UNBOUNDED: "Unbounded", GRB.CUTOFF: "CutOff", GRB.ITERATION_LIMIT: "IterationLimit", GRB.NODE_LIMIT: "NodeLimit", GRB.TIME_LIMIT: "TimeLimit",
                         GRB.SOLUTION_LIMIT: "SolutionLimit", GRB.INTERRUPTED: "Interrupted", GRB.NUMERIC: "Numeric", GRB.SUBOPTIMAL: "SubOptimal", GRB.INPROGRESS: "InProgress", GRB.USER_OBJ_LIMIT: "UserObjLimit", GRB.WORK_LIMIT: "WorkLimit", GRB.MEM_LIMIT: "MemoryLimit"}
        
        return msgdict[model.status]
#Project for Principle of Operation Research.
#By Bradford Howe and Alejandro Lopez.

# In this code we want to solve regression using Linear Optimization.
#We are using Gurobi for the Linear Optimization.
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import scipy.sparse as sp

try:
    # The name is RegressionGPModel to based on the projects goal.
    RegressionGPModel  = gp.Model("RegressionReplacement")

    # This are the two varaible for the Linear Optimization.
    #b_0 is the intercetion of the regression line.
    #b_1 is the slope for the regression line.
    b_0 = RegressionGPModel.addVar(vtype = "C", name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", name="b_1")
    
    # Setting constrainst for the model.
    # Replace the first 5 with y and last 5 replace with x.
    # The lowest we can go is zero error.
    RegressionGPModel.addConstr(5- b_0 + b_1*5 >= 0, "c3")
    
    # Set objective function.
    # Same as contrain replace the 5.
    # We want to least of error in the regression.
    RegressionGPModel.setObjective( 5- b_0 + (b_1*5) , GRB.MINIMIZE)

    # This function runs the optimization.
    RegressionGPModel.optimize()
    print("\n","\n","This is a solution for regression replacement.")

    # This loop prints the values for each decision variable in the model.
    for v in RegressionGPModel.getVars():
        print('%s %g' % (v.Varname, v.x))\

    # This prints the final value of the objective function.
    print('Obj: %g' % RegressionGPModel.ObjVal)

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
    

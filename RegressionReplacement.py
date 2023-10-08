
# In response to Homework 3 Question 1 Part 1, this is a solution for Homework 1 Question 4.

import gurobipy as gp
from gurobipy import GRB
import numpy as np
import scipy.sparse as sp

try:

    # This names the model after its task- Checking my work for problem 1 on homework 4.
    RegressionGPModel  = gp.Model("RegressionReplacement")

    # This is setting the coefficients for two continuous variables to be summed and maximized
    # within the constraints set below.
    b_0 = RegressionGPModel.addVar(vtype = "C", name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", name="b_1")
    

    # Setting constrainst for the model.
    #######################################
    # Joy cannot work more than 240 minutes and spends 5 minutes on each toy.
    #m.addConstr(5*C + 5*S + 5*T <= 240, "c1")
    # Kim cannot work more than 360 minutes and spends 4, 8, and 6 minutes on
    # cars, soldiers, and trains, respectively.
    #RegressionGPModel.addConstr(b_0 <= 0, "c1")
    #RegressionGPModel.addConstr(b_1 >= 0, "c2")
    RegressionGPModel.addConstr(5- b_0 + b_1*5 >= 0, "c3")
    # Set objective function.
   #for i in dataset
    RegressionGPModel.setObjective( 5- b_0 + (b_1*5) , GRB.MINIMIZE)

    # This function runs the optimization.
    RegressionGPModel.optimize()
    
    print("\n","\n","This is a solution for regression replacement.")

    # This loop prints the values for each decision variable in the model.
    for v in RegressionGPModel.getVars():
        print('%s %g' % (v.Varname, v.x))\
        #print(b_0)

    # This prints the final value of the objective function.
    print('Obj: %g' % RegressionGPModel.ObjVal)

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
    

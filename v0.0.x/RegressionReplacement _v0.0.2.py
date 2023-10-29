

import gurobipy as gp
from gurobipy import GRB, quicksum
import numpy as np
import scipy.sparse as sp
import pandas as pd
import math

try:
    #Get a dataset
    Data = pd.read_csv("C:/Users/BlueSteel/Desktop/R files/GurobiRegression/BFIsubset.csv")
    TwoVarData = Data.iloc[:,0:1]

    # This names the model after its task- Checking my work for problem 1 on homework 4.
    RegressionGPModel  = gp.Model("RegressionReplacement")

    # This is setting the coefficients for two continuous variables to be summed and maximized
    # within the constraints set below.
    b_0 = RegressionGPModel.addVar(vtype = "C", name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", name="b_1")
    

    # Setting constrainst for the model.
    #######################################
    RegressionGPModel.addConstr(b_0 == b_0, "c1")
    RegressionGPModel.addConstr(b_1 == b_1, "c2")
    RegressionGPModel.addConstr(gp.quicksum (math.sqrt(i) - (b_0 + b_1*i) for i in range (1,11)) >= 0, "c3")
    # Set objective function.
   #for i in dataset
    #RegressionGPModel.setObjective( gp.quicksum( TwoVarData[0:i,0]- b_0 + (b_1*TwosVarData[0:i,1]))
                                                         #       for i in 10,
                                                         #      GRB.MINIMIZE)

    RegressionGPModel.setObjective(gp.quicksum (np.absolute(math.sqrt(i) - (b_0 + b_1*i) ) for i in range (1,11)), GRB.MINIMIZE)
    
    # ff= gp.quicksum (i - b_0 + b_1*i for i in range (1,10))

    # print(ff[:,0])
    
    expr = quicksum(i+1 for i in range(3))

    # Print the quicksum object
    print(expr)

    # This function runs the optimization.
    RegressionGPModel.optimize()
    
    print("/n","/n","This is a solution for regression replacement.")

    # This loop prints the values for each decision variable in the model.
    for v in RegressionGPModel.getVars():
        print('%s %g' % (v.Varname, v.x))
        #print(b_0)

    # This prints the final value of the objective function.
    print('Obj: %g' % RegressionGPModel.ObjVal)

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
    

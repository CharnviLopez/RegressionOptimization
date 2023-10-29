

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
    
    BB0 = range(1,11)
    BB1 = range(1,11)
    
    # Setting constrainst for the model.
    #######################################
    #RegressionGPModel.addConstr(b_0 == b_0, "c1")
    #RegressionGPModel.addConstr(b_1 == b_1, "c2")
    #RegressionGPModel.addConstr(quicksum( i for i in range (1,21)) - quicksum(b_0 + b_1*j  for j in range (1,11)) >= 0, "c3")
    #RegressionGPModel.addConstr(gp.quicksum(i - b_0 - b_1*j  for i in BB0 for j in BB1)>= 0, "c3")
    #RegressionGPModel.addConstr(b_0 > 0 , "c5")
    #RegressionGPModel.addConstr(i-(b_0 + b_1 *j)  for i in BB0 for j in BB1)
    #This doesn't work.
    #RegressionGPModel.addConstr(i - (b_0 + b_1*j)  for i in BB0 for j in BB1== abs(i - (b_0 + b_1*j)  for i in BB0 for j in BB1) )
    # Set objective function.
    #for i in dataset
    #RegressionGPModel.setObjective( gp.quicksum( TwoVarData[0:i,0]- b_0 + (b_1*TwosVarData[0:i,1]))
                                                         #       for i in 10,
                                                         #      GRB.MINIMIZE
    # z_0 = RegressionGPModel.addVar(obj=1, name = "z_0")
    # z_1 = RegressionGPModel.addVar(obj=1, name = "z_1")
    # z_0 = RegressionGPModel.addConstr(z_0 = i-b_0  for i in BB0, "c_z_0")
    # z_1 = RegressionGPModel.addConstr(z_1 = b_1*j for j in BB1, "c_z_0")
    

    #RegressionGPModel.addConstr(z_0 - z_1 == quicksum( i for i in BB0) - quicksum(b_0 + b_1*j  for j in BB1) )

    

    #RegressionGPModel.setObjective(gp.quicksum ( i - b_0 - b_1*j   for i in BB0 for j in BB1), GRB.MINIMIZE)
    #RegressionGPModel.setObjective(gp.quicksum ( (i - (b_0 + b_1*j)) * (i - (b_0 + b_1*j) )   for i in BB0 for j in BB1), GRB.MINIMIZE)
    RegressionGPModel.setObjective( (i - (b_0 + b_1*j)) * (i - (b_0 + b_1*j)    for i in BB0 for j in BB1), GRB.MINIMIZE)
    #RegressionGPModel.setObjective(z_0 + z_1, GRB.MINIMIZE)
    # ff= gp.quicksum (i - b_0 + b_1*i for i in range BB0)

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
    

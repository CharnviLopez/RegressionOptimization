import gurobipy as gp
from gurobipy import GRB, quicksum
import numpy as np
import scipy.sparse as sp
import pandas as pd
import math

try:
    #Get a dataset
    #Data = pd.read_csv("C:/Users/BlueSteel/Desktop/R files/GurobiRegression/BFIsubset.csv")
    #TwoVarData = Data.iloc[:,0:1]
    X= range(10)
    Y = range(10)
    

    # This names the model after its task- Checking my work for problem 1 on homework 4.
    RegressionGPModel  = gp.Model("RegressionReplacement")

    # These are the intercept and slope in a regression.  
    b_0 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_1")
    #z = RegressionGPModel.addVars (obj=1, name = "z")
    #z_0 = RegressionGPModel.addVar(obj=1, name = "z_0")
    #z_1 = RegressionGPModel.addVar(obj=1, name = "z_1")
    z = RegressionGPModel.addVars( range(10), vtype = "C", lb = -GRB.INFINITY, name = "z")
    z_1 = RegressionGPModel.addVars( range(10), vtype = "C", name = "z_1")
    z_2 = RegressionGPModel.addVars( range(10), vtype = "C", name = "z_2")
    
    
    # These are temporary place holders for data which we manipulate.
    
    print ("Len x ", len(X))
    print ("Len y ", len(Y))
    for i in range(10):
        print(X[i])
        print(Y[i])
    
   
 
    

    # Giving value of the range
    #z_1 = range (0,10)
    #z_0 = TempYi
    #z_1 = TempXi
    
    # Setting constrainst for the model.
    #######################################
    # For some reason these are necessary.
    # GRB.INFINITY
    #RegressionGPModel.addConstr(b_0 == b_0, "c1")
    #RegressionGPModel.addConstr(b_1 == b_1, "c2") 
    ###
    # These are attempts to use the Andy & Ollie absolute value solution.
    ### V1
    
    ### V2
    # z_0 = RegressionGPModel.addConstr(z_0 = i-b_0  for i in TempXi, "c_z_0")
    # z_1 = RegressionGPModel.addConstr(z_1 = b_1*j for j in TempYi, "c_z_0")
    
    # New 0.5 version contr
    #RegressionGPModel.addConstrs(TempYi[i]- b_0 - b_1 *TempXi[i] == z for i in range(len(TempXi)))
    RegressionGPModel.addConstrs(z[i] == Y[i] - b_1*X[i] - b_0 for i in range(10))
    RegressionGPModel.addConstrs(z[i] == z_1[i] - z_2[i] for i in range(10))
    #RegressionGPModel.addConstrs(z_0[i+1] - z_1[i+1] == z for i in TempYi)
    #RegressionGPModel.addConstr(z_3[i] == TempXi[i] for i in range(10))
    #RegressionGPModel.addConstr(z[i] == z_0[i] - z_1[i] for i in range (10))
    #RegressionGPModel.addConstr(z >= 0)    


    #RegressionGPModel.addConstr(quicksum( i for i in TempXi) - quicksum(b_0 + b_1*j  for j in range TempYi) >= 0, "c3")
    # We initially thought this constraint would ensure absolute value, however it performs its work at the wrong
    # point in the arithmetic. It also only ignores negative values instead of making them absoulte, which is what we need.
    # See Excel sheet for a demonstration.
    #RegressionGPModel.addConstr(gp.quicksum(i - b_0 - b_1*j  for i in TempXi for j in TempYi)>= 0, "c3")
    
    #This doesn't work.  Attempt to impose ansolute value.
    #RegressionGPModel.addConstr(i - (b_0 + b_1*j)  for i in TempXi for j in TempYi== abs(i - (b_0 + b_1*j)  for i in TempXi for j in TempYi) )
    
    
    # Set objective function using dataset.
    # RegressionGPModel.setObjective( gp.quicksum( TwoVarData[0:i,0]- b_0 + (b_1*TwosVarData[0:i,1]))
                                                         #       for i in 10,
                                                         #      GRB.MINIMIZE
    

    #zi = zi` - zi
    #zi = xi - b0 - b1*yi
    #implied --> zi` - zi = xi - b0 - b1*yi
    
    # Variaous objective equation attempts.
    #RegressionGPModel.setObjective(gp.quicksum ( i - (b_0 + b_1*j) for i in TempXi for j in TempYi), GRB.MINIMIZE)
    #RegressionGPModel.setObjective(gp.quicksum ( (i - (b_0 + b_1*j)) * (i - (b_0 + b_1*j) ) for i in TempXi for j in TempYi), GRB.MINIMIZE)
    #RegressionGPModel.setObjective(( (i - (b_0 + b_1*j))   for i in TempXi for j in TempYi), GRB.MINIMIZE)
    # Andy and Ollie attempt.
    #Move quicksum
    #RegressionGPModel.setObjective(z_0 + z_1, GRB.MINIMIZE)
    RegressionGPModel.setObjective(quicksum(z_1[i] + z_2[i] for i in range(10)), GRB.MINIMIZE)
    #RegressionGPModel.setObjective( quicksum(TempYi[i]- b_0 - b_1 *TempXi[i] for i in range(len(TempXi)))  , GRB.MINIMIZE)


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
    

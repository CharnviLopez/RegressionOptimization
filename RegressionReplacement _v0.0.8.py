import array
import gurobipy as gp
from gurobipy import GRB, quicksum
import numpy as np
import scipy.sparse as sp
import pandas as pd
import math
from sklearn.linear_model import LinearRegression
from sklearn.metrics._plot import regression

try:
    #Get a dataset
    # Data = pd.read_csv("C:/Users/BlueSteel/Desktop/R files/GurobiRegression/BFIsubset.csv")
    # TwoVarData = Data.iloc[:,0:1]

    # This names the model after its task- Checking my work for problem 1 on homework 4.
    RegressionGPModel  = gp.Model("RegressionReplacement")

    # These are the intercept and slope in a regression.  
    b_0 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_0")
    b_1 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_1")
    #V0.0.7 additional variables
    # Because both b_0 and b_1 are fully continuous, they must be standardized
    b_0p = RegressionGPModel.addVar(vtype = "C", name="b_0p")
    b_0n = RegressionGPModel.addVar(vtype = "C", name="b_0n")
    b_1p = RegressionGPModel.addVar(vtype = "C", name="b_1p")
    b_1n = RegressionGPModel.addVar(vtype = "C", name="b_1n")
    
    z = RegressionGPModel.addVar(obj=1, name = "z")
    z_0 = RegressionGPModel.addVar(obj=1, name = "z_0")
    z_1 = RegressionGPModel.addVar(obj=1, name = "z_1")
    
    
    # These are temporary place holders for data which we manipulate.
    TempXi = range(1,31,3)
    TempYi = range(1,11)
    # Giving value of the range
    #z_0 = TempYi
    #z_1 = TempXi
    
    BasicRegData = pd.DataFrame({'X': TempXi,
                                                          'Y':TempYi
                                                          })
    X = BasicRegData['X'].values.reshape(-1,1)
    Y = BasicRegData['Y'].values.reshape(-1,1)

    reg = LinearRegression().fit( X, Y)
   
    
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
    #z_0 = RegressionGPModel.addConstr((z_0 == i-b_0  for i in TempXi), "c_z_0")
    #z_1 = RegressionGPModel.addConstr((z_1 == b_1*j for j in TempYi), "c_z_1")
    
    #From Dr. Validi
    # For conceptualization
    #zi = zi` - zi''
    #zi = xi - b0 - b1*yi
    #implied --> zi` - zi'' = xi - b0 - b1*yi
    # For coding, just use the implied line to skip the other steps.
    #  zi` - zi'' = xi - b0 - b1*yi
    
    
    # V0.0.5  Contstraints
    RegressionGPModel.addConstr(quicksum(i - b_0 - b_1 * i for i in TempXi) == z)
    #RegressionGPModel.addConstr(z_0 - z_1 == z)
    #RegressionGPModel.addConstr(z_3[i] == TempXi[i] for i in range(10))
    #RegressionGPModel.addConstr(z[i] == z_0[i] - z_1[i] for i in range (10))
    
    # V0.0.51 Constraints
    #RegressionGPModel.addConstrs(TempYi[i]- b_0 - b_1 *TempXi[i] == z for i in range(len(TempXi)))
    #RegressionGPModel.addConstr(i - b_0 - b_1 * i  == z_0-z_1 for i in TempXi)
    #RegressionGPModel.addConstr(z_0 - z_1 == z)
    #RegressionGPModel.addConstr(z >= 0)
    #RegressionGPModel.addConstr(z_3[i] == TempXi[i] for i in range(10))
    #RegressionGPModel.addConstr(z[i] == z_0[i] - z_1[i] for i in range (10))

    # V0.0.6  Constraints
    RegressionGPModel.addConstr(quicksum( i - b_0 - b_1*j for i in TempXi for j in TempYi) == z_0 - z_1)
    RegressionGPModel.addConstr(z_0 - z_1 >= 0)
    
    # v0.0.7 Constraints
    # RegressionGPModel.addConstr(b_0 == b_0p - b_0n, name = "b_0std")
    # RegressionGPModel.addConstr(b_1 == b_1p - b_1n, name = "b_1std")
    # RegressionGPModel.addConstr(b_0p + b_0n >= 0, name = "b_0+")
    # RegressionGPModel.addConstr(b_1p + b_1n >= 0, name = "b_1+")

    # V0.0.8 Constraints
    # RegressionGPModel.addConstr(b_0 == b_0p - b_0n, name = "b_0std")
    # RegressionGPModel.addConstr(b_1 == b_1p - b_1n, name = "b_1std")
    # RegressionGPModel.addConstr(b_0p + b_0n >= 0, name = "b_0+")
    # RegressionGPModel.addConstr(b_1p + b_1n >= 0, name = "b_1+")
    # RegressionGPModel.addConstr(b_0p >= 0, name = "b_0p")
    # RegressionGPModel.addConstr(b_0n >= 0, name = "b_0n")
    # RegressionGPModel.addConstr(b_1p >= 0, name = "b_1p")
    # RegressionGPModel.addConstr(b_1n >= 0, name = "b_1n")
    

    # See Excel sheet for a demonstration.
    #RegressionGPModel.addConstr(gp.quicksum(i - b_0 - b_1*j  for i in TempYi for j in TempXi) >= 0, "c3")
    #RegressionGPModel.addConstr(gp.quicksum(i - b_0 - b_1*j  for i in TempYi for j in TempXi) <= 100, "c3")
    
    #This doesn't work.  Attempt to impose ansolute value.
    #RegressionGPModel.addConstr(i - (b_0 + b_1*j)  for i in TempXi for j in TempYi== abs(i - (b_0 + b_1*j)  for i in TempXi for j in TempYi) )
    
    
    # Set objective function using dataset.
    # Variaous objective equation attempts.
    #RegressionGPModel.setObjective(gp.quicksum ( i - (b_0 + b_1*j) for i in TempXi for j in TempYi), GRB.MINIMIZE)
    # Successfully squares the equation, keeping the solutions positive but returns the wrong varible values and multiplies the objective value by 10.
    #RegressionGPModel.setObjective(gp.quicksum ( (i - (b_0 + b_1*j)) * (i - (b_0 + b_1*j) ) for i in TempYi for j in TempXi), GRB.MINIMIZE)
    #RegressionGPModel.setObjective(gp.quicksum ( (i - (b_0 + b_1*j))^2  for i in TempYi for j in TempXi), GRB.MINIMIZE)
    # Can't convert argument to equation (needs quicksum).    
    #RegressionGPModel.setObjective(( (i - (b_0 + b_1*j))   for i in TempXi for j in TempYi), GRB.MINIMIZE)
    #V0.0.5
    #RegressionGPModel.setObjective(quicksum(z), GRB.MINIMIZE)
    #####################
    # V0.0.6 Andy and Ollie attempt.
    RegressionGPModel.setObjective(z_0 + z_1, GRB.MINIMIZE)
    #######################
    # With V.0.0.7 Constraints
    # Infeasible or unbounded. 
    #RegressionGPModel.setObjective(   quicksum( (i - ( (b_0p-b_0n) + (b_1p-b_1n)  *j) )   for i in TempXi for j in TempYi), GRB.MINIMIZE)
    # Runs, wrong answer. Variables all = 0 with an obj value of 550.
    #RegressionGPModel.setObjective(   quicksum( (i + ( (b_0p+b_0n) + (b_1p+b_1n)  *j) )   for i in TempXi for j in TempYi), GRB.MINIMIZE)
    # Runs, wrong answer.
    #RegressionGPModel.setObjective(   quicksum( (i - (b_0 + b_1*j) )   for i in TempXi for j in TempYi), GRB.MINIMIZE)
    #Infeasible
    #RegressionGPModel.setObjective(   quicksum( (i - (b_0p + b_0n) - (b_1p + b_1n)*j  )   for i in TempYi for j in TempXi), GRB.MINIMIZE)
     # With V.0.0.8 Constraints
    # Infeasible or unbounded. 
    #RegressionGPModel.setObjective(   quicksum( (i - ( (b_0p-b_0n) + (b_1p-b_1n)  *j) )   for i in TempXi for j in TempYi), GRB.MINIMIZE)
    # Runs, wrong answer.    Variables all = 0 with an obj value of 550.
    #RegressionGPModel.setObjective(   quicksum( (i + ( (b_0p+b_0n) + (b_1p+b_1n)  *j) )   for i in TempXi for j in TempYi), GRB.MINIMIZE)
    # Runs, wrong answer.
    #RegressionGPModel.setObjective(   quicksum( (i - (b_0 + b_1*j) )   for i in TempXi for j in TempYi), GRB.MINIMIZE)
    #Unfeasible
    #RegressionGPModel.setObjective(   quicksum( (i - (b_0p + b_0n) - (b_1p + b_1n)*j  )   for i in TempYi for j in TempXi), GRB.MINIMIZE)



    # print("one")
    # print(gp.quicksum ( (i - (b_0 + b_1*j))^2 )for i in TempYi for j in TempXi)
    # print("two")
    # This function runs the optimization.
    RegressionGPModel.optimize()
    
    print("\nBasic regression with given data.")
    print("Intercept: ", round(reg.intercept_[0], 3))
    print("Coefficient: ", [round(coef, 2) for coef in reg.coef_[0]])

    print("\nThis is a solution for regression replacement.")

    # This loop prints the values for each decision variable in the model.
    for v in RegressionGPModel.getVars():
        print('%s %g' % (v.Varname, v.x))
        #print(b_0)

    # This prints the final value of the objective function.
    print('Obj: %g' % RegressionGPModel.ObjVal)

# This is an error handler for Gurobi.
except gp.GurobiError as e:
    print('Error code ' + str(e.errno) +': ' + str(e))
    

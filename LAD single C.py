from gurobipy import GRB, quicksum
import gurobipy as gp
import pandas as pd
import math
import time
import statsmodels.api as sm

#Least Absolute Distance (LAD) regression comparison, Python vs Gurobi.

#Get a dataset from XYregData.csv in Github
#url = 'https://raw.githubusercontent.com/CharnviLopez/RegressionOptimization/main/XYregData.csv?token=GHSAT0AAAAAACK5BZDY6OOBVL2YHUB3H7LOZLU2EPQ'
#Data = pd.read_csv(url)
#Student 1 computer
Data = pd.read_csv("C:/RegressionOptimizationFoyer/RegressionOptimization/XYregData.csv")
#Data = pd.read_csv("C:/Users/BlueSteel/Desktop/R files/GurobiRegression/BFIsubset.csv")
#Student 2 computer
#Data = pd.read_csv("/Users/Crow/Desktop/POR/XYregData.csv")

#Data range input
X = Data.iloc[0:99,0]
Y = Data.iloc[0:99,1]
    
# Assign name for Gurobi
RegressionGPModel  = gp.Model("RegressionReplacement")

#Silence Gurobi Code
RegressionGPModel.setParam('OutputFlag', 0)
    
# These are the intercept(b_0) and coefficient(b_1) in a regression.  
b_0 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_0")
b_1 = RegressionGPModel.addVar(vtype = "C", lb = -GRB.INFINITY, name="b_1")
    
# These variable allow Gurobi to interpret an absolute value for the regression error.
z = RegressionGPModel.addVars( range(len(X)), vtype = "C", lb = -GRB.INFINITY, name = "z")
z_1 = RegressionGPModel.addVars( range(len(X)), vtype = "C", name = "z_1")
z_2 = RegressionGPModel.addVars( range(len(X)), vtype = "C", name = "z_2")
    
# This allows for a LAD regression method.
RegressionGPModel.addConstrs(z[i] == (Y[i] - b_1*X[i] - b_0) for i in range(len(X)))
RegressionGPModel.addConstrs(z[i] == z_1[i] - z_2[i] for i in range(len(X)))
    
#Gurobi runs the LAD regression
RegressionGPModel.setObjective(quicksum(z_1[i] + z_2[i] for i in range(len(X))), GRB.MINIMIZE)
RegressionGPModel.optimize()
    
#Print Gurobi data
v = RegressionGPModel.getVars()
print("Gurobi Intercept:", b_0.X)
print("Gurobi Coefficient:", b_1.X)
    
#  LAD regression using statsmodels with HuberT norm (robust to outliers)
K = sm.add_constant(X)
lad_model = sm.RLM(Y, K, M=sm.robust.norms.HuberT()).fit()

# Get the intercept and coeficcient from Python
intercept = lad_model.params[0]
coefficient = lad_model.params[1:]

#Print Pythone data
print("Python Intercept:", intercept)
print("Python Coefficients:", coefficient)

#Print diffrence
print("Intercept diffrence", b_0.X - intercept)
print("Intercept diffrence", b_1.X - coefficient)

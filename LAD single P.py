import pandas as pd
import time
import statsmodels.api as sm

#Least Absolute Distance (LAD) single Python

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

#Timer start
start = time.time()

# LAD regression using statsmodels with HuberT norm (robust to outliers)
K = sm.add_constant(X)
lad_model = sm.RLM(Y, K, M=sm.robust.norms.HuberT()).fit()

#Timer stop
end = time.time()

#Print Python data
print("\nPython LAD regression with statsmodels package.")
print("Python Intercept:", intercept)
print("Python Coefficients:", coefficient)
print("Total time", end-start )

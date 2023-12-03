import pandas as pd
import time
import statsmodels.api as sm

#LAD loop Python

#Get a dataset
#RegData = pd.read_csv('https://raw.githubusercontent.com/CharnviLopez/RegressionOptimization/main/XYregData.csv?token=GHSAT0AAAAAACK5BZDY7H5SP2CZKZJAIZ7EZLHNNEA')
#RegData = pd.read_csv("C:/Users/BlueSteel/Desktop/R files/GurobiRegression/BFIsubset.csv")
RegData = pd.read_csv("C:/RegressionOptimizationFoyer/RegressionOptimization/XYregData.csv")
#RegData = pd.read_csv("/Users/Crow/Desktop/POR/XYregData.csv")

RegStart = time.time()    
for i in range(3,9999):
    Xreg = RegData.iloc[0:i, 0]
    Yreg = RegData.iloc[0:i, 1]
    
    K = sm.add_constant(Xreg)
    
    lad_model = sm.RLM(Yreg, K, M=sm.robust.norms.HuberT()).fit()
    print(i)
    
RegEnd = time.time()
print("\nPython LAD regression with statsmodels package.")
print("Total time", RegEnd - RegStart)

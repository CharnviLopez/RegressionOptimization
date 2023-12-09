import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import time

#OLS single Python

#Get a dataset
#Data = pd.read_csv('https://raw.githubusercontent.com/CharnviLopez/RegressionOptimization/main/XYregData.csv?token=GHSAT0AAAAAACK5BZDZQMHVQXNCHH2PUAP4ZLHMRIQ
RegData = pd.read_csv("C:/RegressionOptimizationFoyer/RegressionOptimization/XYregData.csv")
#RegData = pd.read_csv("/Users/Crow/Desktop/POR/XYregData.csv")

RegStart = time.time() 
Xreg = RegData.iloc[0:99,0].values.reshape(-1, 1)
Yreg = RegData.iloc[0:99,1]
reg = LinearRegression().fit(Xreg,Yreg)
RegEnd = time.time()
#print("Intercept:", reg.intercept_)
#print("Coefficients:", reg.coef_)


print("\nPython OLS regression with sklearn package.")
print("Total time", RegEnd - RegStart)        
    
    
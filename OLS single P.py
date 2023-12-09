import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import time

#Ordinary Least Squares (OLS) single with Python

#Get a dataset from XYregData.csv in Github
#url = 'https://raw.githubusercontent.com/CharnviLopez/RegressionOptimization/main/XYregData.csv?token=GHSAT0AAAAAACK5BZDY6OOBVL2YHUB3H7LOZLU2EPQ'
#Data = pd.read_csv(url)
#Student 1 computer
#Data = pd.read_csv("C:/RegressionOptimizationFoyer/RegressionOptimization/XYregData.csv")
#Data = pd.read_csv("C:/Users/BlueSteel/Desktop/R files/GurobiRegression/BFIsubset.csv")
#Student 2 computer
Data = pd.read_csv("/Users/Crow/Desktop/POR/XYregData.csv")

#Timer start
Start = time.time() 

#Data range input
X = Data.iloc[0:99,0].values.reshape(-1, 1)
Y = Data.iloc[0:99,1]

# OLS regression with sklearn package
reg = LinearRegression().fit(Xreg,Yreg)

#Timer stop
End = time.time()

#Print Python data
print("\nPython OLS regression with sklearn package.")
print("Python Intercept:", reg.intercept_)
print("Python Coefficients:", reg.coef_)
print("Total time", End - Start)       
    

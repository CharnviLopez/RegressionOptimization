import pandas as pd
import time
import statsmodels.api as sm

#Least Absolute Distance (LAD) loop time with Python

#Get a dataset from XYregData.csv in Github
#url = 'https://raw.githubusercontent.com/CharnviLopez/RegressionOptimization/main/XYregData.csv?token=GHSAT0AAAAAACK5BZDY6OOBVL2YHUB3H7LOZLU2EPQ'
#Data = pd.read_csv(url)
#Student 1 computer
Data = pd.read_csv("C:/RegressionOptimizationFoyer/RegressionOptimization/XYregData.csv")
#Data = pd.read_csv("C:/Users/BlueSteel/Desktop/R files/GurobiRegression/BFIsubset.csv")
#Student 2 computer
#Data = pd.read_csv("/Users/Crow/Desktop/POR/XYregData.csv")

#Timer start
Start = time.time() 
#Data range input, and start of loop
for i in range(3,99):
    X = Data.iloc[0:i, 0]
    Y = Data.iloc[0:i, 1]
    
    # LAD regression using statsmodels with HuberT norm (robust to outliers)
    K = sm.add_constant(X)
    lad_model = sm.RLM(Y, K, M=sm.robust.norms.HuberT()).fit()
    
    #Print i to know which regression it's on
    print(i)
    
#End time and print results
End = time.time()
print("\nPython LAD regression with statsmodels package.")
print("Total time", End - Start)

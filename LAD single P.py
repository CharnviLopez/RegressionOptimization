import pandas as pd
import time
import statsmodels.api as sm

#LAD single Python

#Get a dataset
#Data = pd.read_csv('https://raw.githubusercontent.com/CharnviLopez/RegressionOptimization/main/XYregData.csv?token=GHSAT0AAAAAACK5BZDY7H5SP2CZKZJAIZ7EZLHNNEA')
#Data = pd.read_csv("C:/Users/BlueSteel/Desktop/R files/GurobiRegression/BFIsubset.csv")
Data = pd.read_csv("C:/RegressionOptimizationFoyer/RegressionOptimization/XYregData.csv")
#Data = pd.read_csv("/Users/Crow/Desktop/POR/XYregData.csv")

X = Data.iloc[0:99999,0]
Y = Data.iloc[0:99999,1]

start = time.time()
# Add constant for intercept term
K = sm.add_constant(X)

# LAD regression using statsmodels with HuberT norm (robust to outliers)
lad_model = sm.RLM(Y, K, M=sm.robust.norms.HuberT()).fit()
end = time.time()

print("\nPython LAD regression with statsmodels package.")
print("Total time", end-start )
#print(lad_model.summary())
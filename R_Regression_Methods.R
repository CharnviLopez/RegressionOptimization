# Psych library hosts the OLS regression function
library(psych)
# L1pack library hosts the LAD regression function
library(L1pack)


# Pull laboratory data into a dataframe.
a = read.table("XYregData.csv",
               sep = ",",
               header = T)


##########################################
##########################################
## OLS regression method single run

# Set data size here (R starts indexing at 1 not 0)
RegSubset = a[1:100,]

# g and h record the system time immediately before and after running 
# the regression. Running the line h-g will display the computation time for
# the method.
g = Sys.time()
ff = lm(Y~X, RegSubset)
h = Sys.time()
h-g


##########################################
##########################################
## LAD regression method single run

# Set data size here (R starts indexing at 1 not 0)
RegSubset = a[1:100,]

# g and h record the system time immediately before and after running 
# the regression. Running the line h-g will display the computation time for
# the method.
g = Sys.time()
ff = lm(Y~X, RegSubset)
h = Sys.time()
h-g


##########################################
##########################################
## OLS regression method iterative loop 

# Set loop size here (R starts indexing at 1 not 0)
# R will run a regression for a data set equal in length to the loop
# number.
g = Sys.time()
for (i in 1:10000)
{
   ff = lm(RegSubset[1:i,2]~RegSubset[1:i,1])
}
h = Sys.time()
h-g


##########################################
##########################################
## LAD regression method iterative loop 

# Set data size here (R starts indexing at 1 not 0)
# R will run a regression for a data set equal in length to the loop
# number.
g = Sys.time()
for (i in 3:102)
{
   ff = lad(RegSubset[1:i,2]~RegSubset[1:i,1])
}
h = Sys.time()
h-g




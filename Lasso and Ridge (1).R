### Data
setwd("~/Desktop")
credit <- read.csv("Credit.csv")
dim(credit)
str(credit)
credit
# remove column 1 (index column)
credit1 <- credit[,-1]
credit1
# Ensure that all missing values are removed
# remove na datas
credit1 <- na.omit(credit1)
nrow(credit)

set.seed(12358)

# Look for multicollinearity
library("GGally")
library(ggplot2)
ggpairs(credit1)
#get a general idea of multicollinearity 

# # Divide the data into a training and test set
# N <- nrow(credit1)
# 
# # 75% of data goes to training set
# target <- round(.75*N)
# 
# # Create the vector of N uniform random variables: gp
# gp <- runif(N)
# training <- credit1[gp < .75,]
# test <- credit1[gp >=.75,]
# nrow(training)
# nrow(test)


############################################################
###**** Nonlinear Regression: Ridge and LASSO

# Needed packages to perform Ridge and LASSO
install.packages("MASS")
install.packages("glmnet")
library(MASS)
library(glmnet)


#**************************************
#		Ridge Regression
#**************************************

# Function: glmnet(x, y, family, alpha= , 
#                 nlambda= , lambda= , standardize= )
#gml: genraized linear model (for non linear methods)
# x = input matrix
# y = response variable 
# family is set based on response variable (i.e. 
# family = "gaussian" when y is quantitative)
# if alpha = 0 -> then will use the ridge penalty
# if alpha = 1 -> then will use the LASSO penalty
# nlambda - number of lambda values - default is 100
# lambda - user supplied lambda sequence
# standardize=TRUE is default


# Use model.matrix() function to create x -> not only does
# it produce a matrix corresponding to the p predictors 
# but it also automatically transforms any qualitative 
# variables into dummy variables. This property is important
# because glmnet() can only take numerical, quantitative inputs.

# make sure you remove the first column which will
# leave only the predictors
#have the formula as the first argument 
x <- model.matrix(Balance~., credit1)[,-1]
y <- credit1$Balance

# Fit a model using Ridge regression: 
# use the default of 100 nlambda
#set alpha=0 for Ridge 
ridge1 <- glmnet(x, y, alpha=0, standardize=TRUE)
summary(ridge1)

# Get the dimensions of the coefficients for the model
# should be p + intercept rows by nlambda columns
#the num of predictors +1 and the num of columns
dim(coef(ridge1))

# Look at the lambda values used 
ridge1$lambda[1:10]
summary(ridge1$lambda)

# Extract the coefficients at a single value of lambda
coef(ridge1, s=ridge1$lambda[60])


# if you would like to specify a specific
# sequence of lambdas
lambda_seq <- 10^seq(10,-5,length=150)
#lambda argument--- if you wish to provide your own sequence 
ridge2 <- glmnet(x, y, alpha=0, lambda=lambda_seq)

# Draw a plot of the coefficients 
# Expect to see that the coefficients should be much
# smaller with very large lambda
#svar:x axis the lambda value 
#label = TRUE: number the lines. 
plot(ridge1, xvar="lambda", label=TRUE, main="Ridge Trace for Credit Data")
plot(ridge2, xvar="lambda", label=TRUE, main="Ridge Trace for Credit Data")


## One of the main concerns with Ridge (and LASSO) is with how 
# to choose the best tuning parameter; we can use CV to choose
# the optimal/best lambda

# Function: cv.glmnet(x, x, alpha, lambda, nfolds, type.measure)
# x, y, alpha are all the same arguments from glmnet
# lambda - sequence of lambdas to use - can use default or create own
# nfolds = number of folds to use; default is 10 folds
# type.measure = method to calculate prediction error (5 options)

## Ridge Regression with K-Fold CV
ridge.cv <- cv.glmnet(x, y, nfolds=5, alpha=0, type.measure = "mse" )
#bars---std error(prediction error); larger the lambda, the bigger the shrinkage 
#
# Draw a plot of the training MSE as a funnction of lambda
plot(ridge.cv, main="Ridge Regression using CV")


# Choose the lambda that minimizes the prediction error
##** lambda.min will be the lambda that minimizes the MSE
best_lambda <- ridge.cv$lambda.min

# lambda.1se -> will be the largest value of lambda such that
# the error is within 1 SE of the minimum
ridge.cv$lambda.1se

# Get the coefficients to the Ridge Model
coef(ridge.cv, s=best_lambda)

# Final Model using Lambda chosen from CV
#restrict it to one specific lambda 
ridge_final <- glmnet(x, y, alpha=0, lambda=best_lambda)
coef(ridge_final)


##** You can use the predict function for the ridge model 
# with the optimal lambda from CV
# prd <- predict(ridge1, newx=x_train, s=best_lambda)

# Calculate Training/Test Error
# mean((prd - obs_y)^2)

# Remember at the end to fit the ridge regression using the
# full data set and the lambda selected using CV

##** REMEMBER that Ridge Regression does NOT perform variable
# variable selection



#**************************************
#		Lasso Regression
#**************************************

# We will again be able to use glmnet to perform LASSO regression 
# Use glmnet(x, y, alpha) 
# if alpha = 0 - uses the ridge penalty
# if alpha = 1 - uses the lasso penalty

# Fit a model using LASSO regression
#alpha=1: use lasso panelty instead of ridge 
#nlambda: number of lambdas to run the model 
lasso1 <- glmnet(x, y, alpha=1, nlambda=150)

# Look at the lambda values used 
lasso1$lambda[1:20]

# Extract the coefficients at a single value of lambda
coef(lasso1, s=lasso1$lambda[60])

# Coefficient plot
#put the model in the first arguement 
plot(lasso1, xvar="lambda", label=TRUE, main="Coefficient Plot for LASSO")


# Perform LASSO regression with K-Fold CV
#only need to change the alpha arguement 
lasso.cv <- cv.glmnet(x, y, type.measure="mse", alpha=1)

# Draw plot of MSE as a function of lambda
plot(lasso.cv)

# Coefficient plot as a function of lambda
#gives the same thing as 183
plot(lasso.cv$glmnet.fit, xvar="lambda", label=TRUE)

# Just like Ridge, we want to select the lambda that
# gives us the smallest prediciton error
(lambda.lasso <- lasso.cv$lambda.min)
lasso.cv$lambda.1se

# Final LASSO model
# select the lamdba within the range of lambda.min and mse 
final_lasso <- glmnet(x, y, alpha=1, lambda = lambda.lasso)

# Coefficients for the final model
coef(final_lasso)


# Remember at the end to fit the ridge regression using the
# full data set and the lambda selected using CV

## Things to note - if the tuning parameter is chosen
# wisely, then Ridge and LASSO will actually outperform 
# Least Squares model in terms of prediction error/test set error

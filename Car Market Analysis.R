setwd("~/Desktop/STAT4220/final")
library("GGally")
library(class)
library(gmodels)
library(caret)
library(dplyr)
library(purrr)

set.seed(123456)

### Data
cars <- read.csv("cleaned_car_ad.csv",header=T)
cars <- na.omit(cars)
cars <- cars[cars$price > 0,]
cars$year <- as.numeric(cars$year)
cars$age <- 2016 - cars$year
cars$logprice <- log(cars$price)
colnames(cars)
str(cars)
ggpairs(cars[,-c(1,3,6:10)])


## clustering
cars_scaled <- data.frame(cars[,c(1,3,6:10)],scale(cars[,c(2,4,5,11)]))
cars_scaled <- na.omit(cars_scaled)

tot_withinss <- map_dbl(1:10,  function(k){
  model <- kmeans(x = cars_scaled[,c(9,11)], centers = k, nstart=15)
  model$tot.withinss
})

elbow_df <- data.frame(
  k = 1:10 ,
  tot_withinss = tot_withinss
)

ggplot(elbow_df, aes(x = k, y = tot_withinss)) +
  geom_line() +
  scale_x_continuous(breaks = 1:10)

model_km2 <- kmeans(cars_scaled[,c(9,11)],centers=2,nstart=15)
model_km2
clust_km2 <- model_km2$cluster
cars_scaled_km2 <- mutate(cars_scaled, cluster=clust_km2)
cars_scaled_km2$price_range <- ifelse(cars_scaled_km2$price>mean(cars_scaled_km2$price), "High","Low")
cars_scaled_km2$price_range <- as.factor(cars_scaled_km2$price_range)
ggplot(cars_scaled_km2, aes(x = mileage, y = age, label = price_range, color=factor(cluster))) +
  theme_bw() +
  geom_point() + geom_text(hjust=0, vjust=0, size=3) +
  labs(title = "Car sales - Mileage vs. Age", subtitle ="K-Means, K=2", y = "Age", x = "Mileage", caption = "(based on data from Kaggle)", hjust=0, vjust=0) +
  theme(plot.title = element_text(hjust = 0.5), plot.subtitle = element_text(hjust = 0.5)) +
  guides(color=guide_legend(title="Clusters"))



##################################################################
#### Seperate into training and testing datasets
cars_random <- cars[sample(nrow(cars)),]
N <- nrow(cars)
(target <- round(.90*N))
gp <- runif(N)
training <- cars_random[gp < 0.9,]
test <- cars_random[gp >= 0.9,]
nrow(training)
nrow(test)

#### Modeling
null <- lm(logprice~1, data=training)
full1 <- lm(logprice~.-model-year-age, data=training)
full2 <- lm(logprice~.-model-year-mileage, data=training)

step(null, scope = list(upper = full1), direction = "both")
step(null, scope = list(upper = full2), direction = "both")

fit1 <- lm(formula = logprice ~ price + car + mileage + registration + 
             drive + engType + body, data = training)
summary(fit1)
# fit1 : Adjusted R-squared:  0.8144, p-value: < 2.2e-16

fit2 <- lm(formula = logprice ~ price + age + car + registration + drive + 
             body + engType + engV, data = training)
summary(fit2)

# fit2: Adjusted R-squared:  0.9139 , p-value: < 2.2e-16

final <- fit2
final

### Calculate training error
mean((training$logprice - final$fitted.values)^2)
# training error: 0.07586725

# Testing Error
prd <- predict(final, test)
mean((test$logprice - prd)^2)
# test: 0.09223887

### include in final: why choose kmeans over hierachical


library(mgcv)
library(car)
data1<- read.csv(file="packages_info.csv", header=T)
data1

# check collineation
alias( lm(log(num_downstream_repos) ~ log(num_commits+1) + log(num_authors+1) + log(age+1) + log(stars+1)
           + package_domain + sub_domain + No.layer + dependences + supply_chain_name, data=data1) )

vif_test <- lm(log(num_downstream_repos) ~ log(num_commits+1) + log(num_authors+1) + log(age+1) + log(stars+1)
                + sub_domain + No.layer + dependences + supply_chain_name, data=data1)
vif(vif_test)

g <- gam(log(num_downstream_repos) ~ s(log(num_commits+1)) + s(log(num_authors+1)) + s(log(age+1)) + s(log(stars+1))
          + sub_domain + as.factor(No.layer) + s(dependences) + supply_chain_name, data=data1,
         method = 'REML')

summary(g)



g <- gam(log(num_downstream_repos) ~ s(log(num_authors+1))  + package_domain
          + s(log(dependences)), data=data1,
         method = 'REML')
summary(g)
layout(matrix(1:1, nrow = 1))
plot(g, shade = TRUE)
plot(g, select = 2, pch = 20, shade = TRUE, residuals = TRUE)

AIC(g)

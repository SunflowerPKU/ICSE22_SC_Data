library(rcompanion)
data<-read.csv('first_last_month.csv')

d1 <- data$PT_SC_First
d2 <- data$PT_SC_Last

# caculate effect size
library(coin)
GroupA = d1
GroupB = d2
g = factor(c(rep("GroupA", length(GroupA)), rep("GroupB", length(GroupB))))
v = c(GroupA, GroupB)
wilcox_test(v ~ g)
6.60839/sqrt(length(GroupA)+length(GroupB))

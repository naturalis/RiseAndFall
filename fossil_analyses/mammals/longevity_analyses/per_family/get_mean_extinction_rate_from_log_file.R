data<-read.table(file.choose(), header = T)
data$m_0
#burnin the first 2000 steps
mean(tail(data$m_0,2000))
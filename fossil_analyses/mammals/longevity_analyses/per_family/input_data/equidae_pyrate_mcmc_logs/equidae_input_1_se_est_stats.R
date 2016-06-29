
	setwd("/Users/tobias/Documents/Sweden/PhD/rise_and_fall/longevity_analyses/mammals/families/equidae_pyrate_mcmc_logs")
	tbl = read.table(file = "equidae_input_1_se_est_stats.txt",header = T)
	pdf(file='fequidae_input_1_se_est_stats.pdf',width=12, height=9)
	time = -tbl$time
	par(mfrow=c(2,2))
	library(scales)
	plot(time,tbl$diversity, type="l",lwd = 2, ylab= "Number of lineages", xlab="Time (Ma)", main="Diversity through time", ylim=c(0,max(tbl$M_div,na.rm =T)+1),xlim=c(min(time),0))
	polygon(c(time, rev(time)), c(tbl$M_div, rev(tbl$m_div)), col = alpha("#504A4B",0.5), border = NA)
	plot(time,tbl$median_genus_age, type="l",lwd = 2, ylab = "Median age", xlab="Time (Ma)", main= "Taxon age", ylim=c(0,max(tbl$M_age,na.rm =T)+1),xlim=c(min(time),0))
	polygon(c(time, rev(time)), c(tbl$M_age, rev(tbl$m_age)), col = alpha("#504A4B",0.5), border = NA)
	plot(time,tbl$turnover, type="l",lwd = 2, ylab = "Fraction of new taxa", xlab="Time (Ma)", main= "Turnover", ylim=c(0,max(tbl$M_turnover,na.rm =T)+.1),xlim=c(min(time),0))
	polygon(c(time, rev(time)), c(tbl$M_turnover, rev(tbl$m_turnover)), col = alpha("#504A4B",0.5), border = NA)
	plot(time,tbl$life_exp, type="l",lwd = 2, ylab = "Median longevity", xlab="Time (Ma)", main= "Taxon (estimated) longevity", ylim=c(0,max(tbl$M_life_exp,na.rm =T)+1),xlim=c(min(time),0))
	polygon(c(time, rev(time)), c(tbl$M_life_exp, rev(tbl$m_life_exp)), col = alpha("#504A4B",0.5), border = NA)
	n<-dev.off()
	
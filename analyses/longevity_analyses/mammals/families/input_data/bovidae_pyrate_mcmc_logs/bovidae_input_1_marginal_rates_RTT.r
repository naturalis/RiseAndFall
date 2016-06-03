# 1 files combined:
# 	/Users/tobias/Dropbox/Anthropocene_mammal_extinction/Data/pyrate_output/bovidae_pyrate_mcmc_logs/bovidae_input_1_marginal_rates.log

# 95% HPDs calculated using code from Biopy (https://www.cs.auckland.ac.nz/~yhel002/biopy/)

pdf(file='/Users/tobias/Dropbox/Anthropocene_mammal_extinction/Data/pyrate_output/bovidae_pyrate_mcmc_logs/bovidae_input_1_marginal_rates_RTT.pdf',width=0.6*9, height=0.6*21)
par(mfrow=c(3,1))
library(scales)
L_hpd_m95=c(0.147, 0.147,0.153,0.241,0.25,0.238,0.236,0.172,0.162,0.173,0.17,0.172,0.162,0.166,0.163,0.172,0.173,0.172)
L_hpd_M95=c(0.546, 0.546,0.555,0.869,0.879,0.869,0.864,0.747,0.695,0.694,0.676,0.668,0.649,0.647,0.642,0.647,0.647,0.647)
M_hpd_m95=c(0.034, 0.034,0.037,0.044,0.061,0.071,0.075,0.075,0.075,0.075,0.076,0.076,0.077,0.078,0.078,0.078,0.078,0.078)
M_hpd_M95=c(0.483, 0.483,0.401,0.404,0.411,0.411,0.416,0.418,0.418,0.418,0.415,0.413,0.41,0.41,0.411,0.411,0.411,0.411)
R_hpd_m95=c(-0.25, -0.25,-0.094,-0.066,-0.083,-0.083,-0.086,-0.117,-0.134,-0.14,-0.12,-0.123,-0.118,-0.118,-0.117,-0.107,-0.112,-0.112)
R_hpd_M95=c(0.417, 0.417,0.405,0.73,0.68,0.665,0.648,0.546,0.506,0.491,0.491,0.474,0.463,0.46,0.462,0.471,0.467,0.467)
L_mean=c(0.358, 0.358,0.363,0.488,0.489,0.49,0.479,0.435,0.423,0.421,0.416,0.411,0.405,0.402,0.403,0.404,0.405,0.406)
M_mean=c(0.256, 0.256,0.217,0.219,0.234,0.246,0.252,0.254,0.255,0.255,0.253,0.251,0.245,0.242,0.242,0.242,0.241,0.241)
R_mean=c(0.102, 0.102,0.146,0.269,0.255,0.244,0.227,0.181,0.167,0.165,0.162,0.16,0.161,0.16,0.161,0.163,0.164,0.165)
trans=0.5
age=(0:(18-1))* -1
plot(age,age,type = 'n', ylim = c(0, 0.9669), xlim = c(-18.9,0.9), ylab = 'Speciation rate', xlab = 'Ma',main='bovidae' )
polygon(c(age, rev(age)), c(L_hpd_M95, rev(L_hpd_m95)), col = alpha("#4c4cec",trans), border = NA)
lines(rev(age), rev(L_mean), col = "#4c4cec", lwd=3)
plot(age,age,type = 'n', ylim = c(0, 0.5313), xlim = c(-18.9,0.9), ylab = 'Extinction rate', xlab = 'Ma' )
polygon(c(age, rev(age)), c(M_hpd_M95, rev(M_hpd_m95)), col = alpha("#e34a33",trans), border = NA)
lines(rev(age), rev(M_mean), col = "#e34a33", lwd=3)
plot(age,age,type = 'n', ylim = c(-0.275, 0.803), xlim = c(-18.9,0.9), ylab = 'Net diversification rate', xlab = 'Ma' )
abline(h=0,lty=2,col="darkred")
polygon(c(age, rev(age)), c(R_hpd_M95, rev(R_hpd_m95)), col = alpha("#504A4B",trans), border = NA)
lines(rev(age), rev(R_mean), col = "#504A4B", lwd=3)
n <- dev.off()
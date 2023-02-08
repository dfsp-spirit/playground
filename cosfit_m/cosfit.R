#!/usr/bin/env Rscript

library("R.matlab");

file_contents <- R.matlab::readMat("data.mat");
Y <- file_contents$multMUAz;

y = Y[1,] # Select first column of data only for now.
t <- c(-2.6180,   -1.5708,   -0.5236,    0.5236,   1.5708,    2.6180);

ssp <- spectrum(y)
per <- 1/ssp$freq[ssp$spec==max(ssp$spec)]
reslm <- lm(y ~ sin(2*pi/per*t)+cos(2*pi/per*t))
summary(reslm)

rg <- diff(range(y))
plot(y~t,ylim=c(min(y)-0.1*rg,max(y)+0.1*rg))
lines(fitted(reslm)~t,col=4,lty=2)   # dashed blue line is sin fit

# including 2nd harmonic really improves the fit
reslm2 <- lm(y ~ sin(2*pi/per*t)+cos(2*pi/per*t)+sin(4*pi/per*t)+cos(4*pi/per*t))
summary(reslm2)
lines(fitted(reslm2)~t,col=3)    # soli


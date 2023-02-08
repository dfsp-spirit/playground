
load("data.mat")


data = multMUAz;
nContrast = size(data, 1); % Num columns in data matrix.

%Cosine fitting
cosFitParam = NaN(nContrast, 2);  % Amplitude and phase parameters to extract from the fit.
binCenters = [-2.6180   -1.5708   -0.5236    0.5236    1.5708    2.6180]; % as 2*PI f

mygca = zeros(nContrast,1);
for contrast_idx= 1:nContrast
    cosFitParam = fn_cos_fit(data(contrast_idx, : ), binCenters, contrast_idx); 
    mygca(contrast_idx) = gca;
end 





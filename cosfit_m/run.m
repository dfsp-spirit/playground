
load("data.mat")


data = multMUAz;
nContrast = 6; % coliumn in data matrix

%Cosine fitting
cosFitParam = NaN(nContrast,2);  % Amplitude and phase parameters that I want to extract from the fitting
binCenters = [-2.6180   -1.5708   -0.5236    0.5236    1.5708    2.6180];
sel_method = 3;    % 1=attempt 1, 2=attempt 2, 3=attempt 3
for idxContr = 1:nContrast
    cosFitParam = fn_cos_fit(data(idxContr, : ), binCenters, idxContr, sel_method); 
    mygca(idxContr) = gca;
end 
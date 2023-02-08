function [cosFit] = fn_cos_fit (data, binCenters, iCon) 

DC = mean(data); % DC component of data.

% Initial guess for solver.
amplitude = 1e-6; % Worth messing around with, at least a bit.
phase = 0; % We know for sure.
C = [amplitude, phase, DC];

% Function to fit
fh = @(C,x) C(3) + C(1) * cos(x + C(2));
% Fit with least squares
cosFit = lsqcurvefit(fh, C, binCenters, data);
    
% Plot the result
figure(8);
subplot(2, 3 , iCon);
scatter(rad2deg(binCenters), data, 'b');
hold on;
angles = (-180:180);
plot(angles, fh(cosFit, deg2rad(angles)),'-r');
end

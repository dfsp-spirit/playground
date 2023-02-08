function [cosFit] = fn_cos_fit (data,binCenters,iCon,sel) 
if sel == 1
    % Define Start points, fit-function and fit curve ___________ GIAMMI
    x = binCenters';
    y = data';
    DC = mean(y);
    x0 = [binCenters(1,3) data(1,1)];
    fitfun = fittype( @(a,b,x) DC+a*cos(2*pi*(x+b)) );
    [fitted_curve,~] = fit(x,y,fitfun,'StartPoint',x0);
    
    % Save the coeffiecient values for a,b,c and d in a vector
    cosFit = coeffvalues(fitted_curve);
    
    % Plot the result
    figure(6)
    subplot(2,3,iCon)
    scatter(rad2deg(x),data,'b')
    hold on
    plot(rad2deg(x),fitted_curve(x))
    
elseif sel == 2
    % Define C parameters ___________ JACKSON
    % C = [DC,amplitude,frequency,phase];
    N = numel(data);
    DC = mean(data);
    dataOff = data - DC;
    fourier = 1/N * exp(-1i*binCenters) * dataOff';
    amplitude = 2*(abs(fourier));
    phase = angle(fourier);
    freq = (0: N-1)*(fourier/N); %fourier/N; %(0: N-1)*(fourier/N);
    frequency = freq(4);
    
    C = [DC,amplitude,frequency,phase];
    fh = @( C , x ) C( 1 ) + C( 2 ) * cos( 2 * pi * C( 3 ) * x + C( 4 ) );
    
    % Fit the function with the calculated parameters
    cosFit = lsqcurvefit(fh,C,binCenters,data);
    
    % Plot the result
    figure(7)
    subplot(2,3,iCon)
    scatter(rad2deg(binCenters),data,'b')
    hold on
    % plot(rad2deg(binCenters), fh(C,rad2deg(binCenters)),'-r');
    plot(rad2deg(binCenters), fh(C,binCenters),'-r');
    
elseif sel == 3
    % Define C parameters __________ MARTINA
    % C = [amplitude,phase];
    DC = mean(data); % remove DC component (check if necessary??)
    N = numel(binCenters);
    a = 1/N * exp(-1i*binCenters) * data'; % Extract amp and phase from complex valued wave shape
    amplitude = 2*abs(a);
    phase = angle(a);
    
    C = [amplitude,phase];
    fh = @(C,x) DC + C(1)*cos(2*pi*(x+C(2)));
    
    % Fit the function with the calculated parameters
    
    cosFit = lsqcurvefit(fh,C,binCenters,data);
    
    % Plot the result
    figure(8)
    subplot(2,3,iCon)
    scatter(rad2deg(binCenters),data,'b')
    hold on
    plot(rad2deg(binCenters), fh(C,binCenters),'-r');
end

end

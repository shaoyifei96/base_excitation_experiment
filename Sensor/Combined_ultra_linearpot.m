  %%a = arduino('/dev/cu.usbmodem1421', 'Uno', 'Libraries', 'JRodrigoTech/HCSR04')
 % i = 0
 % while i < 100
  %    i = i+1;
% lin_pot1(i)= readVoltage(a,'A0');
 %lin_pot_dist(i) =  lin_pot1(i)/5+11.12
% If your number X falls between A and B, and you would like Y to fall between C and D, you can apply the following linear transform:
% 
% Y = (X-A)/(B-A) * (D-C) + C
 % end
 % plot(lin_pot1)
  
  %% Measure Distance from Sensed Time
% % * Connect Trig pin to pin D12 on Arduino board.
% % * Connect Echo pin to pin D13 on Arduino board.
% % * Connect VCC pin to 5V pin on Arduino board.
% % * Connect GND pin to GND pin on Arduino board.
%  sensor = addon(a, 'JRodrigoTech/HCSR04', 'D12', 'D13')
% s=serial('/dev/cu.usbmodem1421')%%connect to the other port, to the
% arduino running motor
 %fsopen(s) %Use it now
  %out = fscanf(s) %output data in loop
  %fclose(s) %close port
%   s=serial('/dev/cu.usbmodem1421')
%   fopen(s)
t = 0 ;
x = 0 ;
startSpot = 0;
interv = 1000 ; % considering 1000 samples
step = 0.1 ; % lowering step has a number of cycles and then acquire more data
i=1
%linear pot is 11.12 cm

for i= 1:interv
%     rad_s = fscanf(s);
    lin_pot1(i)= readVoltage(a,'A0');
     lin_pot_dist(i) =  (lin_pot1(i)-lin_pot1(1))/5*11.12;
%ultra(i) = readDistance(sensor)*10; %in cm
ultra(i) = readTravelTime(sensor);
 ultra_distance(i) = (340*(ultra(i)-ultra(1))/.02); %distance in cmeters
end
%%
ultra_distance_smooth = movmean(ultra_distance,5);
PKS_lin_pot = findpeaks(lin_pot_dist);
PKS_ultra = findpeaks(ultra_distance_smooth);
i=1
figure(1)
plot(ultra_distance_smooth)
title('Ultrasonic Sensor')
xlabel('Time (s)')
ylabel('Displacement (cm)')

figure(2)
 plot(lin_pot_dist)
 title('Linear Potentiometer')
xlabel('Time (s)')
ylabel('Displacement (cm)')

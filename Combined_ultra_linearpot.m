  %% Connection to board and senso
  %a = arduino('/dev/cu.usbmodem1421', 'Uno', 'Libraries', 'JRodrigoTech/HCSR04')
  %sensor = addon(a, 'JRodrigoTech/HCSR04', 'D12', 'D13')
  
  % s=serial('/dev/cu.usbmodem1421')%%connect to the other port, to the
% arduino running motor
 %fsopen(s) %Use it now
  %out = fscanf(s) %output data in loop
  %fclose(s) %close port
  %% Ultra Sonic Measure Distance from Sensed Time
% % * Connect Trig pin to pin D12 on Arduino board.
% % * Connect Echo pin to pin D13 on Arduino board.
% % * Connect VCC pin to 5V pin on Arduino board.
% % * Connect GND pin to GND pin on Arduino board.
t = 0 ;
x = 0 ;
interv = 1000 ; % considering this many samples



for i= 1:interv
%     rad_s = fscanf(s); scan from arduio serial port. 
     lin_pot1(i)= readVoltage(a,'A0');
     lin_pot_dist(i) =  (lin_pot1(i)-lin_pot1(1))/5*11.12; %linear pot is 11.12 cm, linearly interpolate and map vlotage (0-5) to distance
    %ultra(i) = readDistance(sensor)*10; % another option, less accurate
    ultra(i) = readTravelTime(sensor);
     ultra_distance(i) = (340*(ultra(i)-ultra(1))/.02); %distance in centimeters
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

#include "DualMC33926MotorShield.h"
//#include <PID_v1.h>

/*
 *Outputs Radian/sec
 *
  Brown: 5V
  Blue: 0
  A: black
  B: White
  Z: Orange
*/

// constants won't change. They're used here to set pin numbers:
const byte A_pin = 2;     // the number of the pushbutton pin
const byte B_pin = 1;      // the number of the LED pin
const byte Z_pin = 3;      // the number of the LED pin
const byte ledPin = 13;
int input;
const int constant = 30;
volatile double CurrentTime;
volatile double ElapsedTime;
volatile double StartTime = 0;
volatile double w;
volatile int counter = 0;
volatile double u = 200;
volatile double sum_error=0;

double Setpoint, Input, Output,Error, prev_err;
float Kp,Ki,Kd;
//volatile long t_p,t_n,t_delta;
//Specify the links and initial tuning parameters
//PID myPID(&Input, &Output, &Setpoint,2,5,1, DIRECT);
DualMC33926MotorShield md;



void stopIfFault()
{
  if (md.getFault())
  {
    Serial.println("fault");
    while(1);
  }
}

void setup()
{
  Serial.begin(9600);
  Serial.println("Dual MC33926 Motor Shield");
  pinMode(ledPin, OUTPUT);
  pinMode(A_pin, INPUT_PULLUP);
  pinMode(7, INPUT);
  attachInterrupt(digitalPinToInterrupt(A_pin), disp, RISING);
 // myPID.SetMode(AUTOMATIC);

  Setpoint = 10;
  Kp = 90;
  Kd = 10;
  Ki = 1;
  md.init();
  //md.setM1Speed(250);
  //delay(40000);

}

void loop()
{
  if(Serial.available()){
    input = Serial.read();
    input =input - 90;
    Serial.print(input);
    if(input > 7 && input < 22){ 
      Setpoint = input;
    }
  }
  while(!digitalRead(7)){
    md.setM1Speed(round(0));
    sum_error = 0;
  }
  Error=Setpoint-w;
  sum_error+=Error;
  Output=Kp*Error+Ki*sum_error+(Error-prev_err)*Kd;//controller
  //Serial.println(Output);
  if(abs(Output)>1000){
    if(Output<-1000){
      Output = -1000;
    }else{
      Output = 1000;
    }
  }
  
  Output = map(Output,-1000,1000,0,400);
  
  int sum_limit = 300;
  if(abs(sum_error)>sum_limit){
    if (sum_error>0){
      sum_error = sum_limit;
    }else{
      sum_error =-sum_limit;
    }
  }

  prev_err = Error;
  //Output = 130;
  md.setM1Speed(round(Output));
  stopIfFault();
  delay(30);

}
//void set_output(){
//  t_n = millis();
//  if(t_n-t_p != 0){
//    t_delta = t_n - t_p;
//  }
//  t_p = t_n;
//}


void disp() {
  ++counter;
  if(counter == constant){
    CurrentTime = millis();
    ElapsedTime = (CurrentTime - StartTime)/1000;
    StartTime = millis();
    counter = 0;
    w = constant * 6.28 / 1024 / ElapsedTime; //rad per sec
    //Serial.println(Setpoint);
    //Serial.println(Output);
    //Serial.println(sum_error);
  }
}



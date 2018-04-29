    /*
    * Ultrasonic Sensor HC-SR04 and Arduino Tutorial
    *
    * Crated by Dejan Nedelkovski,
    * www.HowToMechatronics.com
    *
    */
    // defines pins numbers
    const int trigPin = 12;
    const int echoPin = 13;
    // defines variables
    long duration;
    float distance;
    void setup() {
    pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin, INPUT); // Sets the echoPin as an Input
    pinMode(A0, INPUT);
    Serial.begin(9600); // Starts the serial communication
  
    }
    void loop() {
    // Clears the trigPin
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH);
    // Calculating the distance
    distance= duration*0.034/2.;
    // Prints the distance on the Serial Monitor
    Serial.print(analogRead(A0));
    Serial.print(",");
    Serial.println(distance);
    }

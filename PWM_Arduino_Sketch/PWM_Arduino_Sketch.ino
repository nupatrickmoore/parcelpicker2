//initialize PWM pin
const int PWM_pin = 13;
int PWM_throw = 255;  //initalized throw duty cycle

void setup() {
  // put your setup code here, to run once:
  // initialize serial communication:
  Serial.begin(9600);
  //Declare PWM as output
  pinMode(PWM_pin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  // see if there's incoming serial data:
  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    Serial.readBytes(PWM_throw, 3);
    Serial.print("Received");
    Serial.print('\n');
    Serial.print(PWM_throw);
    Serial.print('\n');
    analogWrite(PWM_pin, PWM_throw);
    delay(5);
  }
}

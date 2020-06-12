//initialize PWM pin
const int PWM_pin = 13;
int Grab_input = 255;  //initalized throw duty cycle

void setup() {
  // put your setup code here, to run once:
  // initialize serial communication:
  Serial.begin(9600);
  //Declare PWM as output
  pinMode(PWM_pin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  // see if there's incoming serial data:
  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    Grab_input = Serial.read();
    Serial.print("Received");
    Serial.print('\n');
    Serial.print(Grab_input);
    Serial.print('\n');
    if(Grab_input == 'H') {
      analogWrite(PWM_pin, 255);
      digitalWrite(LED_BUILTIN, LOW)
    }
    if(Grab_input == 'L') {
      analogWrite(PWM_pin, 0);
      digitalWrite(LED_BUILTIN, HIGH)
    }
    delay(5);
  }
}

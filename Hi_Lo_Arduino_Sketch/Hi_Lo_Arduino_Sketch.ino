//initialize PWM pin
int Grab_input = 255;  //initalized throw duty cycle

void setup() {
  // put your setup code here, to run once:
  // initialize serial communication:
  Serial.begin(9600);
  //Declare PWM as output
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(11, OUTPUT);
  TCCR2B = TCCR2B & B11111000 | B00000011;
}

void loop() {
  // put your main code here, to run repeatedly:
  // see if there's incoming serial data:
  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    Grab_input = Serial.read();
    Serial.print("Received");
    Serial.print('\n');
    if(Grab_input == 'H') {
      analogWrite(11, 140);
      digitalWrite(LED_BUILTIN, LOW);
      Serial.write('H');
      Serial.print("HIGH");
      Serial.print('\n');
    }
    if(Grab_input == 'L') {
      analogWrite(11, 0);
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.write('L');
      Serial.print("LOW");
      Serial.print('\n');
    }
  }
}

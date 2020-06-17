//initialize PWM pin

void setup() {
  // put your setup code here, to run once:
  // initialize serial communication:
  Serial.begin(9600);
  //Declare PWM as output
  pinMode(3, OUTPUT);
  pinMode(11, OUTPUT);
  TCCR2B = TCCR2B & B11111000 | B00000011;
}

void loop() {
  // put your main code here, to run repeatedly:
  // see if there's incomig serial data:
          analogWrite(11, 200);
  }

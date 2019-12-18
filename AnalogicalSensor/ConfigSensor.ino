
const int sensorPin  =  32;
float sensorValue =  0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  sensorValue =  analogRead(sensorPin);
  Serial.println(sensorValue,  DEC);
  delay(500);
}

#include <WiFi.h>
#include <HTTPClient.h>
#include <math.h>
#define LED 2

const char ssid[] = "HUAWEI P20 Pro";
const char password[] = "AcC&Ss0.";

const uint16_t port = 8000;
const char * host = "192.168.43.209";

HTTPClient http;

int sensorPin  =  32;    // select the input pin for the potentiometer, with WiFi connection 12-13-14 pins don't work
int value =  0;          // sensor value
int httpCode = 0;
int timeout = 0;         // sensor timeout, default value
int new_value = 0;

const int id=1;                         // write here the sensor id you created
const String key = "zgwTfwByxfbCZaZ";   // write here the key you receive via e-mail

void setup(){  
  pinMode(LED,OUTPUT);
  Serial.begin(9600);
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi..");
  while(WiFi.status() != WL_CONNECTED){  //blink until connection
    digitalWrite(LED, HIGH);
    delay(50);
    digitalWrite(LED, LOW);
    delay(150);
  }
  Serial.println("Connected to "+(String)ssid+" WiFi");
  Serial.println(WiFi.localIP());
  http.begin("http://"+(String)host+":"+(String)port+"/Noise_Pollution/send_data/"+(String)id+"/");
  httpCode = http.GET();
  if (httpCode>0){ 
    timeout = (http.getString()).toInt();  
    Serial.println(httpCode);
    Serial.println(timeout);
  }
  else{
    Serial.println("Error");
  }
  http.end();
}

void loop(){
  value =  digitalRead(sensorPin);
  http.begin("http://"+(String)host+":"+(String)port+"/Noise_Pollution/send_data/"+(String)id+"/");
  Serial.println(value,  DEC);
  digitalWrite(LED,  LOW);
  if (value==1){
    digitalWrite(LED,  HIGH);
  } 
  delay(timeout*1000);
  http.addHeader("Content-Type", "application/json");
  http.POST("{\"value\": \""+(String)value+"\",\"key\":\""+key+"\"}");
  httpCode = http.GET();
  new_value = (http.getString()).toInt();
  if (httpCode>0 & timeout!=new_value){
    timeout = new_value;
    Serial.println("Collection time modified:");
    Serial.println(timeout);
  }
  http.end();
}

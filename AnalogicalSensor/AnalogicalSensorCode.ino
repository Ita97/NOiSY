#include <WiFi.h>
#include <HTTPClient.h>
#include <math.h>
#define LED 2

//code to modify
const char ssid[] = "HUAWEI P20 Pro";//"Vodafone-3711713";
const char password[] = "AcC&Ss0.";//"AccessoWeb";

const char * host = "192.168.43.209";
const uint16_t port = 8000;

const int sensorPin  =  32;             // select the input pin for the potentiometer, with WiFi connection 12-13-14 pins don't work
const int id=2;                         // write here the sensor id you created
const String key = "QlTmxo57SSwngj7";   // write here the key you received via e-mail

// insert here the data you obtained from ConfigSensor and from a sound level meter
const int offset= 25;                   // decibell from slm
const float testValue = 496;            // value from sensor obtained from ConfigSensor

//code not to touch
HTTPClient http;

float sensorValue =  0;   
float db=0;

int httpCode = 0;
int timeout = 0;         // sensor timeout, default value
int new_value = 0;

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
  sensorValue =  analogRead(sensorPin);
  db = 230*log10(sensorValue/testValue)+offset;
  Serial.println(sensorValue,  DEC);
  Serial.println(db,  DEC);
  
  http.begin("http://"+(String)host+":"+(String)port+"/Noise_Pollution/send_data/"+(String)id+"/");
  digitalWrite(LED,  LOW);
  if (db>70){
    digitalWrite(LED,  HIGH);
  } 
  delay(timeout*1000);
  
  http.addHeader("Content-Type", "application/json");
  http.POST("{\"value\": \""+(String)db+"\",\"key\":\""+key+"\"}");
  
  httpCode = http.GET();
  new_value = (http.getString()).toInt();
  if (httpCode>0 & timeout!=new_value){
    timeout = new_value;
    Serial.println("Collection time is modified:");
    Serial.println(timeout);
  }
  http.end();
}

  

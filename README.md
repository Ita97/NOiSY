# Noise Pollution Detector
### Description

Based on Django Framework and Arduino Code.
This application web can manage rumor sensors and rooms and its purpose is to prevent noise pollution.

Using an ESP32 the sensors send info to the app, you can check in real-time the noise in every rooms with a sensor inside.
You can also check the history of your sensors in a day or an entire week. 
Plus you can virtually manage all your sensors: move, delete it or also change in real-time the data acquisition rate.
Same story for the rooms.

The app is programmed to send an email to a 'rep' of the room when the threshold of 70dB is passed, 
for comunicate that you are in a noise polluted area and to speak slowly for your health.

This application is a must for offices or labs where the work is difficoult with high noises, but also for an health home life.

The security is garanted by Django protocols, and an internal simple authorization method is developed.


### Configuration and Calibration Analogical Sensor

Firstly you have to setup the arduino code before install it in your ESP32.
Go to ***Manage Sensors*** and create a new sensor, remember to create a room before it.
A mail will send to you with the id and a key of the sensor.

Then you have to calibrate it.
The sensor we used was not very accurate, and we use an SPL meter to configure it.
Install the ConfigCode in the ESP32 and find the value of the sensor, better if you twist the potentiometer until the values reach 400, 
and then check the decibel on your SPL meter (a free app on your phone is fine).
Write down this two value on the AnalogicalSensorCode with the id and the key received by mail.
Now you can install it and check the value you obtain in decibel.

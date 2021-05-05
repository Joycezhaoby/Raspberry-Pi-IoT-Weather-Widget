# Raspberry Pi IoT Weather Widget
###### ECE 4180 Final Project - by Luca DeCicco, Jinghong Peng, Bingyue Zhao
###### Georgia Institute of Technology

## Overview
This project aims to develop an IoT weather widget on Raspberry Pi 4 and set up a GUI for users to interact with. The weather information will be extracted from the internet and update every minute. Users can change the city and the temperature threshold setting through the GUI, and once the temperature drops below that threshold, Pi will send out an email notification through AWS to inform the users. A sonar sensor detects whether a user is standing in front of the display or not. If a user is present, the screen will be on and show weather information; if a user is absent, the display will show a lock screen with the current time. Weather information will also be announced through a PCB-mount speaker when the display wakes up everytime or when the trigger event occurs while the display is on. The RGB LED will light up with specific colors depending on the weather status.

<p align="center">
<img src="docs and code development/flowchart2_1.png" width="50%" height="50%"/>
</p>

#### [Demo Video](https://youtu.be/iJoPHu5lioU)
#### [Presentation](https://youtu.be/49yFB9mnRGA)
## Hardware
Hardware and parts used in the project:
* Raspberry Pi 4 Model B:
  * Micro HDMI cable and monitor\*  
* Distance sensor:
  * Ultrasonic distance sensor HC-SR04
  * Voltage divider resistors: 330 Ω and 510 Ω
* Audio output:
  * Mono audio amp breakout TPA2005D1
  * PCB-mount speaker 8ohm 0.1W
  * Gain resistors：2x 100 kΩ
* LED display:
  * LED - RGB clear common cathode
  * Dropping resistors: 3x 330Ω

Detailed info about each hardware

Pinout and connection

### Ultrasonic Sensor
### Speaker

## Software Development
written in python
### AWS
description of the setup and functionality of AWS. Reference to the Corresponding py file. brief descriptions for SDK/packages/modules used. Feel free to break into smaller sections
### Weather API
### GUI Display
description of the setup and functionality of AWS. Reference to the Corresponding py file. brief descriptions for SDK/packages/modules used. Feel free to break into smaller sections

## Setup and Installation
Initial Pi setup

terminal command for installing modules/packages

## TroubleShooting
possible troubles when setting up the project and how to fix them
## Reflection
what to improve. Thought on future work
## Resources
reference on external resources

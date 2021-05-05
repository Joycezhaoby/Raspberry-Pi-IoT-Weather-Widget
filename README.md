# Raspberry Pi IoT Weather Widget
###### ECE 4180 Final Project - by Luca DeCicco, Jinghong Peng, Bingyue Zhao

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

_\*HDMI connection is optional if a virtual desktop is set up for pi_

Detailed info about each hardware
Pinout and connection

### Distance Sensor
| Sonar Sensor  |  |
| ------------- | ------------- |
| Vcc  | 5V  |
| Trig  | GPIO 24  |
| Echo | GPIO 23\* |
| Gnd | Gnd |

_**\*The GPIO pins on pi are only 3.3V tolerant so a voltage divider is required to drop the voltage from 5V to 3.3V. Refer to the picture below.**_

<p align="center">
<img src="docs and code development/sonar_connection.png" width="50%" height="50%"/>
</p>

### Audio Output
### LED Display

## Software Development
written in python
### AWS
description of the setup and functionality of AWS. Reference to the Corresponding py file. brief descriptions for SDK/packages/modules used. Feel free to break into smaller sections
### Weather API
The application retrieve real-time weather information from openweather.com https://openweathermap.org/api

API key is stored in config.ini file

### GUI Display
GUI display is developed with Python tkinter package

#### **Lock screen**:

When user is not nearby, the screen will only show current time and date.

#### **Weather GUI**:

When user is nearby, the screen will display weather GUI.

User can search weather information by entering city name and select a threshold temperature below which user will receive email alert. User have to input both city name and threshold temperature, or there will be an error. After entering information in the input box, user can search by clicking the green search button.

Information displayed on the GUI includes: City name and its Country, weather, weather icon, temperature in both Celcius and Fahrenheit.

The weather information is updated every minute when a user is nearby.

## Setup and Installation
Initial Pi setup

### Installation:

### Step1: Install Python3 and pip on your computer
  
  Python3: https://www.python.org/downloads/
  
  pip: https://pip.pypa.io/en/stable/installing/
 
### Step2: Install packages in the terminal

  tkinter: *pip install tk*
  
  configparser: *pip install configparser*
  
  PIL: *pip install pillow*
  
  gpiozero: *sudo apt install python3-gpiozero*
  
  time: *pip install times*

## TroubleShooting
possible troubles when setting up the project and how to fix them
## Reflection
what to improve. Thought on future work
## Resources
reference on external resources

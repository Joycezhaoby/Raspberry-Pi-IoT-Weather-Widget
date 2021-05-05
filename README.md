# Raspberry Pi IoT Weather Widget
###### 4180 Final Project - Luca DeCicco, Jinghong Peng, Bingyue Zhao

## Overview
Lorem ipsum dolor sit amet, sit unum reque an, mea nonumy deserunt perpetua an, elitr everti oblique in vim. Sed ei harum eloquentiam. Nostro persecuti interpretaris vix te, eum habeo partem eu. Case nostrud qualisque ad eos, vel brute possim evertitur ut.Lorem ipsum dolor sit amet, sit unum reque an, mea nonumy deserunt perpetua an, elitr everti oblique in vim. Sed ei harum eloquentiam. Nostro persecuti interpretaris vix te, eum habeo partem eu. Case nostrud qualisque ad eos, vel brute possim evertitur ut.
#### Demo Video
<p align="center">
<img src="docs and code development/flowchart2_1.png" width="75%" height="75%"/>
</p>

## Hardware
list hardware used in the project here

Detailed info about each hardware

Pinout and connection

### Ultrasonic Sensor
### Speaker

## Software Development
written in python
### AWS
description of the setup and functionality of AWS. Reference to the Corresponding py file. brief descriptions for SDK/packages/modules used. Feel free to break into smaller sections
### Weather API
The application retrieve real-time weather information from openweather.com https://openweathermap.org/api

API key is stored in config.ini file

### GUI Display
GUI display is developed with Python tkinter package

Lock screen:

When user is not nearby, the screen will only show current time and date.

Weather GUI:

When user is nearby, the screen will display weather GUI.

User can search weather information by entering city name and select a threshold temperature below which user will receive email alert. User have to input both city name and threshold temperature, or there will be an error. After entering information in the input box, user can search by clicking the green search button.

Information displayed on the GUI includes: City name and its Country, weather, weather icon, temperature in both Celcius and Fahrenheit.

The weather information is updated every minute when a user is nearby.

## Setup and Installation
Initial Pi setup

Installation:

Step1: Install Python3 and pip on your computer
  
  Python3: https://www.python.org/downloads/
  
  pip: https://pip.pypa.io/en/stable/installing/
 
Step2: Install packages in the terminal

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

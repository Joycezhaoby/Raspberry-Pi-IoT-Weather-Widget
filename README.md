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
* **Raspberry Pi 4 Model B:**
  * Micro HDMI cable and monitor\*  
* **Distance sensor:**
  * Ultrasonic distance sensor HC-SR04
  * Voltage divider resistors: 330 Ω and 510 Ω
* **Audio output:**
  * Mono audio amp breakout TPA2005D1
  * PCB-mount speaker 8ohm 0.1W
  * Gain resistors：2x 100 kΩ
* **LED display:**
  * LED - RGB clear common cathode
  * Dropping resistors: 3x 330Ω

_\*HDMI connection is optional if a virtual desktop is set up for pi_
### Distance Sensor
| Sonar Sensor  |  |
| -------- | -------- |
| Vcc  | 5V  |
| Trig  | GPIO 24  |
| Echo | GPIO 23\* |
| Gnd | Gnd |

_**\*The GPIO pins on Pi are only 3.3V tolerant so a voltage divider is required to drop the voltage from 5V to 3.3V.**_ Connect the 330 Ω resistor to Echo and the 510 Ω resistor in series from 330 Ω to gnd. Then connect the junction to pin 16 (GPIO 23). Refer to the picture below.

<p align="left">
<img src="docs and code development/sonar_connection.png" width="50%" height="50%"/>
</p>

Using the GPIO Zero library makes it easy to control GPIO devices on Pi with Python, and HC-SR04 can be represented by the DistanceSensor class: 
```
gpiozero.DistanceSensor(echo, trigger, max_distance=1, threshold_distance=0.3)
```
The parameter `threshold_distance` sets the distance in meter which will trigger the `in_range` and `out_of_range` events when crossed. Functions can be attachted to the events to run when the device changes states between active and inactive.

### Audio Output
| Audio Amp  |   |
| ------ | ------ |
| PWR+ | 5V  | 
| PWR- | Gnd |
| IN+ | GPIO 12 |
| IN- | Gnd |
| OUT+ | **Speaker** + |
| OUT- | **Speaker** - |

Raspberry Pi has two PWM channels and each channel has two output pins:
* PWM0: GPIO 12 and GPIO 18
* PWM1: GPIO 13 and GPIO 19

The Pi has three audio output modes: HDMI 1 and 2, and a headphone jack which uses PWM. The Pi needs to be configured to reroute the audio output to GPIO PWM pins.
1. Select headphone jack as the output option
     - Open the terminal and type in command `sudo raspi-config`
     - Select **System Options** > **Audio**, then select **Headphones**. Please note that the order and arrangment might be different for different models.
2. Use Device Tree Overlay to assign audio outputs
     - Open and edit config.txt file
       - `cd /boot`
       - `sudo nano config.txt`
     - under the `# Enable audio` section, add the following code
       ```
       dtparam=audio=on
       audio_pwm_mode=2
       dtoverlay=audremap,pins_12_13
       ```
     - Write to the file and quit
     - Reboot Pi for the changes to take effect


### LED Display

## Software Development
written in python
### AWS
description of the setup and functionality of AWS. Reference to the Corresponding py file. brief descriptions for SDK/packages/modules used. Feel free to break into smaller sections
### Weather API
- The application retrieve real-time weather information from [OpenWeather](https://openweathermap.org/api)

- API key is stored in config.ini file

### GUI Display
GUI display is developed with Python tkinter package

#### **Lock screen**:

- When user is not nearby, the screen will only show current time and date.

<p align="left">
<img src="docs and code development/lock.png" width="50%" height="50%"/>
</p>

#### **Weather GUI**:

<p align="left">
<img src="docs and code development/input.png" width="50%" height="50%"/>
</p>

- When user is nearby, the screen will display weather GUI.

- User can search weather information by entering city name and select a threshold temperature below which user will receive email alert. User have to input both city name and threshold temperature, or there will be an error. After entering information in the input box, user can search by clicking the green search button.

- Information displayed on the GUI includes: City name and its Country, weather, weather icon, temperature in both Celcius and Fahrenheit.

- The weather information is updated every minute when a user is nearby.

<p align="left">
<img src="docs and code development/weather.png" width="50%" height="50%"/>
</p>

## Setup and Installation
Initial Pi setup

### Installation:

### Step1: Install Python3 and pip on your computer
  
- Python3: https://www.python.org/downloads/
  
- pip: https://pip.pypa.io/en/stable/installing/
 
### Step2: Install packages in the terminal


  tkinter: `pip install tk`
  
  configparser: `pip install configparser`
  
  PIL: `pip install pillow`
  
  gpiozero: GPIO Zero is installed by default in the Raspberry Pi OS desktop image. If in case reinstallation is needed, run the following commands.
  ```
  sudo apt update
  sudo apt install python3-gpiozero
  ```
  
  time: `pip install times`


## TroubleShooting
possible troubles when setting up the project and how to fix them
## Reflection
what to improve. Thought on future work
## Resources
[GPIO Zero Library](https://gpiozero.readthedocs.io/)


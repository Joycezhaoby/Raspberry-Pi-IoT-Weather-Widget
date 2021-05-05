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
class gpiozero.DistanceSensor(echo, trigger, max_distance=1, threshold_distance=0.3)
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

<p align="left">
<img src="docs and code development/speaker_connection.png" width="50%" height="50%"/>
</p>

#### GPIO Setup
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

Now that the audio GPIO output is set up. The GPIO pins' current functions can be checked via `gpio readall` and all possible functions can be looked up on the [datasheet](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bcm2711/rpi_DATA_2711_1p0_preliminary.pdf). With the audio amp and speaker wired up, now all system sounds can be played through the speaker. 

#### Volumn Adjustment
There are several ways to adjust the output volumn through the speaker if it is too soft/loud.
1. Adjust the system sound output level from the GUI or `alsamixer` in the terminal.
2. Add resistors to the audio amp to adjust the gain.
     - In this project, the audio output is not loud enough so gain resistors are added to the amplifier. There are two identical resistors, indicated in the white rectangles on the amplifier board, that set the gain of the board. Two additional resistors can be added in parallel to reduce the resistor value. 100 kΩ resistors are added (shown below) to boost the gain from 2 to 3. For more detailed information and restrictions, please consult the datasheet and this [guide](https://www.sparkfun.com/tutorials/392).

<p align="left">
<img src="docs and code development/audio amp.png" width="20%" height="20%"/>
</p>

### LED Display
| RGB LED  |   |
| ------ | ------ |
| R | GPIO 17  | 
| Gnd (longest) | Gnd |
| G | GPIO 27 |
| B | GPIO 22 |

Please note that **dropping resistors** need to be connected in ***series*** to limit the voltage drop across the LEDs.

<p align="left">
<img src="docs and code development/led_connection.png" width="50%" height="50%"/>
</p>

The RGBLED class in GPIO Zero library is used to set up the weather LED patterns. Functions `blink` and `pulse` make the device turn on and off or fade in and out repeatedly.
```
classgpiozero.RGBLED(red, green, blue)
blink(on_time=1, off_time=1, fade_in_time=0, fade_out_time=0, on_color=(1, 1, 1), off_color=(0, 0, 0), n=None, background=True)
pulse(fade_in_time=1, fade_out_time=1, on_color=(1, 1, 1), off_color=(0, 0, 0), n=None, background=True)
```
The parameter `background` is set to `True` (the default) to start a background thread to continue blinking/pulsing and return immediately so that the program will not halt. 9 LED lighting patterns are designed and assigned to distinct weathers, and the [demo program](LEDdemo.py) shows all the effects at once. 

## Software Development
The application is written in Python.

### AWS

AWS is used to send an email notification to the user is a certain threshold has been met. It uses the AWSIotMQTT Client to send messages to an AWS account that is configured to send those messages to a given endpoint (which in this case is an email address)

### Weather API
The application retrieves real-time weather information from [OpenWeather](https://openweathermap.org/api) which provides a free weather API for the public. Create an account and subscribe the _Current Weather Data_ API.

Obtained API key is stored in config.ini file.

### GUI Display
GUI display is developed with Python tkinter package.

#### Lock screen:

- When a user is not nearby, the sonar is inactive and the `out_of_range` event is set. The screen will only show current time and date.

<p align="left">
<img src="docs and code development/lock.png" width="50%" height="50%"/>
</p>

#### Weather Display:

<p align="left">
<img src="docs and code development/input.png" width="50%" height="50%"/>
</p>

- When a user is nearby, the sonar is active and the `in_range` event is set. The screen will display weather.

- Users can search weather information by entering city name and select a threshold temperature below which user will receive an email alert. Users will have to input both city name and threshold temperature, or there will be an error message. Users will also receive an error message if the city name is invalid. After entering information in the input box, user can search by clicking the green search button.

- Information displayed on the GUI includes: City name and Country, weather, weather icon, temperature in both Celcius and Fahrenheit.

- The weather information is updated every minute in the background by using tkinter `after()` callback function. When the `update_GUI()` function is called, new weather information is fetched from OpenWeather, and is compared to the trigger value. The LED and GUI display is updated along with weather information, and the previous callback handle will be canceled to prevent accidental accumulations of the callback function. 

<p align="left">
<img src="docs and code development/weather.png" width="50%" height="50%"/>
</p>

### Text-to-Speech
A TTS engine is needed to announce the weather through the speaker. **eSpeak** provides offline text-to-speech conversions with easy access. Developed code is included in [notification.py](notification.py).

## Setup and Installation

### Installation:

### Step 1: Install Python3 and pip on your computer
  
- Python3: https://www.python.org/downloads/
  
- pip: https://pip.pypa.io/en/stable/installing/
 
### Step 2: Install packages in the terminal

  tkinter: `pip3 install tk`
  
  configparser: `pip3 install configparser`
  
  PIL: `pip3 install pillow`
  
  time: `pip3 install times`
  
  requests: `pip3 install requests`
  
  datetime: `pip3 install DateTime`
  
  num2words: `pip3 install num2words`
  
  gpiozero: GPIO Zero is installed by default in the Raspberry Pi OS desktop image. If in case reinstallation is needed, run the following commands.
  ```
  sudo apt update
  sudo apt install python3-gpiozero
  ```
  
  eSpeak:
  ```
  sudo apt-get update
  sudo apt-get install espeak
  ```


### Step 3: Set Up AWS

1) Navigate to [AWS](https://aws.amazon.com) and create an account
2) [Create an IoT Thing](https://docs.aws.amazon.com/iot/latest/developerguide/iot-moisture-create-thing.html) and its relevant certificate files. Download these files to the Raspberry Pi
3) Create an IoT [Rule](https://docs.aws.amazon.com/iot/latest/developerguide/iot-moisture-create-rule.html) that sends messages recieved from the Raspberry Pi as an SNS push notification
4) Create the [SNS Topic and Subscription](https://docs.aws.amazon.com/iot/latest/developerguide/iot-moisture-create-sns-topic.html) that will send these SNS pushes to a given email address
5) AWS should now be configured correctly. On the Rapsberry Pi side, follow [these instructions](https://docs.aws.amazon.com/iot/latest/developerguide/connecting-to-existing-device.html) to download the necessary packages that are required to connect the Pi to AWS
6) Configure the AWS connection with the medthod used in the file awsconnect.py
 - the "payload1" variable defines the topic the Pi will publish to. This topic will also be the same one selected in step 3 to send as an SNS push
 - "certPath" defines the folder in which you placed the certificate files in step 2. These files will be used to connect to the AWS server

## Possible Future Improvements

* Provide more options for trigger settings (e.g. specific weather conditions, high temperature threshold, etc.)
* Include a secondary display device
* Select alternative audio output devices

## Resources

[Raspberry Pi 4B Datasheet](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bcm2711/rpi_DATA_2711_1p0_preliminary.pdf)

[GPIO Zero Library](https://gpiozero.readthedocs.io/)

[Open Weather Map API](https://openweathermap.org/api)

[Mono Audio Amp Guide](https://www.sparkfun.com/tutorials/392)

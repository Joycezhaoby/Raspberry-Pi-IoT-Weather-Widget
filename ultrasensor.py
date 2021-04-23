from gpiozero import DistanceSensor
from time import sleep

# pin16-GPIO23, pin18-GPIO24, voltage divider required for echo
sensor = DistanceSensor(echo=23, trigger=24, max_distance=3)
sensor.threshold_distance = 0.5 #set trigger threshold

screen_on = 0

def user_absent():
    global screen_on
    print("user absent")
    screen_on = 0
    #lock screen commands

def user_present():
    global screen_on
    print("user present")
    screen_on = 1
    #active screen

def main():
    sensor.when_out_of_range = user_absent
    sensor.when_in_range = user_present

main()

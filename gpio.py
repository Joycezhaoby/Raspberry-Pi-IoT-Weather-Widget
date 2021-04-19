from gpiozero import DistanceSensor
# import RPi.GPIO
from time import sleep

# pin16 - GPIO23, pin18 - GPIO24
sensor = DistanceSensor(23, 24) #(echo, trig)

while True:
    print('Distance to nearest object is', sensor.distance, 'm')
    sleep(1)
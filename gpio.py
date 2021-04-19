from gpiozero import DistanceSensor
from time import sleep

# pin16-GPIO23, pin18-GPIO24, voltage divider required for echo
sensor = DistanceSensor(echo=23, trigger=24, max_distance=3)
sensor.threshold_distance = 0.5


while True:
    print('Distance to nearest object is', sensor.distance, 'm')
    sleep(1)
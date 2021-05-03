from gpiozero import RGBLED
from time import sleep

# pin11-GPIO 17, pin13-GPIO 27, pin15-GPIO 22
led = RGBLED(red=17, green=27, blue=22)

def weather_color(weather_id):
    if 200 <= weather_id < 300: #thunderstorm
        led.blink(on_time=0.1, off_time=0.1, fade_in_time=0, fade_out_time=0,
                  on_color=(1, 1, 1), off_color=(0, 0, 0), n=None, background=True)
    elif 300 <= weather_id <400: #drizzle
        led.pulse(fade_in_time=0.5, fade_out_time=0.5, on_color=(0,0,1),
                  off_color=(0, 0, 0), n=None, background=True)
    elif 500 <= weather_id <600: #rain
        led.pulse(fade_in_time=0.15, fade_out_time=0.15, on_color=(0,0,1),
                  off_color=(0, 0, 0), n=None, background=True)
    elif 600 <= weather_id <700: #snow
        led.blink(on_time=1, off_time=1, fade_in_time=0.2, fade_out_time=0.2,
                  on_color=(0.1, 0.1, 1), off_color=(0.7, 0.7, 1), n=None, background=True)
    elif (700<=weather_id<720) or (weather_id==741): #white atmosphere - fog, mist, smoke
        led.blink(on_time=1, off_time=1, fade_in_time=0.2, fade_out_time=0.2,
                  on_color=(1, 0.6, 0.1), off_color=(0.3, 0.1, 0), n=None, background=True)
    elif (720<=weather_id<740) or (750<=weather_id<770): #yellow atmosphere - sand, dust, haze, ash
        led.blink(on_time=0.5, off_time=0.5, fade_in_time=0.2, fade_out_time=0.2,
                  on_color=(1, 0.3, 0), off_color=(0.3, 0.1, 0), n=None, background=True)
    elif 770 <= weather_id <800: #tornado, squall
        led.blink(on_time=0.3, off_time=0.3, fade_in_time=0.2, fade_out_time=0.2,
                  on_color=(1, 0, 0), off_color=(0.3, 0.1, 0), n=None, background=True)
    elif 801 <= weather_id <810: #clouds
        led.blink(on_time=1, off_time=1, fade_in_time=0.2, fade_out_time=0.2,
                  on_color=(1, 1, 1), off_color=(0.5, 0.5, 0.5), n=None, background=True)
    elif weather_id == 800: #clear
        led.blink(on_time=1, off_time=1, fade_in_time=0.2, fade_out_time=0.2,
                  on_color=(0.4, 1, 0.4), off_color=(0.1, 0.8, 0.1), n=None, background=True)
    elif weather_id == 0: #off
        led.off()
    else:
        led.off()
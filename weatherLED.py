from gpiozero import RGBLED
from time import sleep

# pin15-GPIO 22, pin13-GPIO 27, pin11-GPIO 17
led = RGBLED(red=22, green=27, blue=17)

def weather_color(weather_id):
    if 200 <= weather_id < 300:
        print('thunderstorm')
        led.blink(on_time=0.1, off_time=0.1, fade_in_time=0, fade_out_time=0,
                  on_color=(1, 1, 1), off_color=(0, 0, 0), n=None, background=True)
    elif 300 <= weather_id <400:
        print('drizzle')
        led.pulse(fade_in_time=0.5, fade_out_time=0.5, on_color=(0,0,1),
                  off_color=(0, 0, 0), n=None, background=True)
    elif 500 <= weather_id <600:
        print('rain')
        led.pulse(fade_in_time=0.15, fade_out_time=0.15, on_color=(0,0,1),
                  off_color=(0, 0, 0), n=None, background=True)
    elif 600 <= weather_id <700:
        print('snow')
        led.blink(on_time=1, off_time=1, fade_in_time=0.2, fade_out_time=0.2,
                  on_color=(0.1, 0.1, 1), off_color=(0.7, 0.7, 1), n=None, background=True)
    elif (700<=weather_id<720) or (weather_id==741):
        print('atmosphere white')
        led.blink(on_time=1, off_time=1, fade_in_time=0.2, fade_out_time=0.2,
                  on_color=(1, 0.6, 0.1), off_color=(0.3, 0.1, 0), n=None, background=True)
    elif (720<=weather_id<740) or (750<=weather_id<770):
        print('atmosphere yellow')
        led.blink(on_time=0.5, off_time=0.5, fade_in_time=0.2, fade_out_time=0.2,
                  on_color=(1, 0.3, 0), off_color=(0.3, 0.1, 0), n=None, background=True)
    elif 770 <= weather_id <800:
        print('atmosphere red')
        led.blink(on_time=0.3, off_time=0.3, fade_in_time=0.2, fade_out_time=0.2,
                  on_color=(1, 0, 0), off_color=(0.3, 0.1, 0), n=None, background=True)
    elif 801 <= weather_id <810:
        print('clouds')
        led.blink(on_time=1, off_time=1, fade_in_time=0.2, fade_out_time=0.2,
                  on_color=(1, 1, 1), off_color=(0.5, 0.5, 0.5), n=None, background=True)
    elif weather_id == 800:
        print('clear')
        led.blink(on_time=1, off_time=1, fade_in_time=0.2, fade_out_time=0.2,
                  on_color=(0.4, 1, 0.4), off_color=(0.1, 0.8, 0.1), n=None, background=True)
    elif weather_id == 0:
        led.off()
    else:
        led.off()
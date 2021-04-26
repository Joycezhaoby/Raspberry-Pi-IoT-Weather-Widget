from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
from PIL import ImageTk, Image
import requests

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
    update_GUI()
    #lock screen commands

def user_present():
    global screen_on
    print("user present")
    screen_on = 1
    update_GUI()
    #active screen

def main():
    sensor.when_out_of_range = user_absent
    sensor.when_in_range = user_present

# Set up OpenWeather API
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_cel = temp_kelvin - 273.15
        temp_fahr = (temp_kelvin - 273.15) * 9 / 5 + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        final = (city, country, temp_cel, temp_fahr, icon, weather)
        return final
    else:
        return None

def change_setting():
    global city
    city = city_text.get()
    update_GUI()

def update_GUI():
    weather = get_weather(city)
    if screen_on:
        display_weather(weather)
    else:
        lock_screen()
    temp_label.after(60000,update_GUI)


def display_weather(weather):
    global img
    if weather:
        location_label['text'] = '{}, {}'.format(weather[0], weather[1])
        imgpath = "weather_icons/{}.png".format(weather[4])
        img = Image.open(imgpath)
        img = ImageTk.PhotoImage(img)
        imagel['image'] = img
        temp_label['text'] = '{:.2f}°C, {:.2f}°F'.format(weather[2], weather[3])
        weather_label['text'] = weather[5]
    else:
        messagebox.showerror('Error', 'Cannot find city')
        change_setting()
    app.update()

def lock_screen():
    #something in here
    #display system time in super large font
    print('display lock screen')
    location_label['text'] = ''
    imagel['image'] = ''
    temp_label['text'] = ''
    weather_label['text'] = ''
    app.update()

# Create object and set up default screen size
app = Tk()
app.title("Weather GUI")
app.config(bg="white")
app.attributes("-fullscreen", True)
app.bind("<F11>", lambda event: app.attributes("-fullscreen", not app.attributes("-fullscreen")))
app.bind("<Escape>", lambda event: app.attributes("-fullscreen", False))
app.geometry('700x350')

# ----------
city = ''
city_text = StringVar()
city_entry = Entry(app, textvariable = city_text)
city_entry.pack(expand=True)
# ------------
search_button = Button(app, text = 'Search Weather', width = 12, command = change_setting,bg="white")
search_button.pack()
# ------------
location_label = Label(app, text = '', font = ('bold', 20),bg="white")
location_label.pack()
# --------------
img = Image.open("weather_icons/02d.png")
#img = img.resize((150,150))
img = ImageTk.PhotoImage(img)
imagel = Label(app, image = '',bg="white")
imagel.pack()
# -----------------
temp_label = Label(app, text = '',bg="white")
temp_label.pack()
# -----------------
weather_label = Label(app, text = '',bg="white")
weather_label.pack(expand=True)

main()
#screen_on = True
app.mainloop()

from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
from PIL import ImageTk, Image
import requests
import datetime
from gpiozero import DistanceSensor
from time import sleep

import notification
import weatherLED


# pin16-GPIO23, pin18-GPIO24, voltage divider required for echo
sensor = DistanceSensor(echo=23, trigger=24, max_distance=3)
sensor.threshold_distance = 0.5 #set trigger threshold

screen_on = 1
weather = ''
timer_id = ''

def user_absent():
    global screen_on
    screen_on = 0
    print("user absent")
    lock_screen()

def user_present():
    global screen_on
    screen_on = 1
    print("user present")
    display_weather(True)

def main():
    sensor.when_out_of_range = user_absent
    sensor.when_in_range = user_present

# Set up OpenWeather API
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


def get_weather():
    global weather
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        cityname = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_cel = temp_kelvin - 273.15
        temp_fahr = (temp_kelvin - 273.15) * 9 / 5 + 32
        icon = json['weather'][0]['icon']
        weather_main = json['weather'][0]['main']
        weather_id = json['weather'][0]['id']
        weather = (cityname, country, temp_cel, temp_fahr, icon, weather_main, weather_id)
        return weather
    else:
        messagebox.showerror('Error', 'Cannot find city')
        return None

def change_setting():
    global city
    global thres_temp
    city = city_text.get()
    thres_temp = Threshold.get()
    if city and thres_temp:
        update_GUI(False)
        
first_trigger = 1

def compare_temp():
    global first_trigger
    trigger = float('{}'.format(weather[3])) <= float(thres_temp)
    if not trigger:
        first_trigger = 1
    else:
        if first_trigger == 1:
            first_trigger = 0
            notification.notify(thres_temp,weather,screen_on)
    print (trigger)

    

def update_GUI(first_time):
    global timer_id
    get_weather()
    compare_temp()
    weatherLED.weather_color(weather[6])
    print(weather[6])
    if screen_on:
        display_weather(first_time)
    else:
        lock_screen()
    if timer_id: temp_label.after_cancel(timer_id)
    timer_id = temp_label.after(60000,update_GUI,False)


def display_weather(first_time):
    global img
    if weather:
        location_label['text'] = '{}, {}'.format(weather[0], weather[1])
        imgpath = "weather_icons/{}.png".format(weather[4])
        img = Image.open(imgpath)
        img = ImageTk.PhotoImage(img)
        imagel['image'] = img
        temp_label['text'] = '{:.2f}°C, {:.2f}°F'.format(weather[2], weather[3])
        weather_label['text'] = weather[5]
        if first_time:
            noti_text = 'The weather in {}, {} is {}'.format(weather[0], weather[1],weather[5])
            notification.speak(noti_text)
    app.update()

def lock_screen():
    now = datetime.datetime.now()
    print ("Current date and time : ")
    print (now.strftime("%Y-%m-%d %H:%M"))
    #something in here
    #display system time in super large font
    print('display lock screen')
    location_label['text'] = now.strftime("%Y-%m-%d %H:%M")
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
city_entry.place(x = 260, y = 30)
# ------------\
thres_temp = ''
Threshold = StringVar()
Thres_entry = Entry(app, textvariable = Threshold).place(x = 260, y = 60)
# ------------
user_name = Label(app, text = "City Name", bg="white").place(x = 150,y = 30) 
user_password = Label(app, text = "Get alert when tempature is below", bg="white").place(x = 20,y = 60) 
degree = Label(app, text = "°F", bg="white").place(x = 450, y = 60)
# ------------
button_img = PhotoImage(file = "weather_icons/button_new.png")
search_button = Button(app, image = button_img, width = 50, height = 50,command = change_setting,bg="white")
search_button.place(x = 480, y = 32)
# ------------
location_label = Label(app, text = '', font = ('bold', 20),bg="white")
location_label.place(x = 275, y = 110)
# --------------
img = Image.open("weather_icons/02d.png")
#img = img.resize((150,150))
img = ImageTk.PhotoImage(img)
imagel = Label(app, image = '',bg="white")
imagel.place(x = 275, y = 160)#x = 275, y = 160, relheight=0.4, relx=0.5, rely=0.5
# -----------------
temp_label = Label(app, text = '',bg="white")
temp_label.place(x = 275, y = 250)
# -----------------
weather_label = Label(app, text = '',bg="white")
weather_label.place(x = 313, y = 280)

main()
#screen_on = True
app.mainloop()
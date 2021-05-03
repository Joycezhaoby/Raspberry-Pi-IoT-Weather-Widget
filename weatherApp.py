from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
from PIL import ImageTk, Image
from gpiozero import DistanceSensor
from time import sleep
import requests
import datetime
import notification
import weatherLED

# set up ultrasonic distance sensor
# pin16-GPIO23, pin18-GPIO24, voltage divider required for echo
sensor = DistanceSensor(echo=23, trigger=24, max_distance=3)
sensor.threshold_distance = 0.5 #set trigger threshold

# global variables
screen_on = 1
first_trigger = 1 # first time trigger occurs
city = ''
weather = ''
thres_temp = ''
timer_id = '' # callback function id

# sensor interrupt functions
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

def sensor_main():
    sensor.when_out_of_range = user_absent
    sensor.when_in_range = user_present

# set up OpenWeather API
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

# update weather with user city input
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

# change user city and trigger settings
def change_setting():
    global city
    global thres_temp
    city = city_text.get()
    thres_temp = Threshold.get()
    if city and thres_temp:
        update_GUI(False)

# compare temperature with threshold setting
def compare_temp():
    global first_trigger
    trigger = float('{}'.format(weather[3])) <= float(thres_temp)
    if not trigger:
        first_trigger = 1
    else:
        if first_trigger == 1:
            first_trigger = 0
            notification.notify(thres_temp,weather,screen_on)

# update GUI every minute with new weather information
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

# display weather
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

# display lock screen
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

# user input boxes
city_text = StringVar()
city_entry = Entry(app, textvariable = city_text)
city_entry.place(x = 260, y = 30)
Threshold = StringVar()
Thres_entry = Entry(app, textvariable = Threshold).place(x = 260, y = 60)
# user input text prompts
user_name = Label(app, text = "City Name", bg="white").place(x = 150,y = 30) 
user_password = Label(app, text = "Get alert when tempature is below", bg="white").place(x = 20,y = 60) 
degree = Label(app, text = "°F", bg="white").place(x = 450, y = 60)
# user setting search button
button_img = PhotoImage(file = "weather_icons/button_new.png")
search_button = Button(app, image = button_img, width = 50, height = 50,command = change_setting,bg="white")
search_button.place(x = 480, y = 32)
# location label
location_label = Label(app, text = '', font = ('bold', 20),bg="white")
location_label.place(x = 275, y = 110)
# weather icon
img = Image.open("weather_icons/02d.png")
img = ImageTk.PhotoImage(img)
imagel = Label(app, image = '',bg="white")
imagel.place(x = 275, y = 160)#x = 275, y = 160, relheight=0.4, relx=0.5, rely=0.5
# temperature label
temp_label = Label(app, text = '',bg="white")
temp_label.place(x = 275, y = 250)
# weather info label
weather_label = Label(app, text = '',bg="white")
weather_label.place(x = 313, y = 280)

sensor_main() # activate sensor interrupt functions
app.mainloop() # start GUI
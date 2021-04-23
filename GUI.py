from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests
from PIL import ImageTk, Image

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

app = Tk()
app.title("Weather app")
app.geometry('700x350')

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


def search():
	global img
	city = city_text.get()
	weather = get_weather(city)
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

city_text = StringVar()
city_entry = Entry(app, textvariable = city_text)
city_entry.pack()

search_button = Button(app, text = 'Search Weather', width = 12, command = search)
search_button.pack()

location_label = Label(app, text = '', font = ('bold', 20))
location_label.pack()

img = Image.open("weather_icons/02d.png")
#img = img.resize((150,150))
img = ImageTk.PhotoImage(img)

imagel = Label(app, image = '')
imagel.pack()

temp_label = Label(app, text = '')
temp_label.pack()

weather_label = Label(app, text = '')
weather_label.pack()
app.mainloop()
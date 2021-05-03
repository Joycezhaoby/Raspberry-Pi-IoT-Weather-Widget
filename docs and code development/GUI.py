from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests


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
	city = city_text.get()
	weather = get_weather(city)
	if weather:
		location_label['text'] = '{}, {}'.format(weather[0], weather[1])
		image['bitmap'] = 'weather_icons/{}.png'.format(weather[4])
		temp_label['text'] = '{:.2f}°C, {:.2f}°F'.format(weather[2], weather[3])
		weather_label['text'] = weather[5]
	else:
		messagebox.showerror('Error', 'Cannot find city')

city_text = StringVar()
city_entry = Entry(app, textvariable = city_text).place(x = 250, y = 30)


Threshold = StringVar()
Thres_entry = Entry(app, textvariable = Threshold).place(x = 250, y = 60)




user_name = Label(app, text = "City Name").place(x = 150,y = 30) 
user_password = Label(app, text = "Get alert when tempature is below").place(x = 35,y = 60) 
degree = Label(app, text = "°C").place(x = 440, y = 60)


search_button = Button(app, text = 'Search Weather', width = 10, command = search).place(x = 460, y = 30)

alert_button = Button(app, text = 'set alert', width = 10, command = search).place(x = 460, y = 60)

location_label = Label(app, text = '', font = ('bold', 20))
location_label.place(x = 275, y = 130)


image = Label(app, bitmap = '')
image.place(x = 275, y = 160)

temp_label = Label(app, text = '')
temp_label.place(x = 275, y = 250)

weather_label = Label(app, text = '')
weather_label.place(x = 313, y = 280)
app.mainloop()

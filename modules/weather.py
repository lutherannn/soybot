from math import floor
import requests
import os


def weather(*, message):
    url = (
        "http://api.openweathermap.org/data/2.5/weather?appid="
        + os.getenv("TEST")
        + "&q="
        + message
    )
    resp = requests.get(url)
    cont = resp.json()

    if cont["cod"] != "404":
        weatherData = cont["main"]
        temp = weatherData["temp"]
        temp = floor((temp - 273.15) * 1.8 + 32)
        return f"Temperature in {message.title()}: {str(temp)}"
    else:
        return "City not found, or openweathermap is down"

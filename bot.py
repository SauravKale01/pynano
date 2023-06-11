import requests
from telegram.ext import Updater, CommandHandler

TOKEN = "6169875332:AAHkcJvM2V7rB-CTKoi9RHp7hOlDy69RGW4"
API_KEY = "N3co0uwxaCuE0QG9KgwAaRL9vgor5MKe"

def start(update, context):
    message = "Welcome to the Weather Bot! Send /weather <city> to get the current weather conditions for a specific city."
    update.message.reply_text(message)

def help(update, context):
    message = "This bot provides current weather information for a specific city.\n\nUsage:\n/weather <city> - Get the weather for a specific city."
    update.message.reply_text(message)

def weather(update, context):
    city = context.args[0]
    url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={API_KEY}&q={city}"
    response = requests.get(url).json()
    
    if response and len(response) > 0:
        if 'Key' in response[0]:
            location_key = response[0]['Key']
            conditions_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}"
            conditions_response = requests.get(conditions_url).json()
            
            if conditions_response and len(conditions_response) > 0:
                try:
                    temperature = conditions_response[0]["Temperature"]["Metric"]["Value"]
                    weather_text = conditions_response[0]["WeatherText"]
                    humidity = conditions_response[0].get("RelativeHumidity")
                    wind_speed = conditions_response[0]["Wind"]["Speed"]["Metric"]["Value"]
                    wind_direction = conditions_response[0]["Wind"]["Direction"]["Localized"]
                    
                    message = f"Weather in {city}:\n\nTemperature: {temperature}°C\nWeather: {weather_text}\nHumidity: {humidity}%\nWind Speed: {wind_speed} km/h\nWind Direction: {wind_direction}"
                    update.message.reply_text(message)
                except KeyError:
                    update.message.reply_text("Sorry, I couldn't retrieve the weather information for that location.")
            else:
                update.message.reply_text("Sorry, I couldn't retrieve the weather information for that location.")
        else:
            update.message.reply_text("Sorry, I couldn't find the specified location.")
    else:
        update.message.reply_text("Sorry, I couldn't find the specified location.")



def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("weather", weather))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

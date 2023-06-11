import requests
from telegram.ext import Updater, CommandHandler

# AccuWeather API key
API_KEY = "N3co0uwxaCuE0QG9KgwAaRL9vgor5MKe"

# Telegram bot token
TOKEN = "6169875332:AAHkcJvM2V7rB-CTKoi9RHp7hOlDy69RGW4"

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Weather Bot! Type /weather <city> to get the current weather.")

def weather(update, context):
    if len(context.args) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a city name.")
        return

    city = " ".join(context.args)

    # Get location key for the provided city
    location_url = f"http://dataservice.accuweather.com/locations/v1/search?q={city}&apikey={API_KEY}"
    location_response = requests.get(location_url).json()

    if len(location_response) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="City not found.")
        return

    location_key = location_response[0]["Key"]
    city_name = location_response[0]["LocalizedName"]
    country_name = location_response[0]["Country"]["LocalizedName"]

    # Get current conditions using the location key
    current_conditions_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}"
    conditions_response = requests.get(current_conditions_url).json()

    if len(conditions_response) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Could not fetch weather data.")
        return

    weather_text = conditions_response[0]["WeatherText"]
    temperature = conditions_response[0]["Temperature"]["Metric"]["Value"]
    humidity = conditions_response[0]["RelativeHumidity"]
    wind_speed = conditions_response[0]["Wind"]["Speed"]["Metric"]["Value"]
    wind_direction = conditions_response[0]["Wind"]["Direction"]["Localized"]

    weather_message = f"Weather in {city_name}, {country_name}:\n"
    weather_message += f"Condition: {weather_text}\n"
    weather_message += f"Temperature: {temperature}°C\n"
    weather_message += f"Humidity: {humidity}%\n"
    weather_message += f"Wind: {wind_speed} km/h, {wind_direction}"

    context.bot.send_message(chat_id=update.effective_chat.id, text=weather_message)

def random_fact(update, context):
    fact_url = "https://uselessfacts.jsph.pl/random.json?language=en"
    fact_response = requests.get(fact_url).json()

    if "text" in fact_response:
        context.bot.send_message(chat_id=update.effective_chat.id, text=fact_response["text"])
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Could not fetch random fact.")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    weather_handler = CommandHandler("weather", weather)
    fact_handler = CommandHandler("fact", random_fact)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(weather_handler)
    dispatcher.add_handler(fact_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

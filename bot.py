import os

import requests

from pyrogram import Client, filters, idle

# AccuWeather API credentials

ACCUWEATHER_API_KEY = "N3co0uwxaCuE0QG9KgwAaRL9vgor5MKe"

# Telegram bot credentials

BOT_TOKEN = '6169875332:AAFgpEnSNbY49ix4Sd1UiRQIbA_jGEhM_ZM'

API_ID = 16743442

API_HASH = '12bbd720f4097ba7713c5e40a11dfd2a'

# Initialize the Telegram bot

bot = Client('weather_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command('start'))

def start_command(client, message):

    # Send a welcome caption and an image

    caption = "Welcome to the AccuWeather Bot\n\nDev: @SexyNano"
    bot.send_photo(message.chat.id, "https://graph.org/file/c59aa664bb6f449f271b5.jpg", caption=caption)

@bot.on_message(filters.command("help"))

def help_command(client, message):

    # Provide help menu with examples

    help_text = (

        "I'm an AccuWeather Bot and I can provide you with weather forecasts.\n\n"
        "Here are some commands you can use:\n"
        "/start - Start the bot and receive a welcome message.\n"
        "/weather location - Get the weather forecast for a specific location.\n"
        "/help - Show this help menu.\n\n"
        "**Example usage:**\n"
        "/weather New York - Get the weather forecast for New York.\n"
        "/weather London, UK - Get the weather forecast for London, UK"

    )

    bot.send_message(message.chat.id, help_text)

@bot.on_message(filters.command('weather'))

def weather_command(client, message):

    # Get the location from the message arguments

    # If no location is provided, send a message requesting the location

    if len(message.command) < 2:

        bot.send_message(message.chat.id, "Please provide a location. For example: /weather New York.")

        return

    location = message.command[1]

    # Query the AccuWeather API for the weather information

    url = 'http://dataservice.accuweather.com/locations/v1/cities/search'

    params = {'apikey': ACCUWEATHER_API_KEY, 'q': location}

    response = requests.get(url, params=params)

    data = response.json()

    # Extract the city key from the API response

    city_key = data[0]['Key']

    # Query the AccuWeather API for the daily forecast

    url = f'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{city_key}'

    params = {'apikey': ACCUWEATHER_API_KEY, 'metric': True}

    response = requests.get(url, params=params)

    data = response.json()

    # Get the weather information for the next day

    date = data['DailyForecasts'][0]['Date']

    temperature_min = data['DailyForecasts'][0]['Temperature']['Minimum']['Value']

    temperature_max = data['DailyForecasts'][0]['Temperature']['Maximum']['Value']

    day_weather_text = data['DailyForecasts'][0]['Day']['IconPhrase']

    night_weather_text = data['DailyForecasts'][0]['Night']['IconPhrase']

    # Send the weather information to the user

    message_text = f"Weather forecast for ```{location}```:\n"
    message_text = f"Date: ```{date}```\n"
    message_text = f"Temperature: ```{temperature_min}```°C - ```{temperature_max}```°C\n"
    message_text = f"Day: ```{day_weather_text}```\n"
    message_text = f"Night: ```{night_weather_text}```\n\n"
    message_text = f"**Whether Info By: @AccuWeatherRoBot**"

    bot.send_message(message.chat.id, message_text)

# Run the bot

bot.run()
idle()

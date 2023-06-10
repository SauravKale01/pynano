import os
import requests
from pyrogram import Client, filters, idle

# AccuWeather API credentials
ACCUWEATHER_API_KEY = 'Ct2XMUchemaAmFlwik3mGDRneIlhiyYc'

# Telegram Bot credentials
BOT_TOKEN = '6169875332:AAFgpEnSNbY49ix4Sd1UiRQIbA_jGEhM_ZM'
API_ID = '16743442'
API_HASH = '12bbd720f4097ba7713c5e40a11dfd2a'

# Initialize the Telegram bot
bot = Client('weather_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start command handler
@bot.on_message(filters.command('start'))
def start_command(client, message):
    # Send a welcome message and an image
    client.send_message(message.chat.id, 'Welcome to the Weather Bot!')
    client.send_photo(message.chat.id, 'https://example.com/welcome_image.jpg')

# Weather command handler
@bot.on_message(filters.command('weather'))
def weather_command(client, message):
    # Get the location from the message arguments
    location = ' '.join(message.command[1:])

    # Query the AccuWeather API for the weather information
    url = f'http://dataservice.accuweather.com/locations/v1/cities/search'
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
    message_text = f'Weather forecast for {location} - {date}:\n'
    message_text += f'Min Temperature: {temperature_min}°C\n'
    message_text += f'Max Temperature: {temperature_max}°C\n'
    message_text += f'Day: {day_weather_text}\n'
    message_text += f'Night: {night_weather_text}\n'
    client.send_message(message.chat.id, message_text)

# Run the bot
bot.run()
idle()

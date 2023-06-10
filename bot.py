import os

import requests

from pyrogram import Client, filters, idle

from pymongo import MongoClient

# AccuWeather API credentials

ACCUWEATHER_API_KEY = 'N3co0uwxaCuE0QG9KgwAaRL9vgor5MKe'

# Telegram Bot credentials

BOT_TOKEN = '6169875332:AAFgpEnSNbY49ix4Sd1UiRQIbA_jGEhM_ZM'

API_ID = '16743442'

API_HASH = '12bbd720f4097ba7713c5e40a11dfd2a'

# MongoDB credentials

MONGODB_URI = 'mongodb+srv://sonu55:sonu55@cluster0.vqztrvk.mongodb.net/?retryWrites=true&w=majority'

MONGODB_DATABASE = 'weather_bot'

MONGODB_COLLECTION = 'users'

# Initialize the Telegram bot

bot = Client('weather_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize the MongoDB client

mongo_client = MongoClient(MONGODB_URI)

db = mongo_client[MONGODB_DATABASE]

users_collection = db[MONGODB_COLLECTION]

# Start command handler

@bot.on_message(filters.command('start'))

def start_command(client, message):

    # Save the user in the database

    user = {

        'user_id': message.from_user.id,

        'username': message.from_user.username,

        'first_name': message.from_user.first_name,

        'last_name': message.from_user.last_name,

    }

    users_collection.insert_one(user)

    # Send a welcome caption and an image

    caption = 'Welcome to the Weather Bot! Enjoy your stay.'

    client.send_photo(message.chat.id, 'https://example.com/welcome_image.jpg', caption=caption)

# Help command handler

@bot.on_message(filters.command('help'))

def help_command(client, message):

    # Provide a help menu with examples

    help_text = (

        "I'm a Weather Bot and I can provide you with weather forecasts!\n\n"

        "Here are some commands you can use:\n"

        "/start - Start the bot and receive a welcome message.\n"

        "/weather <location> - Get the weather forecast for a specific location.\n"

        "/help - Show this help menu.\n"

        "/users - Get the total number of users who started the bot.\n"

        "/broadcast <message> - Send a broadcast message to all users who started the bot.\n\n"

        "Example usage:\n"

        "/weather New York - Get the weather forecast for New York.\n"

        "/weather London, UK - Get the weather forecast for London, UK."

    )

    client.send_message(message.chat.id, help_text)

# Users command handler

@bot.on_message(filters.command('users'))

def users_command(client, message):

    # Get the total number of users from the database

    total_users = users_collection.count_documents({})

    client.send_message(message.chat.id, f"Total users: {total_users}")

# Broadcast command handler

@bot.on_message(filters.command('broadcast'))

def broadcast_command(client, message):

    # Check if the user is an admin (optional)

    # You can customize the admin check according to your requirements

    if message.from_user.id not in [6198858059]:

        client.send_message(message.chat.id, "You are not authorized to use this command.")

        return

    # Get the broadcast message from the command arguments

    broadcast_message = ' '.join(message.command[1:])

    # Fetch all users from the database

    users = users_collection.find()

    # Send the broadcast message to all users

    for user in users:

        user_id = user['user_id']

        client.send_message(user_id, broadcast_message)

# Weather command handler

@bot.on_message(filters.command('weather'))

def weather_command(client, message):

    # Get the location from the message arguments

    if len(message.command) < 2:

        # If no location is provided, send a message requesting the location

        client.send_message(message.chat.id, "Please provide a location. For example: `/weather New York`")

        return

    location = ' '.join(message.command[1:])

    # Query the AccuWeather API for the weather information

    url = f'http://dataservice.accuweather.com/locations/v1/cities/search'

    params = {'apikey': ACCUWEATHER_API_KEY, 'q': location}

    response = requests.get(url, params=params)

    data = response.json()

    if not data:

        client.send_message(message.chat.id, "Location not found.")

        return

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

    message_text += f'**Min Temperature**: {temperature_min}°C\n'

    message_text += f'**Max Temperature**: {temperature_max}°C\n'

    message_text += f'**Day**: {day_weather_text}\n'

    message_text += f'**Night**: {night_weather_text}\n'

    client.send_message(message.chat.id, message_text)

if __name__ == '__main__':

    bot.start()

    # Send a deployment success message

    bot.send_message('-1001905486162', 'Bot deployed successfully!')

    idle()

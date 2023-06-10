import os
import requests
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# AccuWeather API credentials
ACCUWEATHER_API_KEY = 'N3co0uwxaCuE0QG9KgwAaRL9vgor5MKe'

# Telegram Bot credentials
BOT_TOKEN = '6169875332:AAFgpEnSNbY49ix4Sd1UiRQIbA_jGEhM_ZM'
API_ID = '16743442'
API_HASH = '12bbd720f4097ba7713c5e40a11dfd2a'

# Initialize the Telegram bot
bot = Client('weather_bot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start command handler
@bot.on_message(filters.command('start'))
def start_command(client, message):
    # Send a welcome caption and an image
    caption = 'Welcome to the AccuWeather Bot! Enjoy your stay.'
    client.send_photo(message.chat.id, 'https://graph.org/file/c59aa664bb6f449f271b5.jpg', caption=caption)

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
    )
    client.send_message(message.chat.id, help_text)

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

    # Send the weather information to the user with inline query buttons
    message_text = f'Weather forecast for {location} - {date}:\n'
    message_text += f'**Min Temperature**: {temperature_min}°C\n'
    message_text += f'**Max Temperature**: {temperature_max}°C\n'
    message_text += f'**Day**: {day_weather_text}\n'
    message_text += f'**Night**: {night_weather_text}\n'

    inline_keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton('Share', switch_inline_query=location)]]
    )

    client.send_message(message.chat.id, message_text, reply_markup=inline_keyboard)

# Inline query handler
@bot.on_inline_query()
def inline_query_handler(client, inline_query):
    location = inline_query.query

    # Query the AccuWeather API for the weather information
    url = f'http://dataservice.accuweather.com/locations/v1/cities/search'
    params = {'apikey': ACCUWEATHER_API_KEY, 'q': location}
    response = requests.get(url, params=params)
    data = response.json()

    if not data:
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

    # Generate the inline query results with weather information
    results = [
        InlineQueryResultArticle(
            id='1',
            title=f'Weather forecast for {location}',
            input_message_content=InputTextMessageContent(
                f'Weather forecast for {location} - {date}:\n'
                f'**Min Temperature**: {temperature_min}°C\n'
                f'**Max Temperature**: {temperature_max}°C\n'
                f'**Day**: {day_weather_text}\n'
                f'**Night**: {night_weather_text}\n'
            ),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton('Share', switch_inline_query=location)]]
            )
        )
    ]

    client.answer_inline_query(inline_query.id, results)

if __name__ == '__main__':
    bot.start()
    idle()

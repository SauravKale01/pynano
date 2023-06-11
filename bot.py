import requests
from pyrogram import Client, filters, idle
from pyrogram.types import InputMediaPhoto
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# AccuWeather API key
API_KEY = 'N3co0uwxaCuE0QG9KgwAaRL9vgor5MKe'

# Telegram bot token
TOKEN = '6169875332:AAHkcJvM2V7rB-CTKoi9RHp7hOlDy69RGW4'

# API ID and API hash for Pyrogram
API_ID = '16743442'
API_HASH = '12bbd720f4097ba7713c5e40a11dfd2a'

# Pyrogram client
app = Client(
    'my_bot',
    bot_token=TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

# Telegram bot
bot = Updater(TOKEN, use_context=True)
dispatcher = bot.dispatcher

# Command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Weather Bot!")
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action="upload_photo")
    context.bot.send_media_group(
        chat_id=update.effective_chat.id,
        media=[
            InputMediaPhoto(media="https://graph.org/file/c59aa664bb6f449f271b5.jpg", caption="Welcome to the Weather Bot!")
        ]
    )


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Weather handler
def get_weather(update, context):
    city = update.message.text

    # Retrieve weather data
    url = f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={API_KEY}&q={city}"
    response = requests.get(url).json()
    location_key = response[0]['Key']

    url = f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}?apikey={API_KEY}&metric=true"
    response = requests.get(url).json()
    forecasts = response['DailyForecasts']

    # Format weather information
    message = f"Weather forecast for {city}:\n\n"
    for forecast in forecasts:
        date = forecast['Date']
        min_temp = forecast['Temperature']['Minimum']['Value']
        max_temp = forecast['Temperature']['Maximum']['Value']
        day_desc = forecast['Day']['IconPhrase']
        night_desc = forecast['Night']['IconPhrase']
        message += f"Date: {date}\nMin Temp: {min_temp}°C\nMax Temp: {max_temp}°C\nDay: {day_desc}\nNight: {night_desc}\n\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

weather_handler = MessageHandler(Filters.text & (~Filters.command), get_weather)
dispatcher.add_handler(weather_handler)

# Start the bot
bot.start_polling()
bot.idle()

# Start the Pyrogram client
app.run()
idle()

from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests

# Initialize your bot
bot = Client("accuweather_bot", bot_token="6206599982:AAE5HLjxGJA-aSTV0YZCgFnrpgzGhtvIoMA", api_id=16743442, api_hash="12bbd720f4097ba7713c5e40a11dfd2a")

# Define the AccuWeather API endpoint and your API key
base_url = "http://dataservice.accuweather.com"
api_key = "Ct2XMUchemaAmFlwik3mGDRneIlhiyYc"

# Handle the "/start" command
@bot.on_message(filters.command("start"))
def start(bot: Client, message: Message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Welcome to AccuWeather Bot!\n\nUse /weather <location> to get the current weather information for a location.",
    )

# Handle the "/weather" command
@bot.on_message(filters.command("weather"))
def weather(bot: Client, message: Message):
    # Get the location from the command arguments
    location = " ".join(message.command[1:])

    # Make a request to the AccuWeather API to get the weather information
    endpoint = f"{base_url}/locations/v1/cities/search"
    params = {
        "apikey": api_key,
        "q": location
    }
    response = requests.get(endpoint, params=params)
    data = response.json()

    if data:
        location_key = data[0]["Key"]
        forecast_endpoint = f"{base_url}/currentconditions/v1/{location_key}"
        forecast_params = {
            "apikey": api_key
        }
        forecast_response = requests.get(forecast_endpoint, params=forecast_params)
        forecast_data = forecast_response.json()

        if forecast_data:
            weather_text = forecast_data[0]["WeatherText"]
            temperature = forecast_data[0]["Temperature"]["Metric"]["Value"]
            bot.send_message(
                chat_id=message.chat.id,
                text=f"The weather in {location} is {weather_text} with a temperature of {temperature}°C.",
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text="Unable to fetch the weather information.",
            )
    else:
        bot.send_message(chat_id=message.chat.id, text="Location not found.")

# Handle inline queries
@bot.on_inline_query()
def inline_weather(bot: Client, query):
    # Get the query text (location) from the inline query
    location = query.query

    # Make a request to the AccuWeather API to get the weather information
    endpoint = f"{base_url}/locations/v1/cities/search"
    params = {
        "apikey": api_key,
        "q": location
    }
    response = requests.get(endpoint, params=params)
    data = response.json()

    if data:
        location_key = data[0]["Key"]
        forecast_endpoint = f"{base_url}/currentconditions/v1/{location_key}"
        forecast_params = {
            "apikey": api_key
        }
        forecast_response = requests.get(forecast_endpoint, params=forecast_params)
        forecast_data = forecast_response.json()

        if forecast_data:
            weather_text = forecast_data[0]["WeatherText"]
            temperature = forecast_data[0]["Temperature"]["Metric"]["Value"]
            results = [
                InlineQueryResultArticle(
                    id="1",
                    title=f"Weather in {location}",
                    input_message_content=InputTextMessageContent(
                        f"The weather in {location} is {weather_text} with a temperature of {temperature}°C."
                    ),
                )
            ]
            bot.answer_inline_query(query.id, results=results)
        else:
            bot.answer_inline_query(query.id, results=[])
    else:
        bot.answer_inline_query(query.id, results=[])

# Handle the "/help" command
@bot.on_message(filters.command("help"))
def help(bot: Client, message: Message):
    help_text = (
        "AccuWeather Bot Help\n\n"
        "This bot provides the current weather information for a location.\n\n"
        "Commands:\n"
        "/start - Start the bot and get a welcome message.\n"
        "/help - Get help and instructions for using the bot.\n"
        "/weather <location> - Get the current weather for a location."
    )
    bot.send_message(chat_id=message.chat.id, text=help_text)

# Error handling
@bot.on_message(filters.command("weather") & filters.private)
def error_handler(bot: Client, message: Message):
    bot.send_message(chat_id=message.chat.id, text="Please provide a valid location.")

# Run the bot
bot.run()
idle()

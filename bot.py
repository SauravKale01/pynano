from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import requests

# Initialize your bot
bot = Client("accuweather_bot", bot_token="6169875332:AAFgpEnSNbY49ix4Sd1UiRQIbA_jGEhM_ZM", api_id=16743442, api_hash="12bbd720f4097ba7713c5e40a11dfd2a")

# Define the AccuWeather API endpoint and your API key
base_url = "http://dataservice.accuweather.com"
api_key = "Ct2XMUchemaAmFlwik3mGDRneIlhiyYc"

# Handle the "/start" command
@bot.on_message(filters.command("start"))
def start(bot: Client, message: Message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Welcome to AccuWeather Bot!\n\nUse /weather <location> to get the current weather information for a location.\n\n➠ Dev : @SexyNano",
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
        forecast_endpoint = f"{base_url}/forecasts/v1/daily/5day/{location_key}"
        forecast_params = {
            "apikey": api_key,
            "metric": True
        }
        forecast_response = requests.get(forecast_endpoint, params=forecast_params)
        forecast_data = forecast_response.json()

        if forecast_data:
            bot.send_message(
                chat_id=message.chat.id,
                text=f"Weather in {location}:"
            )

            for day in forecast_data["DailyForecasts"]:
                date = day["Date"]
                min_temp = day["Temperature"]["Minimum"]["Value"]
                max_temp = day["Temperature"]["Maximum"]["Value"]
                day_text = day["Day"]["IconPhrase"]
                night_text = day["Night"]["IconPhrase"]

                weather_text = (
                    f"Date: {date}\n"
                    f"Min Temp: {min_temp}°C\n"
                    f"Max Temp: {max_temp}°C\n"
                    f"Day: {day_text}\n"
                    f"Night: {night_text}\n\n"
                )

                bot.send_message(
                    chat_id=message.chat.id,
                    text=weather_text
                )

            # Send inline button for more information
            button_text = "More Information"
            button_data = f"more_{location}"
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(button_text, callback_data=button_data)]])
            bot.send_message(
                chat_id=message.chat.id,
                text="For more information, click the button below:",
                reply_markup=reply_markup
            )
        else:
            bot.send_message(
                chat_id=message.chat.id,
                text="Unable to fetch the weather information.",
            )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Location not found.",
        )

# Handle inline button callbacks
@bot.on_callback_query()
def button_callback(bot: Client, query):
    callback_data = query.data

    if callback_data.startswith("more_"):
        location = callback_data[5:]
        bot.send_message(
            chat_id=query.message.chat.id,
            text=f"More information about {location}..."
        )
        # You can add more code here to fetch and send additional information about the weather for the location

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
      

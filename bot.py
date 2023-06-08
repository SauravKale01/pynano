import pyrogram
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Replace with your own API credentials
api_id = "16743442"
api_hash = "12bbd720f4097ba7713c5e40a11dfd2a"
bot_token = "6206599982:AAEtRoU2jV7heQn8t0Zkwh1L6khiC8EXfcM"

# Create a Pyrogram client
app = pyrogram.Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Start command handler

@app.on_message(filters.command("start"))
def start_command(client, message):

    # Send a welcome message with an image
    client.send_photo(
        chat_id=message.chat.id,
        photo="https://graph.org/file/0f929eba3345324c98f3e.jpg",
        caption=f"🟢 **Name:** Nano\n"
                f"🟢 **Username:** @SexyNano\n"
                f"🟢 **User ID:** 6198858059\n"
                f"🟢 **Birthday:** 03 June\n"
                f"🟢 **Age:** 18+\n"
                f"🟢 **From:** Maharashtra\n"
    )

# Help command handler

@app.on_message(filters.command("help"))
def help_command(client, message):

    # Create an inline keyboard with bot list
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Camellia", url="t.me.MissCamellia_Bot")],
            [InlineKeyboardButton("Nobara Music", url="t.me.Nobara_Music_Bot")],
            [InlineKeyboardButton("Temp Mail Bot", url="t.me.TempMailGenRoBot")],
            [InlineKeyboardButton("The Komi", url="t.me.TheKomi_Bot")],
            [InlineKeyboardButton("My Channel", url="t.me.Index_AC")],
            [InlineKeyboardButton("Chat Group", url="t.me.Anime_Krew")],
        ]
    )

    # Get your bot's information
    bot_info = app.get_chat(bot_token)

    # Construct the help message with bot info

    help_message = f"🤖 **My Bot Info** 🤖\n\n" \
                   f"🟢 **Name:**About Nano\n" \
                   f"🟢 **Username:**@AboutNanoBot\n" \
                   f"🟢 **Description:**This Bot Made By Nano\n"

    # Send help message with inline keyboard
    client.send_message(
        chat_id=message.chat.id,
        text=help_message,
        reply_markup=keyboard
    )
# Run the bot
app.start()
idle()

from pyrogram import Client, filters, idle

app = Client("my_bot", config_file="config.py")

@app.on_message(filters.command("hello"))
def hello(_, message):
    message.reply_text("Hello, world!")

app.run()
idle()

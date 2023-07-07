import os
from pyrogram import Client, filters, idle
from PIL import Image, ImageDraw, ImageOps
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Add any button you want below your welcome image
markup = InlineKeyboardMarkup([[InlineKeyboardButton("MODS", url="https://t.me/xxx")]])

# Your bot credentials and access tokens
api_id = 16743442  # Replace with your API ID
api_hash = "12bbd720f4097ba7713c5e40a11dfd2a"  # Replace with your API hash
bot_token = "your_bot_token"  # Replace with your bot token

# Create the Client object
app = Client("welcome_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Paths for the welcome template image and the generated welcome images
welcome_template_image_path = "path/to/welcome_template.jpg"
welcome_images_directory = "path/to/welcome_images"

@app.on_message(filters.new_chat_members & filters.group)
async def welcome(_, message):
    for user in message.new_chat_members:
        try:
            profile_pic_url = user.photo.big_file_id
            response = await app.download_media(profile_pic_url)

            # Modify the dimensions and appearance of the welcome image as desired
            image_width = 600
            image_height = 400
            
            # Load the custom welcome template image
            welcome_image = Image.open(welcome_template_image_path)
            welcome_image = welcome_image.resize((image_width, image_height))
            
            # Load and resize the new user's profile picture
            profile_pic = Image.open(response)
            profile_pic = profile_pic.resize((150, 150))
            
            # Create a new blank image for the combined welcome image
            welcome_with_profile_pic = Image.new("RGB", (image_width, image_height))
            
            # Paste the welcome template onto the new image
            welcome_with_profile_pic.paste(welcome_image, (0, 0))
            
            # Apply a circular mask to the profile picture
            mask = Image.new("L", profile_pic.size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, profile_pic.size[0], profile_pic.size[1]), fill=255)
            profile_pic = ImageOps.fit(profile_pic, mask.size)
            profile_pic.putalpha(mask)
            
            # Calculate the position of the profile picture on the left side
            profile_pic_position = (10, (image_height - profile_pic.height) // 2)
            
            # Paste the circular profile picture onto the welcome image
            welcome_with_profile_pic.paste(profile_pic, profile_pic_position, profile_pic)
            
            # Save the final welcome image with a unique name
            welcome_image_filename = f"welcome_{user.id}.jpg"
            welcome_image_path = os.path.join(welcome_images_directory, welcome_image_filename)
            welcome_with_profile_pic.save(welcome_image_path)
            
            # Specify the welcome message
            msg = f"""
Welcome to {message.chat.title}!

NAME: {user.first_name}
ID: {user.id}
USERNAME: @{user.username}
COUNT: {await app.get_chat_members_count(message.chat.id)}
"""
            
            # Reply to the message with the custom welcome image and caption
            await message.reply_photo(photo=open(welcome_image_path, 'rb'), caption=msg, reply_markup=markup)
        except Exception as e:
            print(f"Error sending welcome message for {user.first_name}: {str(e)}")

# Run the client
app.run()
idle()

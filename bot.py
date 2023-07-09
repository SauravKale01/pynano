import os
from pyrogram import Client, filters, idle
from PIL import Image, ImageDraw, ImageOps, ImageFont
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api_id=''
api_hash=''
bot_token=''

# client installtion
app= Client('welcome_bot', api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Add any button you want below your welcome image
markup = InlineKeyboardMarkup([[InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/JHBots")]])

@app.on_message(filters.new_chat_members & filters.group)
async def welcome(_, message):
    for user in message.new_chat_members:
        try:
            profile_pic_url = user.photo.big_file_id
            response = await app.download_media(profile_pic_url)
            
            # Modify the dimensions and appearance of the welcome image as desired
            image_width = 1280
            image_height = 720
            
            # Load the custom welcome template image
            welcome_image = Image.open("template/UchihaMadara.png")
            welcome_image = welcome_image.resize((image_width, image_height))
            
            # Load and resize the new user's profile picture
            profile_pic = Image.open(response)
            profile_pic = profile_pic.resize((300, 300))
            
            # Create a new blank image for the combined welcome image
            welcome_with_profile_pic = Image.new("RGB", (image_width, image_height))
            
            # Paste the welcome template onto the new image
            welcome_with_profile_pic.paste(welcome_image, (0, 0))
            
            # Apply a circular mask to the profile picture
            mask = Image.new("L", profile_pic.size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, profile_pic.size[0], profile_pic.size[1]), fill=455)
            profile_pic = ImageOps.fit(profile_pic, mask.size)
            profile_pic.putalpha(mask)

            # Add an outline to the profile picture
            outline_color = (255, 255, 255)  # White color for the outline
            border_width = 9  # Adjust the border width as desired
            profile_pic_with_outline = ImageOps.expand(profile_pic, border=border_width, fill=outline_color)            
            
            # Calculate the position of the profile picture on the left side
            profile_pic_position = (150, (image_height - profile_pic.height) // 2 + 140)
            
            # Paste the circular profile picture onto the welcome image
            welcome_with_profile_pic.paste(profile_pic, profile_pic_position, profile_pic)                                  
            
            # Save the final welcome image with a unique name based on the user's ID
            welcome_image_path = f"welcome_{user.id}.jpg"
            welcome_with_profile_pic.save(welcome_image_path)
            
            # Specify the welcome message
            msg = f"""
Hᴇʏ! {user.first_name}, Wᴇʟᴄᴏᴍᴇ Tᴏ ~ {message.chat.title}!

Mʏ Sʜᴀʀɪɴɢᴀɴ Aʟᴡᴀʏs Wᴀᴛᴄʜɪɴɢ Yᴏᴜ!
"""
            
            # Reply to the message with the custom welcome image and caption
            await message.reply_photo(photo=welcome_image_path, caption=msg, reply_markup=markup)
            
            # Remove the temporary welcome image file
            welcome_with_profile_pic.close()
            os.remove(welcome_image_path)
        except Exception as e:
            print(f"Error sending welcome message for {user.first_name}: {str(e)}")

# run the bot
app.run()
idle()


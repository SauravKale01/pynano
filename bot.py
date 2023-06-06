from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
from pyrogram import idle

app = Flask(__name__)

@app.route('/welcome_image', methods=['POST'])
def generate_welcome_image():
    data = request.get_json()
    name = data['name']
    username = data['username']
    group_name = data['group_name']

    # Load the background image
    background_image = Image.open('IMG_20230601_152627_048.jpg')

    # Create a copy of the background image
    welcome_image = background_image.copy()

    # Set the font style and size
    font = ImageFont.truetype('arial.ttf', 30)

    # Create a drawing object
    draw = ImageDraw.Draw(welcome_image)

    # Write the welcome message
    welcome_message = f"Welcome to {group_name}!"
    draw.text((50, 50), welcome_message, fill='white', font=font)

    # Write the user details
    user_details = f"Name: {name}\nUsername: {username}"
    draw.text((50, 100), user_details, fill='white', font=font)

    # Save the generated image
    welcome_image.save('welcome_image.jpg')

    response = {
        'message': 'Welcome image generated successfully!',
        'image_url': 'https://my-flask-app.herokuapp.com/welcome_image.jpg'
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run()
    idle() 

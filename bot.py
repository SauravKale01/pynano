from pyrogram import Client, filters, idle

import requests

bot_token = "6206599982:AAEtRoU2jV7heQn8t0Zkwh1L6khiC8EXfcM"

api_id = "16743442"

api_hash = "12bbd720f4097ba7713c5e40a11dfd2a"

bot = Client("pet_care_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

PETFINDER_API_URL = "https://api.petfinder.com/v2"
YOUR_PETFINDER_API_TOKEN = "ebWoRlapNs1QBu3N65cAhxMU9wzGo1VvicGQUY6Ad0d3NOrxjU"

@bot.on_message(filters.command("start"))

def start_command(client, message):

    client.send_message(message.chat.id, "Welcome to Pet Care Bot! How can I assist you?")

@bot.on_message(filters.command("petcaretips"))

def pet_care_tips_command(client, message):

    client.send_message(message.chat.id, "Sorry, pet care tips are currently unavailable. Please try again later.")

@bot.on_message(filters.command("breedinfo"))

def breed_info_command(client, message):

    if len(message.command) < 2:

        client.send_message(message.chat.id, "Please provide a breed name.")

        return

    breed_name = " ".join(message.command[1:])

    headers = {"Authorization": f"Bearer {YOUR_PETFINDER_API_TOKEN}"}

    response = requests.get(f"{PETFINDER_API_URL}/types/dog/breeds?q={breed_name}", headers=headers)

    data = response.json()

    if "breeds" not in data:

        client.send_message(message.chat.id, "Breed information not found.")

        return

    breed = data["breeds"][0]

    breed_info = f"Breed Name: {breed['name']}\n\nDescription: {breed['description']}"

    client.send_message(message.chat.id, breed_info)

@bot.on_message(filters.command("findvet"))

def find_vet_command(client, message):

    if len(message.command) < 2:

        client.send_message(message.chat.id, "Please provide your location.")

        return

    location = " ".join(message.command[1:])

    headers = {"Authorization": f"Bearer {YOUR_PETFINDER_API_TOKEN}"}

    response = requests.get(f"{PETFINDER_API_URL}/organizations?type=veterinarian&location={location}", headers=headers)

    data = response.json()

    if "organizations" not in data:

        client.send_message(message.chat.id, "No veterinary services found.")

        return

    organizations = data["organizations"]

    vet_info = "Veterinary Services near you:\n\n"

    for org in organizations:

        vet_info += f"Name: {org['name']}\nLocation: {org['address']['address1']}, {org['address']['city']}\n\n"

    client.send_message(message.chat.id, vet_info)

bot.run()
idle()

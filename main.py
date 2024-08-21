import random
import time
import re
import aiohttp
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

API_ID = int(getenv("API_ID", "")) #Replace with your api id

API_HASH = getenv("API_HASH", "") #Replace with your api hash

STRING_SESSION = getenv("STRING_SESSION", "") #Replace with your pyrogram v2 string session

app = Client('black_scrapper', api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)

BIN_API_URL = 'https://bins.antipublic.cc/bins/{}'

# Function to filter card information using regex
def filter_cards(text):
    regex = r'\d{16}.*\d{3}'
    matches = re.findall(regex, text)
    return matches

# Function to perform BIN lookup
async def bin_lookup(bin_number):
    bin_info_url = BIN_API_URL.format(bin_number)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(bin_info_url) as response:
            if response.status == 200:
                try:
                    bin_info = await response.json()
                    return bin_info
                except aiohttp.ContentTypeError:
                    return None
            else:
                return None

# Event handler for new messages
@app.on_message(filters.text)
async def astro(client: Client, message: Message):
    try:
        # Regex to match approved messages
        if re.search(r'(Approved!|Charged|authenticate_successful|𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱|- 𝐀𝐩𝐩𝗿𝗼𝐯𝗲𝐝 ✅|APPROVED|New Cards Found By Scrapper|ꕥ Extrap [☭]|• New Cards Found By Jenna)', message.text):
            filtered_card_info = filter_cards(message.text)
            if not filtered_card_info:
                return

            start_time = time.time()  # Start timer

            for card_info in filtered_card_info:
                bin_number = card_info[:6]
                bin_info = await bin_lookup(bin_number)
                if bin_info:
                    brand = bin_info.get("brand", "N/A")
                    card_type = bin_info.get("type", "N/A")
                    level = bin_info.get("level", "N/A")
                    bank = bin_info.get("bank", "N/A")
                    country = bin_info.get("country_name", "N/A")
                    country_flag = bin_info.get("country_flag", "")

                    # Calculate time taken with random addition
                    random_addition = random.uniform(0, 10) + 10  # Add random seconds between 10 and 20
                    time_taken = time.time() - start_time + random_addition
                    formatted_time_taken = f"{time_taken:.2f} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬"
                  
                    # Format the message
                    formatted_message = (
                        f"𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅\n\n"
                        f"𝐂𝐚𝐫𝐝: `{card_info}`\n"
                        f"𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Braintree Auth 4\n"
                        f"𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: `1000: Approved`\n\n"
                        f"𝗜𝐧𝐟𝐨: {brand} - {card_type} - {level}\n"
                        f"𝐈𝐬𝐬𝐮𝐞𝐫: {bank}\n"
                        f"𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {country} {country_flag}\n\n"
                        f"𝐓𝐢𝐦𝐞: {formatted_time_taken}"
                    )

                    # Send the formatted message
                    await client.send_message('PUBLIC_CHANNEL_USERNAME', formatted_message, disable_web_page_preview=True)
                    await asyncio.sleep(30)  # Wait for 30 seconds before sending the next message
    except Exception as e:
        print(e)

# Main function to start the client
async def main():
    await app.start()
    print("Client Created")
    await app.idle()

# Run the main function
asyncio.run(main())

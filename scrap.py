import discord
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

# Discord API token
load_dotenv()
api_key = os.environ.get("API_KEY")


# Connect to Discord
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


# Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# Fetch Google Sheets API credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name('gs_dcscraping_credentials.json', scope)

# Initialize Google Sheets Client
gc = gspread.authorize(credentials)

# Open the Google Sheet
worksheet = gc.open_by_key("11b2o7N0jn_0bUhUDcrF8u8ciAGmeS9kud06zgb2liOs").sheet1

keywords = ["UID", "頭條預測"]
channel_id = 1061935943747129355 # replace with the target channel's ID

@client.event
async def on_ready():
    channel = client.get_channel(1064084359046508585)
    async for message in channel.history(limit=100):
        if any(keyword in message.content for keyword in keywords):
            print(f"{message.author} said {message.content} in {channel.name} at {message.created_at}")
    worksheet.append_row([message.author.name, message.content, channel.name, message.created_at.strftime('%Y-%m-%d %H:%M:%S')])
    

client.run(api_key)


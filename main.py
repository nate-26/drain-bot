import discord
from discord.ext import commands
import time
import os 
from dotenv import load_dotenv

TARGET_ARTISTS = ["Bladee", "Ecco2k", "WhiteArmor", "Thaiboy Digital", "Yung Lean"] 
COOLDOWN_SECONDS = 0 # change later lol

intents = discord.Intents.default()
intents.presences = True
intents.members = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# history tracker for cooldown stuff
last_announced = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_presence_update(before, after):
    # only spotify lol
    for activity in after.activities:
        if isinstance(activity, discord.Spotify):
            if any(target.lower() in activity.artist.lower() for target in TARGET_ARTISTS):
                now = time.time()
                last_time = last_announced.get(after.id, 0) 

                # based on cooldown timer
                if now - last_time >= COOLDOWN_SECONDS: 
                    last_announced[after.id] = now
                    channel = discord.utils.get(after.guild.text_channels, name="bot")
                    if channel:
                        await channel.send(f"{after.mention} is currently draining!!! ({activity.artist}) 🎶")
                    break

# bot token
load_dotenv()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
import discord
from discord.ext import commands
import time
import os 
from dotenv import load_dotenv

TARGET_ARTISTS = ["Bladee", "Ecco2k", "Whitearmor", "Thaiboy Digital", "Yung Lean"] 
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

ARTIST_IMAGES = {
    "Bladee": "images/drain-gang-bladee.gif",
    "Ecco2k": "images/ecco2k.gif",
    "Whitearmor": "images/whitearmor.jpg",
    "Thaiboy Digital": "images/thaiboy.gif",
    "Yung Lean": "images/yung_lean.jpg"
}

@bot.event
async def on_presence_update(before, after):
    # only spotify lol
    for activity in after.activities:
        if isinstance(activity, discord.Spotify):
            matched_artist = next(
                (artist for artist in TARGET_ARTISTS if artist.lower() in activity.artist.lower()), None
            )
            if matched_artist:
                now = time.time()
                last_time = last_announced.get(after.id, 0) 

                # based on cooldown timer
                if now - last_time >= COOLDOWN_SECONDS: 
                    last_announced[after.id] = now
                    channel = discord.utils.get(after.guild.text_channels, name="bot")
                    if channel:
                        # await channel.send(f"{after.mention} is currently draining!!! ({activity.artist}) 🎶")
                        artist_name = activity.artist
                        #image_url = ARTIST_IMAGES.get(artist_name)
                        embed = discord.Embed(
                            title=f"{after.display_name} is currently draining!!! ({activity.artist}) 🎶",
                            color=discord.Color.blue()
                        )

                        image_path = ARTIST_IMAGES.get(matched_artist)

                        if image_path and os.path.exists(image_path):
                            filename = os.path.basename(image_path)
                            file = discord.File(image_path, filename=filename)
                            embed.set_image(url=f"attachment://{filename}")
                            await channel.send(content=after.mention, embed=embed, file=file)
                        else: 
                            await channel.send(content=after.mention, embed=embed)
                    break

# bot token
load_dotenv()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
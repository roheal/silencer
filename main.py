import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# --- Keep-alive web server setup ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# --- Discord bot setup ---
intents = discord.Intents.all()  # Enable all intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
@commands.has_permissions(mute_members=True)
async def muteall(ctx):
    if ctx.author.voice is None:
        await ctx.send("You're not in a voice channel.")
        return
    voice_channel = ctx.author.voice.channel
    for member in voice_channel.members:
        await member.edit(mute=True)
    await ctx.send("All members muted.")

@bot.command()
@commands.has_permissions(mute_members=True)
async def unmuteall(ctx):
    if ctx.author.voice is None:
        await ctx.send("You're not in a voice channel.")
        return
    voice_channel = ctx.author.voice.channel
    for member in voice_channel.members:
        await member.edit(mute=False)
    await ctx.send("All members unmuted.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    else:
        await ctx.send(f"An error occurred: {error}")

# Run the bot with token from Replit Secrets
bot.run(os.environ['YOUR_BOT_TOKEN'])

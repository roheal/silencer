import os
import discord
from discord.ext import commands

# Enable all necessary intents
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True  # 🔥 Required for command reading

# Define bot prefix and create the bot instance
bot = commands.Bot(command_prefix="-", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    # Set custom status: Listening to -muteall & -unmuteall
    activity = discord.Activity(type=discord.ActivityType.listening, name="-muteall & -unmuteall")
    await bot.change_presence(activity=activity)

@bot.command(aliases=["mute"])
@commands.has_permissions(mute_members=True)
async def muteall(ctx):
    """Server mute everyone in the voice channel you're in"""
    if ctx.author.voice and ctx.author.voice.channel:
        vc = ctx.author.voice.channel
        for member in vc.members:
            try:
                await member.edit(mute=True)
                print(f"✅ Muted {member.display_name}")
            except discord.Forbidden:
                await ctx.send(f"❌ Missing permission to mute {member.display_name}")
            except Exception as e:
                await ctx.send(f"❌ Error muting {member.display_name}: {e}")
        await ctx.send(f"🔇 Everyone in **{vc.name}** has been muted.")
    else:
        await ctx.send("❌ You must be in a voice channel to use this command.")

@bot.command(aliases=["unmute"])
@commands.has_permissions(mute_members=True)
async def unmuteall(ctx):
    """Unmute everyone in your voice channel"""
    if ctx.author.voice and ctx.author.voice.channel:
        vc = ctx.author.voice.channel
        for member in vc.members:
            try:
                await member.edit(mute=False)
                print(f"✅ Unmuted {member.display_name}")
            except discord.Forbidden:
                await ctx.send(f"❌ Missing permission to unmute {member.display_name}")
            except Exception as e:
                await ctx.send(f"❌ Error unmuting {member.display_name}: {e}")
        await ctx.send(f"🔊 Everyone in **{vc.name}** has been unmuted.")
    else:
        await ctx.send("❌ You must be in a voice channel to use this command.")

# Run the bot with token from Replit Secrets
bot.run(os.environ['YOUR_BOT_TOKEN'])

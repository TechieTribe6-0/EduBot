import asyncio
import discord
import os
from timer import Timer
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

bot = commands.Bot(command_prefix='!')

timer = Timer()

@bot.event
async def on_ready():
    print('We have logged in as {}'.format(bot.user))

@bot.command(name='start', help="Starts a Pomodoro timer")
async def start_timer(ctx):
    start_work_cm = discord.Embed(title="Time to start working!", color=0x33c633)
    await ctx.send(embed = start_work_cm)

    timer.start()
    while timer.get_status():
        await asyncio.sleep(1)
        if timer.get_ticks()>=10:
            timer.stop()

    start_play_em = discord.Embed(title="Time to start your break!", color=0x33c633)


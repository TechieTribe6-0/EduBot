import asyncio
from email import message
import discord
import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
from enum import Enum


COLOR_DANGER = 0xc63333
COLOR_SUCCESS = 0x33c633

class TimerStatus(Enum):
    INITIALIZED = 1
    RUNNING = 2
    STOPPED = 3
    EXPIRED = 4


class Timer:

    def __init__(self):
        self.status = TimerStatus.INITIALIZED
        self.ticks = 0

    def get_status(self):
        return self.status

    def start(self, max_ticks):
        self.max_ticks = max_ticks
        self.status = TimerStatus.RUNNING
        self.ticks = 0

    def stop(self):
        self.status = TimerStatus.STOPPED

    def get_ticks(self):
        return self.ticks

    def tick(self):
        self.ticks += 1
        if self.get_ticks() >= self.max_ticks:
            self.status = TimerStatus.EXPIRED


def create_tables():
    db = sqlite3.connect('pomobot.db')
    cur = db.cursor()
    # Create table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS alarms (
        id integer PRIMARY KEY AUTOINCREMENT,
        username text NOT NULL,
        start_time text NOT NULL,
        delay text NOT NULL
        )
    ''')
    db.commit()


async def startTimer(message, timer):
    print("Start called")
    db = sqlite3.connect('pomobot.db')
    if timer.get_status() == TimerStatus.RUNNING:
        await show_message(message, "Timer is already running! You should stop the timer before you can restart it!", COLOR_SUCCESS)    
        return

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    cur = db.cursor()
    cur.execute('''
    INSERT INTO alarms (username, start_time, delay)
        VALUES (?,?,?)
    ''', [str(message.author),current_time,'10'])
    db.commit()

    cur = db.cursor()
    for row in cur.execute('SELECT * FROM alarms'):
        print(row)

    await show_message(message, "Time to start working!", COLOR_SUCCESS)
    timer.start(max_ticks=10)
    while timer.get_status() == TimerStatus.RUNNING:
        await asyncio.sleep(1)
        timer.tick()
    if timer.get_status() == TimerStatus.EXPIRED:
        await show_message(message, "Time to start your break!", COLOR_SUCCESS)
        timer.start(max_ticks=10)
        while timer.get_status() == TimerStatus.RUNNING:
            await asyncio.sleep(1)
            timer.tick()
        if timer.get_status() == TimerStatus.EXPIRED:
            await show_message(message, "Okay, break over!", COLOR_SUCCESS)


async def show_message(message, title, color):
    start_work_em = discord.Embed(title=title, color=color)
    await message.channel.send(embed=start_work_em)


async def stopTimer(message, timer):

    if timer.get_status() != TimerStatus.RUNNING:
        await show_message(message, "Timer is already stopped! You should start the timer before you can stop it!", COLOR_SUCCESS)    
        return        
    await show_message(message, "Timer has been stopped!", COLOR_DANGER)
    timer.stop()


async def show_time(message, timer):
    await message.channel.send(f"Current timer status is : {timer.get_status()}")
    await message.channel.send(f"Current time is : {timer.get_ticks()}")


#     @commands.command()
#     async def show_help(self, message):
#         help_commands = dict()
#         for command in self.bot.commands:
#             help_commands[command.name] = command.help
#         description = "Bot commands are: {}".format(help_commands)
#         show_help_em = discord.Embed(title="This is Mr Pomo Dorio, a friendly Pomodoro bot", description=description,
#                                     color=COLOR_SUCCESS)
#         await message.channel.send(embed=show_help_em)

# def setup(client):
#     client.add_cog(DiscordCog(client))
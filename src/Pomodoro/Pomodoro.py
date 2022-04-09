import asyncio
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

class DiscordCog(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.timer = Timer()
        self.db = sqlite3.connect('pomobot.db')
        self.create_tables()


    def create_tables(self):
        cur = self.db.cursor()
        # Create table
        cur.execute('''
        CREATE TABLE IF NOT EXISTS alarms (
            id integer PRIMARY KEY AUTOINCREMENT,
            username text NOT NULL,
            start_time text NOT NULL,
            delay text NOT NULL
            )
        ''')
        self.db.commit()


    @commands.Cog.listener()
    async def on_ready(self):
        print('We have logged in as {}'.format(self.bot.user))

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     await message.channel.send('Started!')

    @commands.command()
    async def start(self, ctx):
        print("Start called")
        if self.timer.get_status() == TimerStatus.RUNNING:
            await self.show_message(ctx, "Timer is already running! You should stop the timer before you can restart it!", COLOR_SUCCESS)    
            return

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        cur = self.db.cursor()
        cur.execute('''
        INSERT INTO alarms (username, start_time, delay)
            VALUES (?,?,?)
        ''', [str(ctx.author),current_time,'10'])
        self.db.commit()

        cur = self.db.cursor()
        for row in cur.execute('SELECT * FROM alarms'):
            print(row)

        await self.show_message(ctx, "Time to start working!", COLOR_SUCCESS)
        self.timer.start(max_ticks=10)
        while self.timer.get_status() == TimerStatus.RUNNING:
            await asyncio.sleep(1)
            self.timer.tick()
        if self.timer.get_status() == TimerStatus.EXPIRED:
            await self.show_message(ctx, "Time to start your break!", COLOR_SUCCESS)
            self.timer.start(max_ticks=10)
            while self.timer.get_status() == TimerStatus.RUNNING:
                await asyncio.sleep(1)
                self.timer.tick()
            if self.timer.get_status() == TimerStatus.EXPIRED:
                await self.show_message(ctx, "Okay, break over!", COLOR_SUCCESS)


    async def show_message(self, ctx, title, color):
        start_work_em = discord.Embed(title=title, color=color)
        await ctx.send(embed=start_work_em)


    @commands.command()
    async def stop(self, ctx):
        if self.timer.get_status() != TimerStatus.RUNNING:
            await self.show_message(ctx, "Timer is already stopped! You should start the timer before you can stop it!", COLOR_SUCCESS)    
            return        
        await self.show_message(ctx, "Timer has been stopped!", COLOR_DANGER)
        self.timer.stop()


    @commands.command()
    async def show_time(self, ctx):
        await ctx.send(f"Current timer status is : {self.timer.get_status()}")
        await ctx.send(f"Current time is : {self.timer.get_ticks()}")


    @commands.command()
    async def show_help(self, ctx):
        help_commands = dict()
        for command in self.bot.commands:
            help_commands[command.name] = command.help
        description = "Bot commands are: {}".format(help_commands)
        show_help_em = discord.Embed(title="This is Mr Pomo Dorio, a friendly Pomodoro bot", description=description,
                                    color=COLOR_SUCCESS)
        await ctx.send(embed=show_help_em)

def setup(client):
    client.add_cog(DiscordCog(client))
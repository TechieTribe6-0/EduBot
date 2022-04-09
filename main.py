import discord
import os 
from dotenv import load_dotenv

from src.Todo.Todo import get_tasks, getEmbededTasks, perform_crd_tasks
load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in")

@client.event
async def on_message(message):
    if message.author == client.user:
        return 
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$todo'):
        response = perform_crd_tasks(message)
        if(response):
            await message.channel.send(response)
        tasks = get_tasks(message.author.name)
        taskEmbed = getEmbededTasks(message, tasks)
        await message.channel.send(embed=taskEmbed)
        

client.run(os.getenv('TOKEN'))

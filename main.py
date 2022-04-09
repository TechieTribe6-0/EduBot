from src.Pomodoro.Pomodoro import DiscordCog
import os 
from discord.ext import commands
from dotenv import load_dotenv

from src.Todo.Todo import get_tasks, getEmbededTasks, perform_crd_tasks
load_dotenv()

client = commands.Bot(command_prefix='!', help_command=None)
client.add_cog(DiscordCog(client))
client.run(os.getenv('TOKEN'))

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

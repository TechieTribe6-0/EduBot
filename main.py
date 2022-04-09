from src.Pomodoro.Pomodoro import DiscordCog
import os 
from discord.ext import commands
from dotenv import load_dotenv
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




# print(os.getenv('TOKEN'))


# if __name__ =='__main__':
#     client.load_extension('src.Pomodoro.Pomodoro')


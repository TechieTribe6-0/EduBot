import discord
import sys
import subprocess
import os
from dotenv import load_dotenv
load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
  print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
  global msg
  msg = message
  if message.author == client.user : return

#   if str(message.channel) == channel and message.content.startswith("#python3"):
  if message.content.startswith("#python3"):
    await message.channel.send('Python bot')
    print(message.content)  
    f = open("demo.py", "w")
    f.write(message.content)
    f.close()
    f = open("demo.py",'r')
    lines = f.readlines()[1:]
    print(lines)
    f.close()
    # msg = """print('Hello World')"""
    # msg = str(msg)
    try :
      # for line in lines:
      run = subprocess.run(f'python -c \"{lines}\"', capture_output=True, text=True, shell=True) 
      await message.channel.send(f"<@{message.author.id}> \n Output : \n{run.stdout} \n")
      await message.channel.send(f"<@{message.author.id}> \n Error : \n{run.stderr} \n")
    except Exception as e:
      await message.channel.send(f"Exception Occurs : {e}")


if __name__ == "__main__":
    client.run(os.getenv('TOKEN')) 

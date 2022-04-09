from time import time
from src.Pomodoro.Pomodoro import show_time, startTimer, stopTimer, Timer
import os 
from dotenv import load_dotenv
import discord
from src.Todo.Todo import get_tasks, getEmbededTasks, perform_crd_tasks
load_dotenv()

# client = commands.Bot(command_prefix='!', help_command=None)
# client.add_cog(DiscordCog(client))
# client.run(os.getenv('TOKEN'))

client = discord.Client()

timer = Timer()

@client.event
async def on_ready():
    print("Logged in")

@client.event
async def on_message(message):
    if message.author == client.user:
        return 
    
@client.event
async def on_message(message):
  global msg
  msg = message
  if message.author == client.user : 
    return

#   if str(message.channel) == channel and message.content.startswith("#python3"):
  if message.content.startswith("#python3"):
    await message.channel.send('Python bot')
    print(message.content)  
    f = open("demo.txt", "w")
    f.write(message.content)
    f.close()
    f = open("demo.txt",'r')
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


    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$todo'):
        response = perform_crd_tasks(message)
        if(response):
            await message.channel.send(response)
        tasks = get_tasks(message.author.name)
        taskEmbed = getEmbededTasks(message, tasks)
        await message.channel.send(embed=taskEmbed)

    if message.content.startswith('$timer'):
        cmd = message.content.split(" ")
        print(cmd)
        if cmd[1] == "-start":
            print("here")
            await startTimer(message, timer)
        elif cmd[1] == "-stop":
            await stopTimer(message, timer)
        elif cmd[1] == "-show":
            await show_time(message, timer)

client.run(os.getenv('TOKEN'))

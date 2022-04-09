from operator import index
from ..db import getDBReference
import discord

def add_to_db(username, title, end_date):
    print(username)
    ref = getDBReference(username + '/Tasks')
    ref.child(title).set({"Title":title, "Deadline":end_date})

def remove_from_db(username, title):
    ref = getDBReference(username  + '/Tasks/'+title)
    ref.delete()

def update_in_db(username, title, new_end_date):
    ref = getDBReference(username  + '/Tasks')
    ref.child(title).set({"Title":title, "Deadline":new_end_date})

def get_tasks(username):
    ref = getDBReference(username + '/Tasks')
    ans = ref.get()
    return ans

def getEmbededTasks(message, tasks):
    embed = discord.Embed(title="Todo List", description="You have got a lot of work to do!", color=0x109319)
    embed.set_author(name=message.author.name)

    i = 1

    titles = ''
    deadlines = ''
    indexes = ''

    for task in tasks:
        indexes = indexes + str(i)+"\n"
        titles = titles + task + "\n"
        deadlines = deadlines + tasks[task]['Deadline']+"\n"
        i += 1

    embed.add_field(name="Sr.", value=indexes, inline=True)
    embed.add_field(name="Title", value=titles, inline=True)
    embed.add_field(name="Deadline", value=deadlines, inline=True)

    embed.set_footer(text="You are super cool!!")
    return embed

def perform_crd_tasks(message):
    msg = message.content
    msg = msg.split(" ")
    if msg[1] == '-add':
        title = msg[2]
        p2 = msg[3]
        add_to_db(message.author.name, title, p2)
        return 'Task Added!'
    elif msg[1] == '-update':
        title = msg[2]
        p2 = msg[3]
        update_in_db(message.author.name, title, p2)
        return 'Task Updated!'
    elif msg[1] == '-delete':
        title = msg[2]
        remove_from_db(message.author.name, title)
        return 'Task Removed!'
        
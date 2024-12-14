import datetime
from http.client import responses

import discord
from discord.ext import commands, tasks

from DataBaseCommands import get_class, fetch_seminars
from botcommands import add_class
from utils import *
import DataBaseCommands as db
import asyncio
import re
import botcommands
import unicodedata
from html import unescape
# Initialize the bot with a command prefix (e.g., "!")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
@bot.command(name="UstawKolo")
async def add_class(ctx):
    await botcommands.add_class(ctx, bot)

@bot.command(name="Kola")
async def print_classes(ctx):
    kola =  db.get_class()
    i=0;
    response=""
    for kolo in kola:
        i+=1
        response+=f"{i}: Kolo z {kolo.type_str}: \n Data: {kolo.date} w godzinach: {kolo.time} \n {kolo.theme} \n {kolo.description} \n"
        if i>5:
            break
    if response=="":
        response="Nie ma zaplanowanych kół"
    await ctx.send( unicodedata.normalize('NFKC',unescape(response)))
@bot.command(name="MojeKola")
async def print_custom_classes(ctx):
    kola = db.get_class()
    i = 0
    response = ""
    for kolo in kola:
        if user_class_match(kolo.type,ctx.author.roles):
            i += 1
            response+=f"{i}: Kolo z {kolo.type_str}: \n Data: {kolo.date} w godzinach: {kolo.time} \n {kolo.theme} \n {kolo.description} \n"
            if (i > 5):
                break
    if response=="":
        response="Nie ma zaplanowanych kół dla twoich ról"
    await ctx.send( unicodedata.normalize('NFKC',unescape(response)))
@bot.command(name="Grupy")
async def print_groups(ctx):
    groups =  db.get_groups()
    i=0

    for group in groups:
        i+=1
        response = unicodedata.normalize('NFKC',unescape(f"{i}: Grupa {group.name}:\n {group.description} \n"))
        await ctx.send(response)
@tasks.loop(seconds=15)
async def hourly_task():
    print(f'Bot is ready. Logged in as {bot.user}')
    date = datetime.date.today()
    time = datetime.datetime.now().now()
    hours= str(time)[:2]
    print(hours)
    seminars = db.get_class(exact_date=date)
    for seminar in seminars:
        seminar_hours = seminar.time[:2]
        if abs(int(hours)-int(seminar_hours))<2 and not seminar.started:
            print(seminar.theme)
            db.start_class(seminar)


@bot.event
async def on_ready():
    if not hourly_task.is_running():
        hourly_task.start()

# Run the bot using your token (replace 'your_token' with the actual bot token)
token = open("token.txt","r").readline()
bot.run(token)
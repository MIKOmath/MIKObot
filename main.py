from http.client import responses

import discord
from discord.ext import commands, tasks

from DataBaseCommands import get_class
from botcommands import add_class
from utils import *
import DataBaseCommands as db
import asyncio
import re
import botcommands
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
    await ctx.send(response)
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
    await ctx.send(response)
@bot.command(name="NoweZadanie")
async def new_problem(ctx):
    await botcommands.new_problem(ctx,bot)



@tasks.loop(hours=1)
async def hourly_task():
    print(f'Bot is ready. Logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

        # Log the received message content
    print(f"Received message: {message.content}")
    # Important: Process commands after custom logic
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    #todo w zależności od kontentu wiadomości różne punkty
    print(reaction.message.content)


@bot.command()
async def ping(ctx):
    await ctx.send(f'pong {ctx.author.name}!')

# Run the bot using your token (replace 'your_token' with the actual bot token)
token = open("token.txt","r").readline()
bot.run(token)
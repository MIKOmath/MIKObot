import discord
from discord.ext import commands, tasks
import DataBaseCommands as db


# Initialize the bot with a command prefix (e.g., "!")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready(): #synchornizujemy bazę danych po restarcie
    print(f'Bot is ready. Logged in as {bot.user}')
    guild = bot.guilds[0]
    for i in bot.guilds:
        if i.name=='testowanie bota':
            guild = i
            print(guild)
    members = guild.members
    db.connect_database()
    db.sync_members(members)
    hourly_task.start()

@tasks.loop(hours=1)
async def hourly_task():
    print(f'Bot is ready. Logged in as {bot.user}')
    guild = bot.guilds[0]
    for i in bot.guilds:
        if i.name == 'testowanie bota':
            guild = i
            print(guild)
    members = guild.members
    db.sync_members(members)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

        # Log the received message content
    print(f"Received message: {message.content}")
    db.add_point(message.author,1)
    # Important: Process commands after custom logic
    await bot.process_commands(message)
@bot.event
async def on_reaction_add(reaction, user):
    #todo w zależności od kontentu wiadomości różne punkty
    db.add_point(reaction.message.author,1)
@bot.event
async def on_reaction_remove(reaction, user):
    db.add_point(reaction.message.author,-1)
@bot.event
async def on_member_join(member):
    db.add_member(member)
@bot.event
async def on_member_remove(member):
    db.remove_member(member)


@bot.command()
async def ping(ctx):
    await ctx.send(f'pong {ctx.author.name}!')

# Run the bot using your token (replace 'your_token' with the actual bot token)
token = open("token.txt","r").readline()
bot.run(token)
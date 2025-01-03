import discord
from aiohttp.helpers import method_must_be_empty_body
from discord.ext import commands, tasks
from utils import *
import DataBaseCommands as db
import asyncio
import re

async def add_class(ctx, bot):
    """
    command to add discord class to schedue
    """
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel


    is_mod=False
    for role in ctx.author.roles:
        if role.name == "BotMod":
            is_mod=True


    if is_mod:
        # Step 1: Ask for the Class day
        await ctx.send("Kiedy będzie koło?(podaj odpowiedź w formacie RRRR-MM-DD)")
        try:
            while True:
                meeting_date = await bot.wait_for("message", check=check, timeout=30.0)
                pattern = r"\d{4}\-\d{2}\-\d{2}"
                if re.fullmatch(pattern, meeting_date.content):
                    if int(meeting_date.content[5:7])<13 and int(meeting_date.content[8:10])<32:
                        break
                    else:
                        await ctx.send("Podaj poprawną datę")
                else:
                    await ctx.send("Podaj poprawną datę")
        except asyncio.TimeoutError:
            await ctx.send("timeout")
            return
        # Step 2: Ask for the Class time
        await ctx.send("I od której do której? (HH:MM-HH:MM)")
        try:
            while True:
                meeting_time = await bot.wait_for("message", check=check, timeout=30.0)
                pattern = r"\d{2}\:\d{2}\-\d{2}\:\d{2}"
                if re.fullmatch(pattern, meeting_time.content):
                    if int(meeting_time.content[0:2]) < 24 and int(meeting_time.content[3:5]) < 60 and int(meeting_time.content[6:8]) < 24 and int(meeting_time.content[9:11]) < 60:
                        break
                    else:
                        await ctx.send("Podaj poprawny czas")
                else:
                    await ctx.send("Podaj poprawną datę")
        except asyncio.TimeoutError:
            await ctx.send("timeout")
            return
        # Step 2: Ask for the Class type

        await ctx.send("Jakie koło: 0 - Matma początkująca, 1 - Matma średnia, 2- Matma finał++, 3-AI, 4-Fiza, 5-Infa")

        try:
            while True:
                meeting_type = await bot.wait_for("message", check=check, timeout=30.0)
                pattern = r"\d{1}"
                if re.fullmatch(pattern, meeting_type.content):
                    if int(meeting_type.content[0])<6:
                        break
                    else:
                        await ctx.send("Podaj poprawny Typ")
                else:
                    await ctx.send("Podaj poprawny typ")
        except asyncio.TimeoutError:
            await ctx.send("timeout")
            return

        # Step 3: Ask for any additional notes
        await ctx.send("Kto prowadzi?")
        try:

            meeting_host = await bot.wait_for("message", check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("timeout")
            return

        await ctx.send("Jakiś opis kurcze ten?")
        try:
            meeting_description = await bot.wait_for("message", check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send("timeout")
            return

        # Summarize the meeting details
        await ctx.send(f"Kółko ustawione")
        kolo = ClassMeet()
        kolo.load_from_discord(meeting_type.content,meeting_date.content,meeting_time.content,meeting_host.content,meeting_description.content)
        db.add_class(kolo)
    else:
        await ctx.send(f"You are not worthy, {ctx.author.mention}")

async def new_problem(ctx,bot):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    await ctx.send("Podaj treść zadania: ")
    try:
        problem_statement = await bot.wait_for("message", check=check, timeout=600.0)
        statement_text = problem_statement.content
        while (True):
            msg = await ctx.send("Jeśli to cała treść, napisz \"koniec\". Jeśli nie pisz dalej")
            problem_statement_ = await bot.wait_for("message", check=check, timeout=600.0)
            if problem_statement_.content == 'koniec':
                await msg.delete()
                await problem_statement_.delete()
                break
            statement_text += "\n" + problem_statement_.content
            await msg.delete()
    except asyncio.TimeoutError:
        return
    await ctx.send("Jeśli masz solva, wpisz go tutaj (koniecznie z spoiler tagiem!), jeśli nie odpisz: \"nie\"")
    try:
        problem_solve = await bot.wait_for("message", check=check, timeout=600.0)
        solve_text = ""
        if not (problem_solve.content == 'nie'):
            solve_text = problem_solve.content
            while (True):
                msg = await ctx.send("Jeśli to cały solve, napisz \"koniec\". Jeśli nie pisz dalej")
                problem_solve_ = await bot.wait_for("message", check=check, timeout=600.0)
                if problem_solve_.content == 'koniec':
                    await msg.delete()
                    await problem_solve_.delete()
                    break
                solve_text += "\n" + problem_solve_.content
                await msg.delete()
    except asyncio.TimeoutError:
        await ctx.send("Spoko")
        return
    await ctx.send("Jeśli masz tagi (np. Geometria) napisz je:")
    try:
        tagi = await bot.wait_for("message", check=check, timeout=600.0)
    except asyncio.TimeoutError:
        await ctx.send("Spoko")
        return
    ID = db.create_problem(statement_text, solve_text, tags=tagi.content)
    await ctx.send(f"Dodano zadanie o ID: {ID}")


import os
from aiohttp.client_exceptions import ClientResponseError
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Literal

from babel.dates import format_datetime

import discord
from discord import app_commands
from discord.ext import commands

from utils.models import Seminar


class SeminarCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = bot.api

    async def _short_seminar_description(self, seminar: Seminar):
        time_format = lambda t: format_datetime(t, 'HH:mm', locale=os.getenv('LOCALE'))
        featured_icon = ':star:' if seminar.featured else ''
        special_guest_icon = ':bust_in_silhouette:' if seminar.special_guest else ''
        group = f'<@&{seminar.group_role_id}>' if seminar.group_role_id else seminar.group_name or ''
        tutors = f'Prowadzący: {', '.join(seminar.tutors)}' if seminar.tutors else ''

        line1 = f'`{time_format(seminar.start)}` **{seminar.theme}** {featured_icon}{special_guest_icon}'
        line2 = f' {group}{tutors}'

        return f'{line1}\n{line2.strip(' ')}' if not line2.isspace() else line1

    @app_commands.command(name='upcoming', description='Wyświetl nadchodzące zajęcia')
    async def upcoming(self, interaction: discord.Interaction, filter: Literal['all', 'my'] = 'all'):
        seminars = await self.api.fetch_seminars(start_date=datetime.now().date(),
                                                 end_date=(datetime.now() + timedelta(weeks=2)).date())
        if filter == 'my':
            user_role_ids = [str(role.id) for role in interaction.user.roles]
            seminars = [seminar for seminar in seminars if seminar.group_role_id in user_role_ids]

        seminars_by_day = defaultdict(list)
        for seminar in seminars:
            seminars_by_day[seminar.start.date()].append(seminar)

        title = 'Nadchodzące zajęcia:' if filter == 'all' else 'Nadchodzące zajęcia dla Ciebie:'
        embed = discord.Embed(title=title, color=int(os.getenv('MIKO_BLUE'), 16))

        date_format = lambda d: format_datetime(d, 'EEEE, d MMMM:', locale=os.getenv('LOCALE'))

        for date, seminars in sorted(seminars_by_day.items())[:5]:
            formatted_seminars = '\n'.join([
                await self._short_seminar_description(seminar)
                for seminar in sorted(seminars, key=lambda s: s.start)
            ])
            embed.add_field(name=date_format(date), value=formatted_seminars, inline=False)

        if not embed.fields:
            embed.description = 'Brak eventów :sob: \nSprawdź ponownie później.'

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='seminar', description='Wyświetl szczegóły zajęć')
    async def seminar(self, interaction: discord.Interaction, seminar_id: int):
        try:
            seminar = await self.api.fetch_seminar(seminar_id)
        except ClientResponseError as e:
            if e.status == 404:
                embed = discord.Embed(title='Nie istnieje!',
                                      description='Nie znaleziono zajęć o takim ID :anguished:',
                                      color=int(os.getenv('MIKO_RED'), 16))
                return await interaction.response.send_message(embed=embed, ephemeral=True)
            raise

        embed = discord.Embed(title=seminar.theme, color=int(os.getenv('MIKO_BLUE'), 16))
        embed.add_field(name='Data i godzina', value=format_datetime(seminar.start, 'd MMMM HH:MM', locale=os.getenv('LOCALE')))
        embed.add_field(name='Trudność', value=seminar.difficulty_label)
        embed.add_field(name='Opis', value=seminar.description, inline=False)
        if seminar.tutors:
            embed.add_field(name='Prowadzący', value=', '.join(seminar.tutors), inline=False)

        await interaction.response.send_message(embed=embed)

    async def cog_app_command_error(self, interaction, error):
        if isinstance(error, app_commands.CommandInvokeError) and isinstance(error.original, ClientResponseError):
            embed = discord.Embed(title='Okropny błąd!',
                                  description=f'Chwilowo nie mam dostępu do danych (`{error.original.status}`). Spróbuj ponownie później lub samodzielnie sprawdź na [stronie internetowej](https://mikomath.org/kolo).',
                                  color=int(os.getenv('MIKO_RED'), 16))
            embed.set_author(name='mikomath.org/kolo', url='https://mikomath.org/kolo')
            return await interaction.response.send_message(embed=embed)
        else:
            raise error


async def setup(bot):
    await bot.add_cog(SeminarCommands(bot), guild=bot.guild)

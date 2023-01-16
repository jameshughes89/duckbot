import asyncio
import random

import discord
import requests
from discord import ChannelType, Client, TextChannel
from discord.ext import commands, tasks

from duckbot.util.datetime import now

from .phrases import phrases


class Posture(commands.Cog):
    def __init__(self, bot: Client):
        self.bot = bot
        self.on_hour_loop.start()

    @on_hour_loop.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()

    @tasks.loop(hours=1.0)
    async def on_hour_loop(self):
        await self.on_hour()

    def cog_unload(self):
        self.on_hour_loop.cancel()

    def should_send_posture_check(self):
        current_time_probability = 1 / (23 - now().hour)  # Get more likely to send as the day goes
        return 10 <= now().hour < 23 and random.random() < current_time_probability

    async def posture_check(self):
        if self.should_send_posture_check():
            self.on_hour_loop.cancel()
            channel = get(self.bot.get_all_channels(), guild__name="Friends Chat", name="general", type=ChannelType.text)
            message = random.choice(phrases)
            await channel.send(message)

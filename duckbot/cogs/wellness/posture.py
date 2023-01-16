import asyncio
import random

import discord
import requests
from discord import ChannelType, Client, TextChannel
from discord.ext import commands, tasks

from .phrases import phrases

class Wellness(commands.Cog):
    def __init__(self, bot: Client):
        self.bot = bot


    def posture_check(self):
        if SEND_NOW?:
            channel = get(self.bot.get_all_channels(), guild__name="Friends Chat", name="general", type=ChannelType.text)
            message = random.choice(phrases)
            await channel.send(message)


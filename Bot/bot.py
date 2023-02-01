import aiosqlite
import discord
from discord.ext import commands

from utils.log import setup_logger


class DragonBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.set_up = False
        super().__init__(*args, **kwargs)


    async def on_ready(self):
        if not self.set_up:
            self.log = setup_logger()

import logging

import discord
from discord.ext import commands
import mafic

from DragonBot import DragonBot
from utils import db


class MaficEventsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener("on_track_start")
    async def on_track_start(self, event: mafic.TrackStartEvent):
        print(event)

    @commands.Cog.listener("on_track_end")
    async def on_track_end(self, event: mafic.TrackEndEvent):
        print(event)


def setup(client: DragonBot):
    client.add_cog(MaficEventsCog(client))

import logging

import pomice
import discord
from discord.ext import commands

from DragonBot import DragonBot
from music.DragonPlayer import DragonPlayer
from utils import db, utils


class PomiceEventCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_pomice_track_start(self, player: DragonPlayer, track: pomice.Track):
        await player.update_embed()

    @commands.Cog.listener()
    async def on_pomice_track_end(
        self, player: DragonPlayer, track: pomice.Track, reason: str
    ):
        await player.do_next()

    @commands.Cog.listener()
    async def on_pomice_track_exception(
        self, player: DragonPlayer, error_code, exception
    ):
        print(f"track_exception: {player.guild.name}: {error_code} ({exception})")

    @commands.Cog.listener()
    async def on_pomice_track_stuck(self, player: DragonPlayer, track: pomice.Track):
        print(f"track_stuck: {player.guild.name}: {track.title}")


def setup(client: DragonBot):
    client.add_cog(PomiceEventCog(client))

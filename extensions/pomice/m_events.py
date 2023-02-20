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
        em = discord.Embed(
            title=f"Now playing {track.title}",
            url=track.uri,
            description=f"""
                    By: {track.author}
                    Duration: {utils.sec_to_min(track.length/1000)}
                    """,
            color=discord.Color.blurple(),
        )
        em.set_image(url=track.thumbnail)
        await player.controller.edit(embed=em)

    @commands.Cog.listener()
    async def on_pomice_track_end(
        self, player: DragonPlayer, track: pomice.Track, reason: str
    ):
        await player.do_next()
        print(f"track_end: {player.guild.name}: {track.title}, reason: {reason}")

    @commands.Cog.listener()
    async def on_pomice_track_exception(self, data: dict, player: DragonPlayer):
        print(f"track_exception: {data}")

    @commands.Cog.listener()
    async def on_pomice_track_stuck(self, data: dict, player: DragonPlayer):
        print(f"track_stuck: {data}")


def setup(client: DragonBot):
    client.add_cog(PomiceEventCog(client))

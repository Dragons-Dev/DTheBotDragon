import logging

import discord
from discord.ext import commands
from pycord import multicog

from DragonPlayer.DragonPlayer import DragonPlayer
from DragonBot import DragonBot
from utils import db


class MusicSkipCog(commands.Cog):
    def __init__(self, client):
        self.client: DragonBot = client

    @multicog.add_to_group("music")
    @commands.slash_command(name="skip", description="Skip the currently playing song")
    async def skip_cmd(self, ctx: discord.ApplicationContext):
        if not ctx.voice_client:
            return await ctx.response.send_message(
                "You can't skip a song I am not playing",
                ephemeral=True,
                delete_after=10,
            )
        player: DragonPlayer = ctx.voice_client
        if (
            ctx.author.voice is None
            or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            return await ctx.response.send_message(
                f"You may not skip a song when you are not in the same channel.",
                ephemeral=True,
                delete_after=10,
            )
        await ctx.response.send_message(
            f"Skipped {player.current}", ephemeral=True, delete_after=10
        )
        controller: discord.Message = player.controller
        await controller.channel.send(
            embed=discord.Embed(color=discord.Color.blurple()).set_author(
                name=f"{ctx.author.display_name} skipped {player.current}",
                icon_url=ctx.author.display_avatar.url,
                url=player.current.uri,
            ),
            delete_after=10,
        )
        await player.stop()


def setup(client: DragonBot):
    client.add_cog(MusicSkipCog(client))

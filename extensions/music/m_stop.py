import logging

import discord
from discord.ext import commands
from pycord import multicog

from DragonBot import DragonBot
from DragonPlayer.DragonPlayer import DragonPlayer
from utils import db


class MusicStopCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @multicog.add_to_group("music")
    @commands.slash_command(name="stop", description="Stop the playback entirely")
    async def skip_cmd(self, ctx: discord.ApplicationContext):
        if not ctx.voice_client:
            return await ctx.response.send_message(
                "You can't stop a playback if I am not playing",
                ephemeral=True,
                delete_after=10,
            )
        player: DragonPlayer = ctx.voice_client
        if (
            ctx.author.voice is None
            or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            return await ctx.response.send_message(
                f"You may not stop the player when you are not in the same channel.",
                ephemeral=True,
                delete_after=10,
            )
        await player.teardown()
        await player.controller.channel.send(f"{ctx.author.display_name}#{ctx.author.discriminator} stopped the player.")
        await ctx.response.send_message(
            f"You stopped the player.", ephemeral=True, delete_after=10
        )


def setup(client: DragonBot):
    client.add_cog(MusicStopCog(client))

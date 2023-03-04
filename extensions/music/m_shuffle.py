import logging

import pomice
import discord
from discord.ext import commands
from pycord import multicog

from DragonPlayer.DragonPlayer import DragonPlayer
from DragonBot import DragonBot
from utils import db


class ShuffleCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @multicog.add_to_group("music")
    @commands.slash_command(name="shuffle", description="Shuffle the queue")
    async def shuffle(self, ctx: discord.ApplicationContext) -> None:
        if not ctx.voice_client:
            return await ctx.response.send_message(
                "You can't shuffle the queue if I am not playing",
                ephemeral=True,
                delete_after=10,
            )
        player: DragonPlayer = ctx.voice_client
        if (
            ctx.author.voice is None
            or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            return await ctx.response.send_message(
                f"You may not shuffle the queue when you are not in the same channel.",
                ephemeral=True,
                delete_after=10,
            )

        player.queue.shuffle()

        await ctx.response.send_message(
            f"Shuffled the queue", ephemeral=True, delete_after=10
        )
        controller: discord.Message = player.controller
        await controller.channel.send(
            embed=discord.Embed(color=discord.Color.blurple()).set_author(
                name=f"{ctx.author.display_name} shuffled the queue",
                icon_url=ctx.author.display_avatar.url,
            ),
            delete_after=10,
        )


def setup(client: DragonBot):
    client.add_cog(ShuffleCog(client))

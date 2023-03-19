import logging

import discord
from discord.ext import commands
from pycord import multicog

from DragonBot import DragonBot
from DragonPlayer.DragonPlayer import DragonPlayer
from utils import db


class MusicVolumeCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @multicog.add_to_group("music")
    @commands.slash_command(
        name="set_volume", description="Set's the volume to a desired number"
    )
    async def volume_cmd(
        self,
        ctx: discord.ApplicationContext,
        volume: discord.Option(int, description="Set your desired volume"),
    ):
        if not ctx.voice_client:
            return await ctx.response.send_message(
                "You can't change the volume if I am not playing",
                ephemeral=True,
                delete_after=10,
            )
        player: DragonPlayer = ctx.voice_client
        if (
            ctx.author.voice is None
            or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            return await ctx.response.send_message(
                f"You may not change the volume when you are not in the same channel.",
                ephemeral=True,
                delete_after=10,
            )
        try:
            vol = int(volume)
        except ValueError:
            return await ctx.response.send_message(
                "You may not use anything else than numbers between 0 and 500",
                delete_after=10,
                ephemeral=True,
            )
        if not 0 < vol < 501:
            return await ctx.response.send_message(
                "You may not use anything else than numbers between 0 and 500",
                delete_after=10,
                ephemeral=True,
            )
        await player.set_volume(vol)
        return await ctx.response.send_message(
            f"You've set the volume to {vol}", delete_after=10, ephemeral=True
        )


def setup(client: DragonBot):
    client.add_cog(MusicVolumeCog(client))

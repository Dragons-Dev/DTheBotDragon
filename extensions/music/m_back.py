import logging

import discord
from discord.ext import commands
import pomice
from pycord import multicog

from DragonPlayer.DragonPlayer import DragonPlayer
from DragonBot import DragonBot
from utils import db


class TrackBackCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @multicog.add_to_group("music")
    @commands.slash_command(name = "back", description = "Play the previous song")
    async def track_back(self, ctx: discord.ApplicationContext):
        if not ctx.voice_client:
            return await ctx.response.send_message(
                "You can't go back a track if I am not playing",
                ephemeral=True,
                delete_after=10,
            )
        player: DragonPlayer = ctx.voice_client
        if (
            ctx.author.voice is None
            or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            return await ctx.response.send_message(
                f"You may not go back a track when you are not in the same channel.",
                ephemeral=True,
                delete_after=10,
            )

        if len(player.queue.history) == 0:
            await ctx.response.send_message(
                f"No song in history!", ephemeral = True, delete_after = 10
            )

        current = player.current
        track = (player.queue.history.pop(-1) if player.queue.last_track is None else player.queue.history.pop(-2))
        player.queue.put_at_front(current)
        player.queue.put_at_front(track)
        await player.stop()

        await ctx.response.send_message(
            f"You went back to {track}", ephemeral = True, delete_after = 10
        )
        controller: discord.Message = player.controller
        await controller.channel.send(
            embed = discord.Embed(color = discord.Color.blurple()).set_author(
                name = f"{ctx.author.display_name} went back to {track}",
                icon_url = ctx.author.display_avatar.url,
            ),
            delete_after = 10,
        )


def setup(client: DragonBot):
    client.add_cog(TrackBackCog(client))

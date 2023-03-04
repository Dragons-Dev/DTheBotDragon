import logging

import discord
import pomice
from discord.ext import commands
from pycord import multicog

from DragonPlayer.DragonPlayer import DragonPlayer
from DragonBot import DragonBot
from utils import db


log = logging.getLogger("DragonLog")


class LoopCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @multicog.add_to_group("music")
    @commands.slash_command(
        name="loop", description="Sets a loop for the current queue"
    )
    async def loop_cmd(
        self,
        ctx: discord.ApplicationContext,
        loop_mode: discord.Option(
            str,
            choices=[
                discord.OptionChoice("Off"),
                discord.OptionChoice("Track"),
                discord.OptionChoice("Queue"),
            ],
        ),
    ):
        if not ctx.voice_client:
            return await ctx.response.send_message(
                "You can't set a loop when I am not playing a song!",
                ephemeral=True,
                delete_after=10,
            )
        player: DragonPlayer = ctx.voice_client
        if (
            ctx.author.voice is None
            or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            return await ctx.response.send_message(
                f"You may not loop the queue when you are not in the same channel.",
                ephemeral=True,
                delete_after=10,
            )
        if loop_mode == "Off":
            player.queue.disable_loop()
            return await ctx.response.send_message(
                f"Loop mode set to off",
                ephemeral=True,
                delete_after=10,
            )
        if loop_mode == "Track":
            player.queue.set_loop_mode(pomice.LoopMode.TRACK)
            return await ctx.response.send_message(
                f"Loop mode set to Track",
                ephemeral=True,
                delete_after=10,
            )
        if loop_mode == "Queue":
            player.queue.set_loop_mode(pomice.LoopMode.QUEUE)
            return await ctx.response.send_message(
                f"Loop mode set to Queue",
                ephemeral=True,
                delete_after=10,
            )
        else:
            log.critical("Invalid loop mode set!")


def setup(client: DragonBot):
    client.add_cog(LoopCog(client))

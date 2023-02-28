import logging

import pomice
import discord
from discord.ext import commands
from pycord import multicog

from DragonPlayer.DragonPlayer import DragonPlayer
from DragonBot import DragonBot
from utils import db


async def autocomplete(ctx: discord.AutocompleteContext):
    if not ctx.interaction.guild.voice_client:
        return "You can't remove a track from the queue if I am not playing"
    if (
        ctx.interaction.user.voice is None
        or ctx.interaction.user.voice.channel
        != ctx.interaction.guild.voice_client.channel
    ):
        return "You may not remove a track from the queue when you are not in the same channel."
    player: DragonPlayer = ctx.interaction.guild.voice_client
    queue: list[pomice.Track] = player.queue.get_queue()
    return [track.title for track in queue]


class DeleteCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @multicog.add_to_group("music")
    @commands.slash_command(
        name="remove_track", description="Remove a track from the queue"
    )
    async def shuffle(
        self,
        ctx: discord.ApplicationContext,
        track: discord.Option(
            description="Show's tracks in the queue to delete one",
            autocomplete=autocomplete,
        ),
    ) -> None:
        if not ctx.voice_client:
            return await ctx.response.send_message(
                "You can't remove a track from the queue if I am not playing",
                ephemeral=True,
                delete_after=10,
            )
        player: DragonPlayer = ctx.voice_client
        if (
            ctx.author.voice is None
            or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            return await ctx.response.send_message(
                f"You may not remove a track from the queue when you are not in the same channel.",
                ephemeral=True,
                delete_after=10,
            )

        queue: list[pomice.Track] = player.queue.get_queue()
        for t in queue:
            if t.title == track:
                player.queue.remove(t)
                break
        else:
            await ctx.response.send_message(
                f"Couldn't find {track} in queue please contact DTheIcyDragon#1214 on discord",
                ephemeral=True,
                delete_after=10,
            )

        await ctx.response.send_message(
            f"You removed {track} from the queue", ephemeral=True, delete_after=10
        )
        controller: discord.Message = player.controller
        await controller.channel.send(
            embed=discord.Embed(color=discord.Color.blurple()).set_author(
                name=f"{ctx.author.display_name} removed {track} from the queue",
                icon_url=ctx.author.display_avatar.url,
            ),
            delete_after=10,
        )


def setup(client: DragonBot):
    client.add_cog(DeleteCog(client))

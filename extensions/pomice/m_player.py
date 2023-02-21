import logging

import pomice
import discord
from discord.ext import commands

from DragonBot import DragonBot
from music.DragonPlayer import DragonPlayer
from utils import db, utils


class PlayerCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="join", aliases=["connect"])
    async def join(
        self, ctx: commands.Context, *, channel: discord.TextChannel = None
    ) -> None:
        if not channel:
            channel = getattr(ctx.author.voice, "channel", None)
            if not channel:
                raise commands.CheckFailure(
                    "You must be in a voice channel to use this command"
                    "without specifying the channel argument."
                )

        await ctx.author.voice.channel.connect(cls=DragonPlayer)
        await ctx.send(f"Joined the voice channel `{channel}`")

    @commands.command(name="play")
    async def play(self, ctx: commands.Context, *, search: str) -> None:
        if not ctx.voice_client:
            await ctx.invoke(self.join)

        player: DragonPlayer = ctx.voice_client
        await player.set_context(ctx)
        msg = await ctx.send(
            embed=discord.Embed(
                title=f"Searching for {search}...", color=discord.Color.blurple()
            )
        )
        results = await player.get_tracks(query=f"{search}", ctx=ctx)
        if player.controller is None:
            player.controller = msg
        else:
            await msg.delete(delay=5)

        if not results:
            raise commands.CommandError("No results were found for that search term.")

        if isinstance(results, pomice.Playlist):
            player.queue.extend(results.tracks)
            if not player.is_playing:
                await player.do_next()
        else:
            track = results[0]
            player.queue.put(track)
            if not player.is_playing:
                await player.do_next()


def setup(client: DragonBot):
    client.add_cog(PlayerCog(client))

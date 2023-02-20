import logging

import pomice
import discord
from discord.ext import commands

from DragonBot import DragonBot
from music.DragonPlayer import DragonPlayer
from utils import db


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
    async def play(self, ctx, *, search: str) -> None:
        if not ctx.voice_client:
            await ctx.invoke(self.join)

        player: DragonPlayer = ctx.voice_client
        await player.set_context(ctx)
        results = await player.get_tracks(query=f"{search}")

        msg = await ctx.send(f"Searching for {search}...")
        player.controller = msg

        if not results:
            raise commands.CommandError("No results were found for that search term.")

        if isinstance(results, pomice.Playlist):
            for track in results.tracks:
                track.requester = ctx.author
                player.queue.put(track)
            if not player.is_playing:
                await player.do_next()
        else:
            track = results[0]
            track.requester = ctx.author
            player.queue.put(track)
            if not player.is_playing:
                await player.do_next()


def setup(client: DragonBot):
    client.add_cog(PlayerCog(client))

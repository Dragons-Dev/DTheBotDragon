import logging

import pomice
import discord
from discord.ext import commands

from DragonBot import DragonBot
from music.DragonPlayer import DragonPlayer
from utils import db, utils


class PlayerCog(commands.Cog):
    def __init__(self, client):
        self.client: DragonBot = client

    @commands.slash_command(name="play", description="Play a song you want to play.")
    async def play(
        self,
        ctx: discord.ApplicationContext,
        search: discord.Option(
            description="Just type what song you want to play and I will search it."
        ),
    ) -> None:
        responded = False
        if not ctx.voice_client:
            channel = getattr(ctx.user.voice, "channel", None)
            if not channel:
                raise commands.CheckFailure(
                    "You must be in a voice channel to use this command"
                    "without specifying the channel argument."
                )

            await ctx.author.voice.channel.connect(cls=DragonPlayer)
            await ctx.response.send_message(
                f"Joined the voice channel `{channel}`", delete_after=10
            )
            responded = True

        player: DragonPlayer = ctx.voice_client
        await self.client.ws.voice_state(
            guild_id=ctx.guild_id,
            channel_id=ctx.voice_client.channel.id,
            self_deaf=True,
        )

        await player.set_context(ctx)
        search_em = discord.Embed(
            title=f"Searching for {search}...", color=discord.Color.blurple()
        )
        if responded:
            msg = await ctx.send(embed=search_em)
        else:
            msg = await ctx.response.send_message(embed=search_em)
        results = await player.get_tracks(query=f"{search}", ctx=ctx)
        if player.controller is None:
            if responded:
                player.controller = msg
            else:
                player.controller = msg.message
        else:
            if responded:
                await msg.delete(delay=5)
            else:
                await msg.delete_original_response(delay=5)

        if not results:
            raise commands.CommandError("No results were found for that search term.")

        if isinstance(results, pomice.Playlist):
            player.queue.extend(results.tracks)
            await player.update_embed()
            if not player.is_playing:
                await player.do_next()
        else:
            track = results[0]
            player.queue.put(track)
            await player.update_embed()
            if not player.is_playing:
                await player.do_next()


def setup(client: DragonBot):
    client.add_cog(PlayerCog(client))

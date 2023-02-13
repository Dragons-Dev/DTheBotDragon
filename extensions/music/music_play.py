import logging

import wavelink
import discord
from discord.ext import commands

from DragonBot import DragonBot
from utils import db, utils


async def get_colors(ctx: discord.AutocompleteContext):
    """Returns a list of search results with the given input"""

    results = await wavelink.YouTubeTrack.search(ctx.value, return_first = False)
    print(results)
    return [track.title for track in results[:5]]


class MusicPlay(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name = "play", description = "Play a song of your desire")
    async def music_play(self,
                         ctx: discord.ApplicationContext,
                         request: discord.Option(
                             str,
                             description = "request to search for a song",
                             autocomplete = get_colors
                         )):
        vc: wavelink.Player = ctx.guild.voice_client

        if not vc:
            vc = await ctx.user.voice.channel.connect(cls = wavelink.Player())

        track = await wavelink.YouTubeTrack.search(request, return_first = True)

        em = discord.Embed(
            title = f"Now playing {track.title}",
            url = track.uri,
            description = f"""
            By: {track.author}
            Duration: {utils.sec_to_min(track.length)}
            """,
            color = discord.Color.blurple(),
        )
        em.set_image(url = track.thumbnail)
        if vc.is_playing():
            await vc.queue.put_wait(track)
        else:
            await vc.queue.put_wait(track)
            track = vc.queue.get()
            await vc.play(track)
        await ctx.response.send_message(embed = em)


def setup(client: DragonBot):
    client.add_cog(MusicPlay(client))

import logging
import datetime

import wavelink
import discord
from discord.ext import commands

from DragonBot import DragonBot
from utils import db, utils


async def play_generator(ctx: discord.AutocompleteContext):
    """Returns a list of search results with the given input"""

    results = await wavelink.YouTubeTrack.search(ctx.value, return_first = False)
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
                             autocomplete = play_generator
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
        await ctx.response.send_message(embed = em, delete_after = 10)
        # generate new panel view
        message_id = await db.get_setting(setting = "music_panel",
                                          guild = ctx.guild.id)
        channel_id = await db.get_setting(setting = "music_panel_channel",
                                          guild = ctx.guild.id)

        msg = await utils.fetch_or_get_message(client = self.client,
                                               message_id = int(message_id[0]),
                                               channel_id = int(channel_id[0]))
        embed = discord.Embed.from_dict(msg.embeds[0].to_dict())
        try:
            embed.clear_fields()
            queue = vc.queue.copy()
            duration_upcoming = vc.queue.copy()
            total_duration = 0
            for track in duration_upcoming:
                total_duration += track.duration
            total_duration += track.duration
            embed.set_footer(text = f"Total duration: {utils.sec_to_min(total_duration)}")
            i = 0
            for next_track in queue:
                i += 1
                embed.add_field(
                    name = f"{i}. in queue",
                    value = f"[{next_track.title}]({next_track.uri})\n-> {next_track.author} :notes:\n-> {utils.sec_to_min(next_track.length)}  :hourglass_flowing_sand:",
                    inline = False,
                )
                if i >= 5:
                    break
            queue = None
        except wavelink.QueueEmpty:
            pass
        except AttributeError:
            pass
        await msg.edit(embed = embed)


def setup(client: DragonBot):
    client.add_cog(MusicPlay(client))

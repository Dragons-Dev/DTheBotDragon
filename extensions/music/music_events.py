import logging
import datetime

import wavelink
import discord
from discord.ext import commands, tasks

from utils import utils
from DragonBot import DragonBot
from utils import db


log = logging.getLogger("DragonLog")


async def edit_panel(vc: wavelink.Player):
    track: wavelink.YouTubeTrack = vc.track
    msg_id_db = await db.get_setting(setting = "music_panel", guild = vc.guild.id)
    channel_id_db = await db.get_setting(setting = "music_panel_channel", guild = vc.guild.id)
    channel_id = int(channel_id_db[0])
    msg_id = int(msg_id_db[0])
    panel = await utils.fetch_or_get_message(client=vc.client, message_id=msg_id, channel_id=channel_id)
    if track is None:
        embed = discord.Embed(
            title="Nothing left to play",
            description="Add new tracks by writing their name into this channel!",
            color=discord.Color.blurple(),
        )
        embed.clear_fields()
    else:
        embed = discord.Embed(
            title=f"Now playing {track.title}",
            description=f"**By: {track.author}\nDuration: {utils.sec_to_min(track.length)}**",
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.now(),
            url=track.uri,
        )
    try:
        embed.set_image(url=track.thumbnail)
    except AttributeError:
        pass
    try:
        queue = vc.queue.copy()
        duration_upcoming = vc.queue.copy()
        total_duration = 0
        for track in duration_upcoming:
            total_duration += track.duration
        total_duration += track.duration
        embed.set_footer(text=f"Total duration: {utils.sec_to_min(total_duration)}")
        i = 0
        for next_track in queue:
            i += 1
            embed.add_field(
                name=f"{i}. in queue",
                value=f"[{next_track.title}]({next_track.uri})\n-> {next_track.author} :notes:\n-> {utils.sec_to_min(next_track.length)}  :hourglass_flowing_sand:",
                inline=False,
            )
            if i >= 5:
                break
        queue = None
    except wavelink.QueueEmpty:
        pass
    except AttributeError:
        pass
    await panel.edit(embed=embed)


class MusicEvent(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.players = []
        self.update_panel.start()

    @commands.Cog.listener("on_wavelink_node_ready")
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        log.debug(f"Node {node.host} loaded with {node.identifier} as identifier")

    @tasks.loop(seconds = 20)
    async def update_panel(self):
        for player in self.players:
            await edit_panel(vc = player)

    @update_panel.before_loop
    async def before_panel_update(self):
        await self.client.wait_until_ready()

    @commands.Cog.listener("on_wavelink_track_start")
    async def on_track_start(self, player: wavelink.Player, track: wavelink.Track):
        if player.guild.id not in self.players:
            self.players.append(player)

    @commands.Cog.listener("on_wavelink_track_end")
    async def on_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        try:
            next_track = player.queue.get()
            await player.play(next_track)
        except wavelink.QueueEmpty:
            pass


def setup(client: DragonBot):
    client.add_cog(MusicEvent(client))

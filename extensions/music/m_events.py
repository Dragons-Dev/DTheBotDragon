import logging

import pomice
import discord
from discord.ext import commands

from DragonBot import DragonBot
from DragonPlayer.DragonPlayer import DragonPlayer
from utils import db, utils


log = logging.getLogger("DragonLog")


class MusicEventCog(commands.Cog):
    def __init__(self, client):
        self.client: DragonBot = client

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        if member != self.client.user:
            return
        if member == self.client.user:
            if after is None:
                vc: DragonPlayer = member.guild.voice_client
                await vc.teardown()
                print("teared_down")
            else:
                guild = member.guild
                guild.voice_client.channel = after.channel

    @commands.Cog.listener()
    async def on_pomice_track_start(self, player: DragonPlayer, track: pomice.Track):
        loop_mode = player.queue.loop_mode
        upcoming = []

        if loop_mode is pomice.LoopMode.TRACK:
            upcoming.append(track)

        elif loop_mode is pomice.LoopMode.QUEUE:
            queue = player.queue.get_queue()
            current = player.queue.find_position(track)
            for t in queue:
                walker = player.queue.find_position(t)
                if walker < current:
                    pass
                else:
                    upcoming.append(t)
            if len(upcoming) < 5:
                for missing in range(5 - len(upcoming)):
                    upcoming.append(queue[missing])

        else:
            queue = player.queue.get_queue()
            for i in range(5):
                try:
                    upcoming.append(queue[i])
                except IndexError:
                    break
        await player.update_embed(
            upcoming_tracks=(upcoming if upcoming is not False else None)
        )

    @commands.Cog.listener()
    async def on_pomice_track_end(
        self, player: DragonPlayer, track: pomice.Track, reason: str
    ):
        await player.do_next()
        player.queue.history.append(track)
        if len(player.queue.history) > 10:
            player.queue.history.pop(0)

    @commands.Cog.listener()
    async def on_pomice_track_exception(
        self, player: DragonPlayer, error_code, exception
    ):
        log.error(f"Pomice exception: {player.guild.name}: {error_code} | {exception} ")
        await player.controller.channel.send(f"Track errored skipping...")
        await player.do_next()

    @commands.Cog.listener()
    async def on_pomice_track_stuck(self, player: DragonPlayer, track: pomice.Track):
        await player.controller.channel.send(
            f"Track got stuck {track.title}\nto put it back in queue use /play {track.title}"
        )


def setup(client: DragonBot):
    client.add_cog(MusicEventCog(client))

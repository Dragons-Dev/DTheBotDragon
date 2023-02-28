import datetime
from contextlib import suppress

import pomice
import discord
from discord.ext import commands

from utils import utils


loop_emoji = {"Off": ":arrow_right:", "Track": ":repeat_one:", "Queue": ":repeat:"}


class DragonPlayer(pomice.Player):
    """Custom pomice Player class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.queue = pomice.Queue()
        self.controller: discord.Message = None
        # Set context here, so we can send a now playing embed
        self.context: commands.Context = None
        self.dj: discord.Member = None

    async def do_next(self) -> None:
        # Queue up the next track, else teardown the player
        try:
            track: pomice.Track = self.queue.get()
        except pomice.QueueEmpty:
            return await self.controller.edit(
                embed=discord.Embed(title="Queue empty", color=discord.Color.blurple())
            )

        await self.play(track)

    async def update_embed(self, upcoming_tracks: list[pomice.Track] = None) -> None:
        queue: list[pomice.Track] = self.queue.get_queue()
        track: pomice.Track = self.current if self.current is not None else queue[0]
        playing_until = 0
        playing_until += self.current.length if self.current is not None else 0
        for t in queue:
            playing_until += t.length
        until = datetime.datetime.now() + datetime.timedelta(milliseconds=playing_until)
        until = until.strftime("%H:%M")

        loop_mode = self.queue.loop_mode
        if loop_mode is pomice.LoopMode.TRACK:
            loop_mode = "Track"
        elif loop_mode is pomice.LoopMode.QUEUE:
            loop_mode = "Queue"
        else:
            loop_mode = "Off"

        embed = discord.Embed(
            title=f"Now playing",
            description=f"""[{track.title}]({track.uri})
                            Duration: {utils.sec_to_min(track.length/1000)} :hourglass_flowing_sand:
                            Author: {track.author} :notes:
                            Playing until: {until if loop_mode == "Off" else "To infinity :infinity:"} :clock3:
                            Loop: {loop_mode} {loop_emoji[loop_mode]}
                        """,
            color=discord.Color.blurple(),
        )
        embed.set_image(url=track.thumbnail)
        embed.set_footer(
            text=f"Requested by {track.requester.name}#{track.requester.discriminator}",
            icon_url=track.requester.display_avatar.url,
        )

        if upcoming_tracks is None:
            for i in range(5):
                now_fields = len(embed.fields)
                if now_fields > 4:
                    break
                try:
                    track = queue[i]
                    embed.add_field(
                        name=f"{now_fields + 1}. in queue",
                        value=f"[{track.title}]({track.uri})\n-> {track.author} :notes:\n-> {utils.sec_to_min(track.length/1000)}  :hourglass_flowing_sand:",
                        inline=False,
                    )
                except IndexError:
                    break
        else:
            for i in range(5):
                now_fields = len(embed.fields)
                if now_fields > 4:
                    break
                try:
                    track = upcoming_tracks[i]
                    embed.add_field(
                        name=f"{now_fields + 1}. in queue",
                        value=f"[{track.title}]({track.uri})\n-> {track.author} :notes:\n-> {utils.sec_to_min(track.length / 1000)}  :hourglass_flowing_sand:",
                        inline=False,
                    )
                except IndexError:
                    break
        await self.controller.edit(embed=embed)

    async def set_context(self, ctx: commands.Context):
        """Set context for the player"""
        self.context = ctx
        self.dj = ctx.author

    async def teardown(self):
        """Clear internal states, remove player controller and disconnect."""
        with suppress(discord.HTTPException, KeyError):
            await self.destroy()
            if self.controller:
                await self.controller.delete()

    async def get_controller(self):
        return self.controller

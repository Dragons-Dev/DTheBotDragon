import datetime
from contextlib import suppress

import pomice
import discord
from discord.ext import commands

from utils import utils


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
            queue = self.queue.copy()
        except pomice.QueueEmpty:
            return await self.controller.edit(
                embed=discord.Embed(title="Queue empty", color=discord.Color.blurple())
            )

        await self.play(track)

        playing_until = 0
        dur_queue = queue.copy()
        while True:
            try:
                playing_until += dur_queue.get().length
            except pomice.QueueEmpty:
                break

        until = datetime.datetime.now() + datetime.timedelta(milliseconds = playing_until)
        until = until.strftime("%H:%M")

        embed = discord.Embed(
            title=f"Now playing",
            description=f"""[{track.title}]({track.uri})
                            Duration: {utils.sec_to_min(track.length/1000)} :hourglass_flowing_sand:
                            Author: {track.author} :notes:
                            Playing until: {until} :clock3:
                        """,
            color=discord.Color.blurple(),
        )
        embed.set_image(url=track.thumbnail)
        embed.set_footer(
            text=f"Requested by {track.requester.name}#{track.requester.discriminator}",
            icon_url=track.requester.display_avatar.url,
        )

        now_fields = len(embed.fields)
        while not now_fields > 4:
            try:
                track = queue.get()
                embed.add_field(
                    name = f"{now_fields + 1}. in queue",
                    value = f"[{track.title}]({track.uri})\n-> {track.author} :notes:\n-> {utils.sec_to_min(track.length/1000)}  :hourglass_flowing_sand:",
                    inline = False,
                )
                now_fields += 1
            except pomice.QueueEmpty:
                break
        await self.controller.edit(embed=embed)

    async def teardown(self):
        """Clear internal states, remove player controller and disconnect."""
        with suppress(discord.HTTPException, KeyError):
            await self.destroy()
            if self.controller:
                await self.controller.delete()

    async def set_context(self, ctx: commands.Context):
        """Set context for the player"""
        self.context = ctx
        self.dj = ctx.author

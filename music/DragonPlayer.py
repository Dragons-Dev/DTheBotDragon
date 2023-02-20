import pomice
import discord
from discord.ext import commands
from contextlib import suppress


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

        # Call the controller (a.k.a: The "Now Playing" embed) and check if one exists

        embed = discord.Embed(
            title=f"Now playing",
            description=f"[{track.title}]({track.uri})",
            color=discord.Color.blurple(),
        )
        embed.set_image(url=track.thumbnail)
        embed.set_footer(
            text=f"Requested by {track.requester.name}#{track.requester.discriminator}",
            icon_url=track.requester.display_avatar.url,
        )
        await self.controller.edit(embed=embed)

    async def teardown(self):
        """Clear internal states, remove player controller and disconnect."""
        with suppress((discord.HTTPException), (KeyError)):
            await self.teardown()
            if self.controller:
                await self.controller.delete()

    async def set_context(self, ctx: commands.Context):
        """Set context for the player"""
        self.context = ctx
        self.dj = ctx.author

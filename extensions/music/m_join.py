import discord
from discord.ext import commands
from pycord import multicog

from DragonBot import DragonBot
from DragonPlayer.DragonPlayer import DragonPlayer


class MusicJoinCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @multicog.add_to_group("music")
    @commands.slash_command(name="join", description="Joins your voice channel")
    async def join_cmd(self, ctx: discord.ApplicationContext):
        if not ctx.voice_client:
            channel = getattr(ctx.user.voice, "channel", None)
            if not channel:
                raise commands.CheckFailure(
                    "You must be in a voice channel to use this command"
                    "without specifying the channel argument."
                )

            vc: DragonPlayer = await ctx.author.voice.channel.connect(cls=DragonPlayer)
            await vc.set_volume(25)
            await ctx.response.send_message(
                f"Joined the voice channel `{channel}`", delete_after=10
            )
            await self.client.ws.voice_state(
                guild_id=ctx.guild_id,
                channel_id=ctx.voice_client.channel.id,
                self_deaf=True,
            )
        else:
            await ctx.response.send_message(
                f"I can't join your voice channel I am already connected to {ctx.voice_client.channel}",
                delete_after=10,
                ephemeral=True,
            )


def setup(client: DragonBot):
    client.add_cog(MusicJoinCog(client))

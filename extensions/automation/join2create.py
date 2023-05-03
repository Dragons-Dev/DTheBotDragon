import discord
from discord.ext import commands

from DragonBot import DragonBot
from utils import db, statics, utils
from views.join2create_v import is_owner


class Join2CreateCog(commands.Cog):
    def __init__(self, client):
        self.client: DragonBot = client

    @commands.slash_command(
        name="permit", description="Allow access to your personal channel"
    )
    async def permit_cmd(
        self,
        ctx: discord.ApplicationContext,
        mention: discord.Option(discord.abc.Mentionable),
        allow: discord.Option(bool),
    ):
        guild = ctx.guild
        member = guild.get_member(ctx.author.id)
        try:
            channel = guild.get_channel(member.voice.channel.id)
        except AttributeError:
            return await ctx.response.send_message(
                f"**You are not in a voice channel.**", ephemeral=True, delete_after=5
            )

        if await is_owner(user_id=member.id, voice_id=channel):
            overwritten = {
                mention: discord.PermissionOverwrite(
                    connect=True,
                    send_messages=True,
                    read_messages=True,
                    read_message_history=True,
                )
            }
            await channel.edit(overwrites=overwritten)
            await ctx.response.send_message(
                f"{'Allowed' if allow else 'Denied'} access for {mention.mention}".strip(
                    "['']"
                ),
                ephemeral=True,
                delete_after=5,
            )

    @commands.Cog.listener("on_voice_state_update")
    async def on_join(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> None:
        join2create_channel = await db.get_setting(
            setting="join2create channel", guild=member.guild.id
        )
        if join2create_channel is None:
            return
        else:
            try:
                if member.voice.channel.id == int(join2create_channel[0]):
                    new_voice = await after.channel.category.create_voice_channel(
                        name=f"{member.display_name}'s-channel",
                        reason=f"Join2Create {member.name}#{member.discriminator}",
                    )
                    await member.move_to(new_voice, reason="Join2Create")
                    await db.add_join2create(channel=new_voice, owner=member.id)
            except AttributeError:
                pass

    @commands.Cog.listener("on_voice_state_update")
    async def on_leave(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> None:
        temp_channel = await db.get_join2create(before.channel)
        if temp_channel is None:
            return
        else:
            try:
                if before.channel.id == int(temp_channel[0]):
                    if len(before.channel.members) == 0:
                        await db.remove_join2create(before.channel)
                        await before.channel.delete(reason="Join2Delete")
            except AttributeError:
                pass


def setup(client: DragonBot):
    client.add_cog(Join2CreateCog(client))

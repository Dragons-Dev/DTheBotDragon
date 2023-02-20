import logging

import discord
from discord.ext import commands

from DragonBot import DragonBot
from utils import db


class MusicPanel(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name="setup_panel", description="Summon the new wavelink panel to use"
    )
    async def setup_panel(self, ctx: discord.ApplicationContext):
        team_id = await db.get_setting(setting="team role", guild=str(ctx.guild_id))
        if team_id is None:
            return await ctx.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You have not set up a team role.\nPlease set up a team role by running /settings Team Role your team role id",
                    color=discord.Color.brand_red(),
                ),
                ephemeral=True,
            )
        for role in ctx.author.roles:
            if int(team_id[0]) == int(role.id):
                await ctx.response.send_message(
                    "Message gets built", ephemeral=True, delete_after=5
                )
                msg = await ctx.channel.send(
                    embed=discord.Embed(
                        title="No song playing now",
                        description="Add new tracks by using /play",
                        color=discord.Color.blurple(),
                    )
                )
                await db.insert_setting(
                    setting="music_panel", value=str(msg.id), guild=ctx.guild_id
                )
                await db.insert_setting(
                    setting="music_panel_channel",
                    value=str(msg.channel.id),
                    guild=ctx.guild_id,
                )
                break
        else:
            await ctx.response.send_message(
                f"You are not allowed to setup the panel.", ephemeral=True
            )


def setup(client: DragonBot):
    client.add_cog(MusicPanel(client))

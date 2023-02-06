import logging

import discord
from discord.ext import commands

from DragonBot import DragonBot
from utils import db
from view import warn_v


class WarnCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.user_command(name = "Warn")
    async def warn(self, ctx: discord.ApplicationContext, member: discord.Member):
        team_id = await db.get_setting(setting = "team role", guild = str(ctx.guild_id))
        if team_id is None:
            return await ctx.response.send_message(embed = discord.Embed(
                title = "Error",
                description = "You have not set up a team role.\nPlease set up a team role by running /settings Team Role your team role id",
                color = discord.Color.brand_red()
            ), ephemeral = True)
        for role in ctx.author.roles:
            if int(team_id[0]) == int(role.id):
                await ctx.response.send_modal(warn_v.WarnModal(title = "Warn Member", user = member))
                break
        else:
            return await ctx.response.send_message("You are not allowed to warn a member!",
                                                   ephemeral = True,
                                                   delete_after = 5)


def setup(client: DragonBot):
    client.add_cog(WarnCog(client))

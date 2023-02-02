import logging

import discord
from discord.ext import commands

from DragonBot import DragonBot
from utils import db
from view import warn_v


class WarnCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.user_command(name = "warn")
    async def warn(self, ctx: discord.ApplicationContext, member: discord.Member):
        for role in ctx.author.roles:
            if not role.id in await db.get_setting():
                return await ctx.response.send_message("You are not allowed to warn a member!",
                                                       ephemeral = True,
                                                       delete_after = 5)

        else:
            await ctx.response.send_modal(warn_v.WarnModal())


def setup(client: DragonBot):
    client.add_cog(WarnCog(client))

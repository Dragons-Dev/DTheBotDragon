import logging

import discord
from discord.ext import commands

from DragonBot import DragonBot
from utils import db


class EcoBankCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command("bank")
    async def add_bank(self, ctx: commands.Context):
        for member in ctx.guild.members:
            m = await db.get_bank_acc(member.id)
            print(
                f"{member.name} got: {m[0]}€ | {m[1]}USD | {m[2]} Gold"
            )


def setup(client: DragonBot):
    client.add_cog(EcoBankCog(client))

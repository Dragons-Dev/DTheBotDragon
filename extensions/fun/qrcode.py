import logging

import discord
from discord.ext import commands
import pyqrcode

from DragonBot import DragonBot
from utils import db


class QRCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def qrcodify(self, ctx: commands.Context):
        qr_codes = []
        for attachment in ctx.message.attachments:
            qr_codes.append(pyqrcode.create(attachment))
        await ctx.reply(qr_codes)


def setup(client: DragonBot):
    client.add_cog(QRCog(client))

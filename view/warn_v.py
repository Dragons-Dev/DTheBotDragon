import discord
from discord import ui

from utils import db


class WarnModal(ui.Modal):
    def __init__(self, user: discord.Member, title = "Warn Context"):
        self.user = user
        self.title = title
        super().__init__()
        self.add_item(ui.InputText(
            style = discord.InputTextStyle.long,
            label = "Reason to warn",
            required = True))

    async def callback(self, interaction: discord.Interaction):
        log = await db.get_setting(setting = "log", guild = interaction.guild_id)
        if log is None:

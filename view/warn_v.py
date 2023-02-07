import discord
from discord import ui

from utils import db


class WarnModal(ui.Modal):
    def __init__(self, user: discord.Member, title = "Warn Context"):
        self.user = user
        self.title = title
        super().__init__(title = title)
        self.add_item(ui.InputText(
            style = discord.InputTextStyle.long,
            label = "Reason to warn",
            required = True))

    async def callback(self, interaction: discord.Interaction):
        log = await db.get_setting(setting = "log", guild = interaction.guild_id)
        await db.add_mod_action(member = self.user.id,
                                moderator = interaction.user.id,
                                action = "warn",
                                reason = self.children[0].value)
        em = discord.Embed(
            title = "Warn",
            description = f"Warn for {self.user.name}#{self.user.discriminator} ({self.user.id})",
            color = discord.Color.gold()
        )
        em.set_author(
            name = f"{interaction.user.name}#{interaction.user.discriminator} ({interaction.user.id})",
            icon_url = interaction.user.display_avatar
        )
        if log is None:
            await interaction.response.send_message(content = f"Please set a log channel to send logs.",
                                                    embed = em,
                                                    ephemeral = True,
                                                    delete_after = 5)

        else:
            log = interaction.client.get_channel(log[0])
            await interaction.response.send_message(embed = em,
                                                    ephemeral = True,
                                                    delete_after = 5)
            await log.send(embed = em)

import discord
from discord.ext import commands

import config
from DragonBot import DragonBot
from utils import db


class SettingsCog(commands.Cog):
    def __init__(self, client):
        self.client: DragonBot = client

    @commands.slash_command(
        name="settings", description="set some settings for your guild"
    )
    async def settings(
        self,
        ctx: discord.ApplicationContext,
        setting: discord.Option(
            required=True,
            choices=[
                discord.OptionChoice("Team Role"),
                discord.OptionChoice("Mod Log Channel"),
            ],
        ),
        value: discord.Option(required=True),
    ):
        await db.insert_setting(setting=setting, value=value, guild=ctx.guild_id)
        embed = discord.Embed(title="Success", color=discord.Color.brand_green())

        match setting:
            case "Team Role":
                embed.description = f"Successfully set {setting} to <@&{value}>"
            case "Mod Log Channel":
                embed.description = f"Successfully set {setting} to <#{value}>"

        await ctx.response.send_message(embed=embed, ephemeral=True)


def setup(client: DragonBot):
    client.add_cog(SettingsCog(client))

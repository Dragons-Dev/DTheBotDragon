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
            description="Choose the setting you want to change",
            required=True,
            choices=[
                discord.OptionChoice("Team Role"),
                discord.OptionChoice("Verified Role"),
                discord.OptionChoice("Mod Log Channel"),
                discord.OptionChoice("Modmail Channel"),
                discord.OptionChoice("Verification Channel"),  # TODO: Check if category channel
                discord.OptionChoice("Join2Create Channel"),
            ],
        ),
        value: discord.Option(
            description="Set the value of the option as id (Developer Mode required)",
            required=True,
        ),
    ):
        for role in ctx.author.roles:
            role: discord.Role = role
            if role.permissions.administrator:
                await db.insert_setting(
                    setting=setting, value=value, guild=ctx.guild_id
                )
                embed = discord.Embed(
                    title="Success", color=discord.Color.brand_green()
                )
                match setting:
                    case "Team Role":
                        embed.description = f"Successfully set {setting} to <@&{value}>"
                    case "Verified Role":
                        embed.description = f"Successfully set {setting} to <@&{value}>"
                    case _:
                        embed.description = f"Successfully set {setting} to <#{value}>"

                await ctx.response.send_message(embed=embed, ephemeral=True)
                break
        else:
            await ctx.response.send_message(
                embed=discord.Embed(
                    title="Error",
                    description="You are not allowed to set this setting!",
                    color=discord.Color.brand_red(),
                ),
                ephemeral=True,
            )


def setup(client: DragonBot):
    client.add_cog(SettingsCog(client))

import logging

import discord
from discord.ext import commands

from DragonBot import DragonBot
from utils import db

log = logging.getLogger("DragonBot")


class VerificationCog(commands.Cog):
    def __init__(self, client):
        self.client: DragonBot = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        resp = await db.get_setting(setting = "verification channel", guild = member.guild.id)
        print(resp)
        print(member.name)
        if resp is None:
            return None
        else:
            inv_category: discord.CategoryChannel = await discord.utils.get_or_fetch(member.guild, "channel", resp[0], default = None)
        overwrite = {
            member.guild.default_role: discord.PermissionOverwrite(view_channel = False),
            member: discord.PermissionOverwrite(view_channel = True,
                                                send_messages = True,
                                                use_slash_commands = True)
        }
        channel = await inv_category.create_text_channel(
            name = f"verify-{member.name}",
            reason = f"Create verification channel",
            topic = "/verify um die \"• Verified\" Rolle zu bekommen.",
            slowmode_delay = 5,
            overwrites = overwrite
        )
        
        await channel.send()



def setup(client: DragonBot):
    client.add_cog(VerificationCog(client))

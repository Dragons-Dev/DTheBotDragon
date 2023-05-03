import logging

import discord
from discord import ui

from utils import db


log = logging.getLogger("DragonLog")


async def is_owner(user_id: int, voice_id: discord.VoiceChannel) -> bool:
    response = await db.get_join2create(voice_id)
    if response is None:
        return False
    if response[1] == user_id:
        return True
    return False


class MaxUsersModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="Max Users", min_length=1, max_length=2, placeholder="5"
            )
        )

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        try:
            channel = guild.get_channel(member.voice.channel.id)
        except AttributeError:
            return await interaction.response.send_message(
                f"**You are not in a voice channel.**"
            )

        if await is_owner(user_id=member.id, voice_id=channel):
            try:
                value = int(self.children[0].value)

                if value < 0:
                    await interaction.response.send_message(
                        f"Please write a positive number.",
                        ephemeral=True,
                        delete_after=5,
                    )

                if value == 0:
                    await interaction.response.send_message(
                        f"Removed max members limit.", ephemeral=True, delete_after=5
                    )

                await interaction.response.send_message(
                    f"Max members adjusted to {value}.", ephemeral=True, delete_after=5
                )

                await channel.edit(user_limit=value)

            except ValueError:
                await interaction.response.send_message(
                    f"**You messed up to write a valid number!**",
                    ephemeral=True,
                    delete_after=5,
                )

            except discord.errors.InteractionResponded:
                pass

        else:
            try:
                await interaction.response.send_message(
                    f"**You are not the owner of the channel.**",
                    ephemeral=True,
                    delete_after=5,
                )
            except discord.errors.InteractionResponded:
                pass


class BitrateModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="Bitrate", min_length=1, max_length=3, placeholder="Default is 64"
            )
        )
        self.add_item(
            discord.ui.InputText(
                label="Information",
                required=False,
                style=discord.InputTextStyle.long,
                value="Minimal Value = 8\nDefault = 64\nNitro Tier 0 = 96\nNitro Tier 1 = 128\nNitro Tier 2 = 256\nNitro Tier 3 = 384",
            )
        )

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        bitrate = {"tier0": 96, "tier1": 128, "tier2": 256, "tier3": 384}
        try:
            channel = guild.get_channel(member.voice.channel.id)
        except AttributeError:
            return await interaction.response.send_message(
                f"**You are not in a voice channel.**"
            )

        if await is_owner(user_id=member.id, voice_id=channel):
            try:
                value = int(self.children[0].value)
                if guild.premium_tier == 0:
                    max_limit = bitrate["tier0"]
                elif guild.premium_tier == 1:
                    max_limit = bitrate["tier1"]
                elif guild.premium_tier == 2:
                    max_limit = bitrate["tier2"]
                elif guild.premium_tier == 3:
                    max_limit = bitrate["tier3"]
                else:
                    max_limit = bitrate["tier0"]

                if value < 8:
                    await interaction.response.send_message(
                        f"The minimum is 8kbps.",
                        ephemeral=True,
                        delete_after=5,
                    )

                if value > max_limit:
                    await interaction.response.send_message(
                        f"This guild is capped at {max_limit}kbps due to discord nitro.",
                        ephemeral=True,
                        delete_after=5,
                    )

                await interaction.response.send_message(
                    f"Bitrate adjusted to {value}.", ephemeral=True, delete_after=5
                )

                await channel.edit(bitrate=value * 1000)

            except ValueError:
                await interaction.response.send_message(
                    f"**You messed up to write a valid number!**",
                    ephemeral=True,
                    delete_after=5,
                )

            except discord.errors.InteractionResponded:
                pass

        else:
            try:
                await interaction.response.send_message(
                    f"**You are not the owner of the channel.**",
                    ephemeral=True,
                    delete_after=5,
                )
            except discord.errors.InteractionResponded:
                pass


class RenameModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="New Name",
                min_length=1,
                max_length=100,
                placeholder="My supercool channel",
            )
        )

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        try:
            channel = guild.get_channel(member.voice.channel.id)
        except AttributeError:
            return await interaction.response.send_message(
                f"**You are not in a voice channel.**"
            )

        if await is_owner(user_id=member.id, voice_id=channel):
            await channel.edit(name=self.children[0].value)
            await interaction.response.send_message(
                f'**Channel name changed to "{self.children[0].value}."**',
                ephemeral=True,
                delete_after=5,
            )

        else:
            try:
                await interaction.response.send_message(
                    f"**You are not the owner of the channel.**",
                    ephemeral=True,
                    delete_after=5,
                )
            except discord.errors.InteractionResponded:
                pass


class Join2CreateBoard(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @ui.button(label="Rename", custom_id="<Join2Create:Rename:1682279386>")
    async def rename(self, button: ui.Button, interaction: discord.Interaction):
        return await interaction.response.send_modal(
            RenameModal(title="Rename your channel")
        )

    @ui.button(label="Limit Users", custom_id="<Join2Create:LimitUsers:1682279386>")
    async def limit_users(self, button: ui.Button, interaction: discord.Interaction):
        return await interaction.response.send_modal(MaxUsersModal(title="Limit users"))

    @ui.button(label="Lock", custom_id="<Join2Create:Lock:1682279386>")
    async def lock(self, button: ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        v_r_response = await db.get_setting(setting="Verified Role", guild=guild.id)
        if v_r_response is None:
            return await interaction.response.send_message(
                f"This guild is not set up properly please contact an administrator.",
                ephemeral=True,
                delete_after=10,
            )
        verified_role = guild.get_role(int(v_r_response[0]))
        try:
            channel = guild.get_channel(member.voice.channel.id)
        except AttributeError:
            return await interaction.response.send_message(
                f"**You are not in a voice channel.**", ephemeral=True, delete_after=5
            )

        if await is_owner(user_id=member.id, voice_id=channel):
            values = await db.get_join2create(channel)
            if values is None:
                log.error("Could not find voice channel, even that it exists")
                return await interaction.response.send_message(
                    "**An internal error occurred, this is not intended to happen and will be fixed if noticed.**",
                    ephemeral=True,
                    delete_after=10,
                )
            else:
                check, owner, locked = values[0], values[1], values[2]
            if check == channel.id and locked == 1:
                prev_perm = channel.overwrites_for(verified_role)
                prev_perm.update(
                    connect=True,
                    send_messages=True,
                    read_messages=True,
                    read_message_history=True,
                )
                await channel.set_permissions(
                    target=verified_role,
                    overwrite=prev_perm,
                    reason="Join2Create Ghosted",
                )
                await db.edit_join2create(channel=channel, key="locked", value=0)
                await interaction.response.send_message(
                    f"**Your channel is now unlocked for {verified_role.name}.**",
                    ephemeral=True,
                    delete_after=10,
                )

            else:
                prev_perm = channel.overwrites_for(verified_role)
                prev_perm.update(
                    connect=False,
                    send_messages=False,
                    read_messages=False,
                    read_message_history=False,
                )
                await channel.set_permissions(
                    target=verified_role,
                    overwrite=prev_perm,
                    reason="Join2Create Ghosted",
                )
                await db.edit_join2create(channel=channel, key="locked", value=1)
                await interaction.response.send_message(
                    f"**Your channel is now locked for {verified_role.name}.**",
                    ephemeral=True,
                    delete_after=10,
                )

    @ui.button(label="Ghost", custom_id="<Join2Create:Ghost:1682279386>")
    async def ghost(self, button: ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        v_r_response = await db.get_setting(setting="Verified Role", guild=guild.id)
        if v_r_response is None:
            return await interaction.response.send_message(
                f"This guild is not set up properly please contact an administrator.",
                ephemeral=True,
                delete_after=10,
            )
        verified_role = guild.get_role(int(v_r_response[0]))
        try:
            channel = guild.get_channel(member.voice.channel.id)
        except AttributeError:
            return await interaction.response.send_message(
                f"**You are not in a voice channel.**", ephemeral=True, delete_after=5
            )

        if await is_owner(user_id=member.id, voice_id=channel):
            values = await db.get_join2create(channel)
            if values is None:
                log.error("Could not find voice channel, even that it exists.")
                return await interaction.response.send_message(
                    "**An internal error occurred, this is not intended to happen and will be fixed if noticed.**",
                    ephemeral=True,
                    delete_after=10,
                )
            else:
                check, owner, ghosted = values[0], values[1], values[3]
            if check == channel.id and ghosted == 1:
                prev_perm = channel.overwrites_for(verified_role)
                prev_perm.update(view_channel=True)
                await channel.set_permissions(
                    target=verified_role,
                    overwrite=prev_perm,
                    reason="Join2Create Ghosted",
                )
                await db.edit_join2create(channel=channel, key="ghosted", value=0)
                await interaction.response.send_message(
                    f"**Your channel is now visible for {verified_role.name}.**",
                    ephemeral=True,
                    delete_after=10,
                )

            else:
                prev_perm = channel.overwrites_for(verified_role)
                prev_perm.update(view_channel=False)
                await channel.set_permissions(
                    target=verified_role,
                    overwrite=prev_perm,
                    reason="Join2Create Ghosted",
                )
                await db.edit_join2create(channel=channel, key="ghosted", value=1)
                await interaction.response.send_message(
                    f"**Your channel is now invisible for {verified_role.name}.**",
                    ephemeral=True,
                    delete_after=10,
                )

    @ui.button(label="Take ownership", custom_id="<Join2Create:Owner:1682279386>")
    async def take_owner(self, button: ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        try:
            channel = guild.get_channel(member.voice.channel.id)
        except AttributeError:
            return await interaction.response.send_message(
                f"**You are not in a voice channel.**", ephemeral=True, delete_after=5
            )
        db_channel = await db.get_join2create(channel=channel)
        c_owner = db_channel[1]
        for member in channel.members:
            if member.id == c_owner:
                return await interaction.response.send_message(
                    f"**The current owner is still in this voice channel.**",
                    ephemeral=True,
                    delete_after=5,
                )
        else:
            await db.edit_join2create(channel=channel, key="owner", value=member.id)
            await channel.send(f"{member.name} is now the owner of this voice channel.")
            return await interaction.response.send_message(
                f"**You are now the owner of this voice channel.**",
                ephemeral=True,
                delete_after=5,
            )

    @ui.button(label="Bitrate", custom_id="<Join2Create:Bitrate:1682279386>")
    async def bitrate(self, button: ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(BitrateModal(title="Adjust your Bitrate"))

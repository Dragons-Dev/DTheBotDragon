import discord
from discord import ui


class LeaveModal(ui.Modal):
    def __init__(self, user: discord.Member, title="Leave Modal"):
        self.user = user
        self.title = title
        super().__init__(title=title)
        self.add_item(
            ui.InputText(
                style=discord.InputTextStyle.short, label="Confirm your decision", required=True, placeholder = "Write 'leave' to leave this server."
            )
        )

    async def callback(self, interaction: discord.Interaction):
        if not self.children[0].value == "leave":
            return await interaction.response.send_message("You didn't pass the check to leave this server")
        await interaction.response.send_message(f"{interaction.user.name}#{interaction.user.discriminator} left whilst the verification.")
        await interaction.user.kick(reason = f"{interaction.user.name}#{interaction.user.discriminator} left whilst the verification.")


class VerificationView(ui.View):    # registered in on_ready to be persistend
    def __init__(self):
        super().__init__(timeout = None)

    @ui.button(
        label = "Leave",
        custom_id = "<pers_butt:Leave:Verification>",
        style = discord.ButtonStyle.red,
        emoji = "<:redTick:962801636152078356>"
    )
    async def red_callback(self, button: discord.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(LeaveModal(interaction.user))

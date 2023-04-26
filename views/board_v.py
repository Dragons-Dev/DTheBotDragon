import discord
from discord import ui

from views import counter_v, join2create_v


class BoardView(ui.View):
    def __init__(self):
        super().__init__(
            timeout=600,
            disable_on_timeout=True
        )

    @ui.string_select(
        placeholder="Select the board to display",
        options=[
            discord.SelectOption(
                label="Counter",
                value="counter",
                description="Display the counter-game here",
                emoji="🔢",
            ),
            discord.SelectOption(
                label="Join2Create",
                value="join2create",
                description="Display the Join2Create Board here",
                emoji="🔉",
            )
        ]
    )
    async def select_callback(self, select: ui.Select, interaction: discord.Interaction):
        views = {
            "counter": counter_v.CounterView(),
            "join2create": join2create_v.Join2CreateBoard()
        }
        view = views[select.values[0]]
        await interaction.response.send_message(view = view)

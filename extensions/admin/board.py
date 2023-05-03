import discord
from discord.ext import commands
from views import board_v


class BoardCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="board", description="Create a board in this channel")
    async def board(self, ctx: discord.ApplicationContext) -> None:
        await ctx.response.send_message(view=board_v.BoardView())


def setup(client):
    client.add_cog(BoardCog(client))

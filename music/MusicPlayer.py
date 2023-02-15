from DragonBot import DragonBot
from discord.abc import Connectable
from mafic import Player, Track


class DragonPlayer(Player[DragonBot]):
    def __init__(self, client: DragonBot, channel: Connectable) -> None:
        super().__init__(client, channel)

        # Mafic does not provide a queue system right now, low priority.
        self.queue: list[Track] = []

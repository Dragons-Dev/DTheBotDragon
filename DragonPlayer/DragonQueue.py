import discord
import pomice


class DragonQueue(pomice.Queue):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.history: list[pomice.Track] = []
        self.last_track: pomice.Track = None

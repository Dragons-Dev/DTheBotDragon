import mafic
import discord
from discord.ext import commands

from music.MusicPlayer import DragonPlayer
from DragonBot import DragonBot
from utils import db


class MaficMusicEventsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="join", description="join's your voice")
    async def join(self, inter: discord.ApplicationContext):
        """Join your voice channel."""

        assert isinstance(inter.user, discord.Member)

        if not inter.user.voice or not inter.user.voice.channel:
            return await inter.response.send_message("You are not in a voice channel.")

        channel = inter.user.voice.channel

        # This apparently **must** only be `Client`.
        await channel.connect(
            cls=DragonPlayer
        )  # pyright: ignore[reportGeneralTypeIssues]
        await inter.send(f"Joined {channel.mention}.")

    @commands.slash_command(name="play", description="Play a song of your desire")
    async def play(self, inter: discord.ApplicationContext, query: str):
        """Play a song.
        query:
            The song to search or play.
        """

        assert inter.guild is not None

        if not inter.guild.voice_client:
            await self.join(inter)

        player: DragonPlayer = (
            inter.guild.voice_client
        )  # pyright: ignore[reportGeneralTypeIssues]

        tracks = await player.fetch_tracks(query)

        if not tracks:
            return await inter.send("No tracks found.")

        if isinstance(tracks, mafic.Playlist):
            tracks = tracks.tracks
            if len(tracks) > 1:
                player.queue.extend(tracks[1:])

        track = tracks[0]

        await player.play(track)

        await inter.send(f"Playing {track}")


'''
async def play_generator(ctx: discord.AutocompleteContext):
    """Returns a list of search results with the given input"""

    node: mafic.Node = mafic.NodePool.get_random_node()

    results = await node.fetch_tracks(ctx.value, search_type = "ytsearch")
    return [track.title for track in results[:5]]


class MaficMusicEventsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name = "play", description = "Play a song of your desire")
    async def music_play(
            self,
            ctx: discord.ApplicationContext,
            request: discord.Option(
                str, description = "request to search for a song", autocomplete = play_generator
            ),
    ):
        player: DragonPlayer = (
            ctx.interaction.guild.voice_client
        )

        if not ctx.user.voice or not ctx.user.voice.channel:
            return await ctx.response.send_message("You are not in a voice channel.", ephemeral = True)

        if not player.is_connected():
            await ctx.user.voice.channel.connect(cls = DragonPlayer)

        tracks = await player.fetch_tracks(request)
        track = tracks[0]

        if not player.current:
            await player.play(track)
            await ctx.response.send_message(f"Now playing `{track.title}`")
        else:
            player.queue.append(track)
            await ctx.response.send_message(f"Put into queue `{track.title}`")


'''


def setup(client: DragonBot):
    client.add_cog(MaficMusicEventsCog(client))

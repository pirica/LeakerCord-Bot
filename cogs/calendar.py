import json

import aiofiles
import aiohttp
import discord
from discord.ext import commands


class calendar(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["eventflags"])
    async def calendar(self, ctx):
        await self.client.wait_until_ready()
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://benbotfn.tk/api/v1/calendar') as data:
                    new = await data.json()
                    await (await aiofiles.open('Cache/calendar.json', mode='w+')).write(
                        json.dumps(new, indent=2))
        except Exception as ex:
            print(ex)
        file = discord.File("Cache/calendar.json")
        await ctx.send(f"Calendar/Eventflags:", file=file)


def setup(client):
    client.add_cog(calendar(client))

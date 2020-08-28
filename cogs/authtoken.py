import json
import traceback

import aiofiles
import aiohttp
from discord.ext import commands, tasks


class authtoken(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.tokencheck.start()
        except Exception as ex:
            print(ex)
            self.tokencheck.stop()
            self.tokencheck.start()

    @tasks.loop(seconds=60)
    async def tokencheck(self):
        await self.client.wait_until_ready()
        try:
            old = json.loads(await (await aiofiles.open('Cache/authtoken.json', mode='r', errors='ignore')).read())
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                        'https://api.nitestats.com/v1/epic/bearer') as data:
                    if data.status != 200:
                        return
                    new = await data.json()
        except Exception as error:
            traceback.print_exception(type(error), error, error.__traceback__)
            return
        if new != old:
            await (await aiofiles.open('Cache/authtoken.json', mode='w+')).write(
                json.dumps(new, indent=2))

    def cog_unload(self):
        self.tokencheck.stop()
        try:
            self.client.unload_extension("cogs.authtoken")
        except:
            pass
        try:
            self.client.load_extension("cogs.authtoken")
        except:
            pass


def setup(client):
    client.add_cog(authtoken(client))

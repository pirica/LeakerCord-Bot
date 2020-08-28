import json
import traceback
from datetime import datetime

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

from Settings import SETTINGS


class free(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.check.start()
        except Exception as ex:
            print(ex)
            self.check.stop()
            self.check.start()

    @tasks.loop(seconds=60)
    async def check(self):
        old = json.loads(
            await (await aiofiles.open('Cache/freegames.json', mode='r')).read())
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US") as response:
                new = await response.json()
                await (await aiofiles.open('Cache/freegames.json', mode='w+')).write(
                    json.dumps(new, indent=2))
        for i in new["data"]["Catalog"]["searchStore"]["elements"]:
            if not i in old["data"]["Catalog"]["searchStore"]["elements"]:
                print(i)
                try:
                    embed = discord.Embed(color=SETTINGS.embedcolor, title=i["title"],
                                          description=f"**Start:** {i['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['startDate'].split('T')[0]}\n"
                                                      f"**End:** {i['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate'].split('T')[0]}\n\n"
                                                      f"**Original Price:** {i['price']['totalPrice']['fmtPrice']['originalPrice']}")
                except:
                    embed = discord.Embed(color=SETTINGS.embedcolor, title=i["title"],
                                          description=f"**Start:** {i['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers'][0]['startDate'].split('T')[0]}\n"
                                                      f"**End:** {i['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers'][0]['endDate'].split('T')[0]}\n\n"
                                                      f"**Original Price:** {i['price']['totalPrice']['fmtPrice']['originalPrice']}")
                embed.set_image(url=i['keyImages'][0]['url'].replace(" ", ""))
                await self.client.get_channel(747731560945549414).send(embed=embed)

    def cog_unload(self):
        self.check.stop()
        try:
            self.client.unload_extension("cogs.freegames")
        except:
            pass
        try:
            self.client.load_extension("cogs.freegames")
        except:
            pass


def setup(client):
    client.add_cog(free(client))

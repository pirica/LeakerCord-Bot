import json

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

import Settings.SETTINGS


class updatechecker(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.checkpc.start()
        except Exception as ex:
            print(ex)
            self.checkpc.stop()
            self.checkpc.start()
        try:
            self.checkandroid.start()
        except Exception as ex:
            print(ex)
            self.checkandroid.stop()
            self.checkandroid.start()
        # try:
        #     self.checkios.start()
        # except Exception as ex:
        #     print(ex)
        #     self.checkios.stop()
        #     self.checkios.start()

    @tasks.loop(seconds=30)
    async def checkpc(self):
        await self.client.wait_until_ready()
        Cached = json.loads(
            await (await aiofiles.open('Cache/pc.json', mode='r')).read())
        token = json.loads(
            await (await aiofiles.open('Cache/authtoken.json', mode='r')).read())
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"bearer {token['accessToken']}"}
            async with session.get(
                    "https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/v2/platform/Windows/namespace/fn/catalogItem/4fe75bbc5a674f4f9b356b5c90567da5/app/Fortnite/label/Live",
                    headers=headers) as req:
                if req.status != 200:
                    return
                new = await req.json()
        if Cached['elements'][0]['buildVersion'] != new['elements'][0]['buildVersion']:
            await (await aiofiles.open(f"Cache/pc.json", mode='w+')).write(
                json.dumps(new, indent=2))
            await self.client.get_channel(743706003803209809).send(
                embed=discord.Embed(color=Settings.SETTINGS.embedcolor,
                                    title=f"New {new['elements'][0]['appName']} PC Update detected!",
                                    description=f"{new['elements'][0]['labelName']}\n{new['elements'][0]['buildVersion']}"))

    @tasks.loop(seconds=30)
    async def checkandroid(self):
        await self.client.wait_until_ready()
        Cached = json.loads(
            await (await aiofiles.open('Cache/android.json', mode='r')).read())
        token = json.loads(
            await (await aiofiles.open('Cache/authtoken.json', mode='r')).read())
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"bearer {token['accessToken']}"}
            async with session.get(
                    "https://launcher-public-service-prod-m.ol.epicgames.com/launcher/api/public/assets/Android/5cb97847cee34581afdbc445400e2f77/FortniteContentBuilds?label=Live",
                    headers=headers) as req:
                if req.status != 200:
                    return
                new = await req.json()
        if Cached['buildVersion'] != new['buildVersion']:
            await (await aiofiles.open(f"Cache/android.json", mode='w+')).write(
                json.dumps(new, indent=2))
            await self.client.get_channel(743706003803209809).send(
                embed=discord.Embed(color=Settings.SETTINGS.embedcolor,
                                    title=f"New {new['appName']} Android Update detected!",
                                    description=f"{new['labelName']}\n{new['buildVersion']}"))

    @tasks.loop(seconds=30)
    async def checkios(self):
        await self.client.wait_until_ready()
        Cached = json.loads(
            await (await aiofiles.open('Cache/ios.json', mode='r')).read())
        token = json.loads(
            await (await aiofiles.open('Cache/authtoken.json', mode='r')).read())
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"bearer {token['accessToken']}"}
            async with session.get(
                    "https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/public/assets/v2/platform/Windows/namespace/fn/catalogItem/4fe75bbc5a674f4f9b356b5c90567da5/app/Fortnite/label/Live",
                    headers=headers) as req:
                if req.status != 200:
                    return
                new = await req.json()
        if Cached["elements"][0]['buildVersion'] != new["elements"][0]['buildVersion']:
            await (await aiofiles.open(f"Cache/ios.json", mode='w+')).write(
                json.dumps(new, indent=2))
            await self.client.get_channel(743706003803209809).send(
                embed=discord.Embed(color=Settings.SETTINGS.embedcolor,
                                    title=f"New {new['elements'][0]['appName']} IOS Update detected!",
                                    description=f"{new['elements'][0]['labelName']}\n{new['elements'][0]['buildVersion']}"))

    def cog_unload(self):
        self.checkpc.stop()
        self.checkandroid.stop()
        self.checkios.stop()
        try:
            self.client.unload_extension("cogs.updatechecker")
        except:
            pass
        try:
            self.client.load_extension("cogs.updatechecker")
        except:
            pass


def setup(client):
    client.add_cog(updatechecker(client))

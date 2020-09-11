import json
import traceback

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

import Settings.SETTINGS


class newstuff(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.checkstatus.start()
        except Exception as ex:
            print(ex)
            self.checkstatus.stop()
            self.checkstatus.start()

    @tasks.loop(seconds=30)
    async def checkstatus(self):
        await self.client.wait_until_ready()
        try:
            Cached = json.loads(await (await aiofiles.open('Cache/playlist.json', mode='r', errors='ignore')).read())
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                        'https://api.peely.de/v1/playlists') as data:
                    if data.status != 200:
                        return
                    new = await data.json()
        except Exception as error:
            traceback.print_exception(type(error), error, error.__traceback__)
            return
        # LTMS
        if Cached["data"]["playlists"] != new["data"]["playlists"]:
            for i in new["data"]["playlists"]:
                if i not in Cached["data"]["playlists"]:
                    print("NEW LTM")
                    await (await aiofiles.open('Cache/playlist.json', mode='w+')).write(
                        json.dumps(new, indent=2))
                    channel = self.client.get_channel(741337081200115753)
                    des = ""
                    dis = ""
                    int = ""
                    try:
                        if i["description"]:
                            des = "**Description**:\n" + str(i["description"])
                    except:
                        pass
                    try:
                        if i["display_name"]:
                            dis = "**Display Name**:\n" + str(i["playlist_name"])
                    except:
                        pass
                    try:
                        if i["playlist_id"]:
                            int = "**Intern Name**:\n" + str(i["playlist_id"])
                    except:
                        pass
                    embed = discord.Embed(color=Settings.SETTINGS.embedcolor,
                                          description=f"\n\n{dis}\n\n{des}\n\n{int}")
                    embed.set_image(url=i["image"])
                    embed.set_author(name="New Battle Royale Playlist/LTM was added/updated.")
                    if Settings.SETTINGS.test is False:
                        await channel.send(embed=embed)

        # Tournaments
        await self.client.wait_until_ready()
        try:
            Cached = json.loads(await (await aiofiles.open('Cache/tournaments.json', mode='r', errors='ignore')).read())
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                        'https://api.peely.de/v1/tournaments') as data:
                    if data.status != 200:
                        return
                    new = await data.json()
        except Exception as error:
            traceback.print_exception(type(error), error, error.__traceback__)
            return
        if Cached["data"]["tournaments"] != new["data"]["tournaments"]:
            await (await aiofiles.open('Cache/tournaments.json', mode='w+')).write(
                json.dumps(new, indent=2))
            print("NEW Tournaments")
            for i in new["data"]["tournaments"]:
                if i not in Cached["data"]["tournaments"]:
                    channel = self.client.get_channel(741337132651773974)
                    embed = discord.Embed(color=Settings.SETTINGS.embedcolor)
                    embed.set_image(url=i["image"])
                    embed.set_author(name=i["name"])
                    embed.add_field(name=f"Description", value=i["description"])
                    if Settings.SETTINGS.test is False:
                        await channel.send(embed=embed)

        await self.client.wait_until_ready()
        Cached = json.loads(await (await aiofiles.open('Cache/notices.json', mode='r', errors='ignore')).read())
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                    'https://api.peely.de/v1/notices') as data:
                if data.status != 200:
                    return
                new = await data.json()
        if new["data"]["messages"] != Cached["data"]["messages"]:
            for i in new["data"]["messages"]:
                if i not in Cached["data"]["messages"]:
                    try:
                        channel = self.client.get_channel(741337172497400109)
                        if Settings.SETTINGS.test is False:
                            await channel.send(embed=discord.Embed(title=i["title"],
                                                                   description=i["description"],
                                                                   color=Settings.SETTINGS.embederror))
                    except Exception as ex:
                        print(ex)
                        traceback.print_exception(type(ex), ex, ex.__traceback__)
            await (await aiofiles.open('Cache/notices.json', mode='w+')).write(
                json.dumps(new, indent=2))

    def cog_unload(self):
        self.checkstatus.stop()
        try:
            self.client.unload_extension("cogs.newstuff")
        except:
            pass
        try:
            self.client.load_extension("cogs.newstuff")
        except:
            pass


def setup(client):
    client.add_cog(newstuff(client))

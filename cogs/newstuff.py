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
            Cached = json.loads(await (await aiofiles.open('Cache/content.json', mode='r', errors='ignore')).read())
            async with aiohttp.ClientSession() as cs:
                async with cs.get(
                        'https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game') as data:
                    if data.status != 200:
                        return
                    try:
                        new = await data.json()
                    except:
                        return
        except Exception as error:
            traceback.print_exception(type(error), error, error.__traceback__)
            return
        if new is None:
            return
        if Cached is None:
            return
        # LTMS
        if Cached["playlistinformation"]["playlist_info"]["playlists"] != new["playlistinformation"]["playlist_info"][
            "playlists"]:
            for i in new["playlistinformation"]["playlist_info"]["playlists"]:
                if i not in Cached["playlistinformation"]["playlist_info"]["playlists"]:
                    print("NEW LTM")
                    await (await aiofiles.open('Cache/content.json', mode='w+')).write(
                        json.dumps(new, indent=2))
                    channel = self.client.get_channel(741337081200115753)
                    des = ""
                    dis = ""
                    int = ""
                    type3 = ""
                    try:
                        if i["description"]:
                            des = "**Description**:\n" + str(i["description"])
                    except:
                        pass
                    try:
                        if i["display_name"]:
                            dis = "**Display Name**:\n" + str(i["display_name"])
                    except:
                        pass
                    try:
                        if i["playlist_name"]:
                            int = "**Intern Name**:\n" + str(i["playlist_name"])
                    except:
                        pass
                    try:
                        if i["violator"]:
                            type3 = "**Type**:\n" + str(i["violator"])
                    except:
                        pass
                    embed = discord.Embed(color=Settings.SETTINGS.embedcolor,
                                          description=f"\n\n{dis}\n\n{des}\n\n{int}\n\n{type3}")
                    embed.set_image(url=i["image"])
                    embed.set_author(name="New Battle Royale Playlist/LTM was added/updated.")
                    if Settings.SETTINGS.test is False:
                        await channel.send(embed=embed)
        # Tournaments
        if Cached["tournamentinformation"]["tournament_info"]["tournaments"] != \
                new["tournamentinformation"]["tournament_info"]["tournaments"]:
            await (await aiofiles.open('Cache/content.json', mode='w+')).write(
                json.dumps(new, indent=2))
            print("NEW Tournaments")
            for i in new["tournamentinformation"]["tournament_info"]["tournaments"]:
                if i not in Cached["tournamentinformation"]["tournament_info"]["tournaments"]:
                    channel = self.client.get_channel(741337132651773974)
                    embed = discord.Embed(color=Settings.SETTINGS.embedcolor)
                    embed.set_image(url=i["poster_front_image"])
                    embed.set_author(name=i["long_format_title"])
                    embed.add_field(name=f"Description", value=i["details_description"])
                    if Settings.SETTINGS.test is False:
                        await channel.send(embed=embed)

        if new["emergencynotice"]["news"]["messages"] != Cached["emergencynotice"]["news"]["messages"]:
            for i in new["emergencynotice"]["news"]["messages"]:
                if i not in Cached["emergencynotice"]["news"]["messages"]:
                    try:
                        channel = self.client.get_channel(741337172497400109)
                        if Settings.SETTINGS.test is False:
                            await channel.send(embed=discord.Embed(title=i["title"],
                                                                   description=i["body"],
                                                                   color=Settings.SETTINGS.embederror))
                    except Exception as ex:
                        print(ex)
                        traceback.print_exception(type(ex), ex, ex.__traceback__)
            await (await aiofiles.open('Cache/content.json', mode='w+')).write(
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

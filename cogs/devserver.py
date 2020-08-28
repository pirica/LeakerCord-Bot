import json
import traceback

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

import Settings.SETTINGS

liste = [
    "fortnite-public-service-devplaytest-prod12.ol.epicgames.com",
    "fortnite-public-service-devplaytestb-prod.ol.epicgames.com",
    "fortnite-public-service-devplaytestc-prod.ol.epicgames.com",
    "fortnite-public-service-devplaytestd-prod.ol.epicgames.com",
    "fortnite-public-service-devplayteste-prod.ol.epicgames.com",
    "fortnite-public-service-devplaytestf-prod.ol.epicgames.com",
    "fortnite-public-service-devplaytestg-prod.ol.epicgames.com",
    "fortnite-public-service-devplaytesth-prod.ol.epicgames.com",
    "fortnite-public-service-devplaytesti-prod.ol.epicgames.com",
    "fortnite-public-service-devplaytestj-prod.ol.epicgames.com",
    "fortnite-public-service-devplaytestk-prod.ol.epicgames.com",
    "fortnite-public-service-devplaytestl-prod.ol.epicgames.com",
    "fortnite-public-service-devplaytestm-prod.ol.epicgames.com",
    "fortnite-public-service-devplaytestn-prod.ol.epicgames.com",
    "fortnite-public-service-devplaytesto-prod.ol.epicgames.com",
    "fortnite-public-service-stage.ol.epicgames.com",
    "fortnite-public-service-nscert-stage.ol.epicgames.com",
    "fortnite-public-service-prod11.ol.epicgames.com",
    "fortnite.fortnite.qq.com",
    "fortnite-public-service-publictest-prod12.ol.epicgames.com",
    "fortnite-public-service-preview-prod.ol.epicgames.com",
    "fortnite-public-service-events-prod.ol.epicgames.com",
    "fortnite-public-service-reviewcn-prod.ol.epicgames.com",
    "fortnite-public-service-extqadevtesting-prod.ol.epicgames.com",
    "fortnite-public-service-extqauetesting-prod.ol.epicgames.com",
    "fortnite-public-service-bacchusplaytest-prod.ol.epicgames.com",
    "fortnite-public-service-loctesting-prod12.ol.epicgames.com",
    "fortnite-public-service-extqareleasetesting-prod.ol.epicgames.com",
    "fortnite-public-service-extqareleasetestingb-prod.ol.epicgames.com",
    "fortnite-public-service-releaseplaytest-prod.ol.epicgames.com",
    "fortnite-public-service-predeploya-prod.ol.epicgames.com",
    "fortnite-public-service-predeployb-prod.ol.epicgames.com",
    "fortnite-public-service-livebroadcasting-prod.ol.epicgames.com",
    "fortnite-public-service-livetesting-prod.ol.epicgames.com",
    "fortnite-service-livetesting.fortnite.qq.com",
    "fortnite-service-epicreleasetesting.fortnite.qq.com",
    "fortnite-service-tencentreleasetesting.fortnite.qq.com",
    "fortnite-service-securitytesting.fortnite.qq.com",
    "fortnite-service-predeploy.fortnite.qq.com",
    "fortnite-public-service-partners-prod.ol.epicgames.com",
    "fortnite-public-service-partnersstable-prod.ol.epicgam",
    "fortnite-public-service-ioscert-prod.ol.epicgames.com",
    "fortnite-public-service-athena-prod.ol.epicgames.com",
    "fortnite-public-service-loadtest-prod.ol.epicgames.com"
]


class devserver(commands.Cog):
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

    @tasks.loop(seconds=80)
    async def checkstatus(self):
        await self.client.wait_until_ready()
        await self.devserverr()
        for url in liste:
            try:
                Cached = None
                newCached = None
                try:
                    Cached = json.loads(
                        await (await aiofiles.open(f"Cache/DevServer/{url}.json", mode='r')).read())
                    newCached = json.loads(
                        await (await aiofiles.open(f"Cache/DevServer/NEW-{url}.json", mode='r')).read())
                except Exception as ex:
                    print(ex)
                    pass
                async with aiohttp.ClientSession() as cs:
                    async with cs.get("https://" + url + "/fortnite/api/version") as data:
                        if data.status != 200:
                            continue
                        temp = await data.json()
                        newnew = {
                            "branch": temp["branch"],
                            "build": temp["build"],
                            "buildDate": temp["buildDate"]
                        }
                        new = {
                            "branch": temp["branch"]
                        }

                if Cached != new:
                    try:
                        stri = ""
                        stri += f"**Server:** ``{url}``\n\n"

                        try:
                            cbranch = Cached["branch"]
                            stri += f"**Old:** ~~{cbranch}~~\n\n"
                        except:
                            pass

                        try:
                            branch = new["branch"]
                        except:
                            branch = "Not found"
                        stri += f"**New:** {branch}\n"

                        channel = self.client.get_channel(741334477434912820)
                        await (await aiofiles.open(f"Cache/DevServer/{url}.json", mode='w+')).write(
                            json.dumps(new, indent=2))
                        if Settings.SETTINGS.test is False:
                            await channel.send(embed=discord.Embed(title="A Dev Server was updated.",
                                                                   description=stri,
                                                                   color=Settings.SETTINGS.embedsuccess))
                    except Exception as ex:
                        print(ex)
                        traceback.print_exception(type(ex), ex, ex.__traceback__)
                if newCached != newnew:
                    stri = ""
                    stri += f"**Server:** ``{url}``\n\n"

                    try:
                        cbranch = newCached["branch"]
                    except:
                        cbranch = "Not found"
                    stri += f"**Old Version:** ~~{cbranch}~~\n"

                    try:
                        branch = newnew["branch"]
                    except:
                        branch = "Not found"
                    stri += f"**New Version:** {branch}\n\n"

                    try:
                        cbuild = newCached["build"]
                    except:
                        cbuild = f"Not found"
                    stri += f"**Old Build-ID:** ~~{cbuild}~~\n"

                    try:
                        build = newnew["build"]
                    except:
                        build = "Not found"
                    stri += f"**New Build-ID:** {build}\n\n"

                    try:
                        i2 = newCached["buildDate"]
                        i2 = i2.split("T")
                        i3 = i2[1]
                        i3 = i3.split(":")
                        i2 = i2[0].split("-")
                        cbuildDate = f"{i2[2]}.{i2[1]}.{i2[0]} - {i3[0]}:{i3[1]}"
                    except:
                        cbuildDate = "Not found"
                    stri += f"**Old Build-Date:** ~~{cbuildDate}~~\n"

                    try:
                        i2 = newnew["buildDate"]
                        i2 = i2.split("T")
                        i3 = i2[1]
                        i3 = i3.split(":")
                        i2 = i2[0].split("-")
                        buildDate = f"{i2[2]}.{i2[1]}.{i2[0]} - {i3[0]}:{i3[1]}"
                    except:
                        buildDate = "Not found"
                    stri += f"**New Build-Date:** {buildDate}"

                    channel = self.client.get_channel(741334477434912820)
                    await (await aiofiles.open(f"Cache/DevServer/NEW-{url}.json", mode='w+')).write(
                        json.dumps(newnew, indent=2))
                    if Settings.SETTINGS.test is False:
                        await channel.send(embed=discord.Embed(title="A Dev Server was updated.",
                                                               description=stri,
                                                               color=Settings.SETTINGS.embedsuccess))
            except Exception as ex:
                continue

    @commands.command()
    async def devserver(self, ctx):
        temp = {}
        for url in liste:
            data = json.loads(
                await (await aiofiles.open(f"Cache/DevServer/{url}.json", mode='r')).read())
            if not data.get("branch"):
                continue
            if not temp.get(str(data["branch"])):
                temp[str(data['branch'])] = 0
            temp[str(data['branch'])] += 1
        string = ""
        for i in temp:
            string += f"{i}: {temp[i]}\n"
        embed = discord.Embed(color=Settings.SETTINGS.embedcolor, title=f"Current Devserver", description=string)
        return await ctx.send(embed=embed)

    async def devserverr(self):
        temp = {}
        for url in liste:
            data = json.loads(
                await (await aiofiles.open(f"Cache/DevServer/{url}.json", mode='r')).read())
            if not data.get("branch"):
                continue
            if not temp.get(str(data["branch"])):
                temp[str(data['branch'])] = 0
            temp[str(data['branch'])] += 1
        channel = self.client.get_channel(741626516454113350)
        msg = await channel.fetch_message(741628204808142908)
        string = ""
        for i in temp:
            string += f"{i}: {temp[i]}\n"
        embed = discord.Embed(color=Settings.SETTINGS.embedcolor, title=f"Current Devserver", description=string)
        async with aiohttp.ClientSession() as ses:
            async with ses.get("https://fortnite-public-service-stage.ol.epicgames.com/fortnite/api/version") as resp:
                if resp.status == 200:
                    embed.set_footer(
                        text=f"The Staging server is current on the v{dict(await resp.json())['version']}.")
        return await msg.edit(embed=embed)

    def cog_unload(self):
        self.checkstatus.stop()
        try:
            self.client.unload_extension("cogs.devserver")
        except:
            pass
        try:
            self.client.load_extension("cogs.devserver")
        except:
            pass


def setup(client):
    client.add_cog(devserver(client))

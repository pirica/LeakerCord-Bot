import json
import traceback

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

import Settings.SETTINGS


class weapon(commands.Cog):
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

    @tasks.loop(minutes=5)
    async def checkstatus(self):
        await self.client.wait_until_ready()
        try:
            Cached = json.loads(
                await (await aiofiles.open('Cache/weapons.json', mode='r')).read())
            async with aiohttp.ClientSession() as cs:
                parameter = {"Authorization": "2fce9bf4-dcb28a26-d7e48ccf-a12cccee"}
                async with cs.get(
                        'https://fortniteapi.io/loot/list?lang=en', headers=parameter) as data:
                    if data.status != 200:
                        return
                    try:
                        new = await data.json()
                    except:
                        return
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            print(ex)
            return
        if new is None:
            nono = self.client.get_user(Settings.SETTINGS.nono)
            await nono.send("weapons not loaded", new)
            return print("LOLweapons")
        if Cached is None:
            nono = self.client.get_user(Settings.SETTINGS.nono)
            await nono.send("weapons cache not loaded")
            return print("LOL weapons")
        if Cached["weapons"] != new["weapons"]:
            for i in new["weapons"]:
                if i not in Cached["weapons"]:
                    i2 = None
                    gefunden = False
                    for i2 in Cached["weapons"]:
                        if i["id"] == i2["id"]:
                            gefunden = True
                            break
                        else:
                            continue
                    if gefunden is False:
                        try:
                            channel = self.client.get_channel(741334712630378567)
                            try:
                                name = i["name"]
                                if name is None:
                                    name = "Name not found"
                            except:
                                name = "Name not found"

                            embed = discord.Embed(color=Settings.SETTINGS.embedcolor, title=f"New Weapon | {name}")

                            try:
                                if i["id"]:
                                    embed.add_field(name="ID", value=i["id"])
                            except:
                                embed.add_field(name="ID", value="Not found ¯\_(ツ)_/¯")

                            try:
                                if i["description"]:
                                    embed.add_field(name="Description", value=i["description"])
                            except:
                                embed.add_field(name="Description", value="Not found ¯\_(ツ)_/¯")

                            try:
                                if i["searchTags"]:
                                    embed.add_field(name="Search Tags", value=i["searchTags"])
                            except:
                                pass

                            stats = "```py\n"
                            try:
                                damage = i["mainStats"]["DmgPB"]
                                if damage is None:
                                    damage = "Not Found"
                            except:
                                damage = "Not Found"
                            stats += f"Damage: {damage}\n"

                            try:
                                FiringRate = i["mainStats"]["FiringRate"]
                                if FiringRate is None:
                                    FiringRate = "Not Found"
                            except:
                                FiringRate = "Not Found"
                            stats += f"Firing Rate: {FiringRate}\n"

                            try:
                                ClipSize = i["mainStats"]["ClipSize"]
                                if ClipSize is None:
                                    ClipSize = "Not Found"
                            except:
                                ClipSize = "Not Found"
                            stats += f"Clip Size: {ClipSize}\n"

                            try:
                                BulletsPerCartridge = i["mainStats"]["BulletsPerCartridge"]
                                if BulletsPerCartridge is None:
                                    BulletsPerCartridge = "Not Found"
                            except:
                                BulletsPerCartridge = "Not Found"
                            stats += f"Bullets per Shoot: {BulletsPerCartridge}\n"

                            try:
                                ReloadTime = i["mainStats"]["ReloadTime"]
                                if ReloadTime is None:
                                    ReloadTime = "Not Found"
                            except:
                                ReloadTime = "Not Found"
                            stats += f"Reload Time: {ReloadTime}\n"

                            stats += "```"

                            try:
                                embed.add_field(name="Stats", value=stats)
                            except:
                                embed.add_field(name="Stats", value="Not found ¯\_(ツ)_/¯")

                            try:
                                embed.set_image(url=i["images"]["background"])
                            except:
                                try:
                                    embed.set_image(url=i["images"]["icon"])
                                except:
                                    embed.set_footer(text="Image not found. ¯\_(ツ)_/¯")

                            if Settings.SETTINGS.test is False:
                                await channel.send(embed=embed)

                        except Exception as ex:
                            traceback.print_exception(type(ex), ex, ex.__traceback__)
                            print(ex)
                    else:
                        try:
                            darf = False
                            if i["name"] != i2["name"]:
                                darf = True
                            if i["mainStats"]["DmgPB"] != i2["mainStats"]["DmgPB"]:
                                darf = True
                            if i["mainStats"]["FiringRate"] != i2["mainStats"]["FiringRate"]:
                                darf = True
                            if i["mainStats"]["ClipSize"] != i2["mainStats"]["ClipSize"]:
                                darf = True
                            if i["mainStats"]["ReloadTime"] != i2["mainStats"]["ReloadTime"]:
                                darf = True
                            if i["mainStats"]["BulletsPerCartridge"] != i2["mainStats"]["BulletsPerCartridge"]:
                                darf = True

                            if darf is True:
                                channel = self.client.get_channel(741334712630378567)
                                try:
                                    name = i["name"]
                                    if name is None:
                                        name = "Name not found"
                                except:
                                    name = "Name not found"

                                embed = discord.Embed(color=Settings.SETTINGS.embedcolor,
                                                      title=f"a Weapon was Updated | {name}")

                                try:
                                    if i["id"]:
                                        embed.add_field(name="ID", value=i["id"])
                                except:
                                    embed.add_field(name="ID", value="Not found ¯\_(ツ)_/¯")

                                stats = "```py\n"
                                try:
                                    damage = i["mainStats"]["DmgPB"]
                                    if damage is None:
                                        damage = "Not Found"
                                except:
                                    damage = "Not Found"
                                try:
                                    olddamage = i2["mainStats"]["DmgPB"]
                                    if olddamage is None:
                                        olddamage = "Not Found"
                                except:
                                    olddamage = "Not Found"
                                stats += f"New Damage: {damage}\n"
                                stats += f"Old Damage: {olddamage}\n\n"

                                try:
                                    FiringRate = i["mainStats"]["FiringRate"]
                                    if FiringRate is None:
                                        FiringRate = "Not Found"
                                except:
                                    FiringRate = "Not Found"
                                try:
                                    oldFiringRate = i2["mainStats"]["FiringRate"]
                                    if oldFiringRate is None:
                                        oldFiringRate = "Not Found"
                                except:
                                    oldFiringRate = "Not Found"
                                stats += f"New Firing Rate: {FiringRate}\n"
                                stats += f"Old Firing Rate: {oldFiringRate}\n\n"

                                try:
                                    ClipSize = i["mainStats"]["ClipSize"]
                                    if ClipSize is None:
                                        ClipSize = "Not Found"
                                except:
                                    ClipSize = "Not Found"
                                try:
                                    oldClipSize = i2["mainStats"]["ClipSize"]
                                    if oldClipSize is None:
                                        oldClipSize = "Not Found"
                                except:
                                    oldClipSize = "Not Found"
                                stats += f"New Clip Size: {ClipSize}\n"
                                stats += f"Old Clip Size: {oldClipSize}\n\n"

                                try:
                                    ReloadTime = i["mainStats"]["ReloadTime"]
                                    if ReloadTime is None:
                                        ReloadTime = "Not Found"
                                except:
                                    ReloadTime = "Not Found"
                                try:
                                    oldReloadTime = i2["mainStats"]["ReloadTime"]
                                    if oldReloadTime is None:
                                        oldReloadTime = "Not Found"
                                except:
                                    oldReloadTime = "Not Found"
                                stats += f"New Reload Time: {ReloadTime}\n"
                                stats += f"Old Reload Time: {oldReloadTime}"

                                try:
                                    BulletsPerCartridge = i["mainStats"]["BulletsPerCartridge"]
                                    if BulletsPerCartridge is None:
                                        BulletsPerCartridge = "Not Found"
                                except:
                                    BulletsPerCartridge = "Not Found"
                                try:
                                    oldBulletsPerCartridge = i2["mainStats"]["BulletsPerCartridge"]
                                    if oldBulletsPerCartridge is None:
                                        oldBulletsPerCartridge = "Not Found"
                                except:
                                    oldBulletsPerCartridge = "Not Found"
                                stats += f"New Bullets per Shoot: {BulletsPerCartridge}\n"
                                stats += f"Old Bullets per Shoot: {oldBulletsPerCartridge}\n"
                                stats += "```"
                                try:
                                    embed.add_field(name="Stats", value=stats)
                                except:
                                    embed.add_field(name="Stats", value="Not found ¯\_(ツ)_/¯")

                                try:
                                    embed.set_image(url=i["images"]["background"])
                                except:
                                    try:
                                        embed.set_image(url=i["images"]["icon"])
                                    except:
                                        embed.set_footer(text="Image not found. ¯\_(ツ)_/¯")
                                if Settings.SETTINGS.test is False:
                                    await channel.send(embed=embed)
                        except Exception as ex:
                            traceback.print_exception(type(ex), ex, ex.__traceback__)
                            print(ex)
            await (await aiofiles.open('Cache/weapons.json', mode='w+')).write(
                json.dumps(new, indent=2))

    def cog_unload(self):
        self.checkstatus.stop()
        try:
            self.client.unload_extension("cogs.weapon")
        except:
            pass
        try:
            self.client.load_extension("cogs.weapon")
        except:
            pass


def setup(client):
    client.add_cog(weapon(client))

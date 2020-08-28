import json

import aiofiles
import aiohttp
import discord
from discord.ext import commands

import Settings.SETTINGS


class cosmetics(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["cosmetics"])
    async def allcosmetics(self, ctx):
        await self.client.wait_until_ready()
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://benbotfn.tk/api/v1/cosmetics/br') as data:
                    new = await data.json()
                    await (await aiofiles.open('Cache/allcosmetics.json', mode='w+')).write(
                        json.dumps(new, indent=2))
        except Exception as ex:
            print(ex)
        file = discord.File("Cache/allcosmetics.json")
        try:
            await ctx.send(f"All Cosmetics:", file=file)
        except Exception as ex:
            await ctx.send(ex)

    @commands.command()
    async def newcosmetics(self, ctx):
        await self.client.wait_until_ready()
        msg = await ctx.send("Which type do you want?\n\n:one: - Json file\n:two: - Embed in Discord")
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        payload = await self.client.wait_for("raw_reaction_add", timeout=60,
                                             check=lambda p: p.user_id == ctx.author.id and p.message_id == msg.id)
        await msg.delete()
        if str(payload.emoji) == "1️⃣":
            try:
                async with aiohttp.ClientSession() as cs:
                    async with cs.get('https://benbotfn.tk/api/v1/newCosmetics') as data:
                        new = await data.json()
                        await (await aiofiles.open('Cache/newcosmetics.json', mode='w+')).write(
                            json.dumps(new, indent=2))
            except Exception as ex:
                print(ex)
                return await ctx.send("Error" + str(ex))
            file = discord.File("Cache/newcosmetics.json")
            try:
                await ctx.send(f"All new Cosmetics:", file=file)
            except Exception as ex:
                await ctx.send(ex)
        else:
            try:
                async with aiohttp.ClientSession() as cs:
                    async with cs.get('https://benbotfn.tk/api/v1/newCosmetics') as data:
                        new = await data.json()
            except Exception as ex:
                print(ex)
                return await ctx.send("Error" + str(ex))
            for i in new["items"]:
                embed = discord.Embed(color=Settings.SETTINGS.embedcolor)
                embed.set_author(name=i["name"])
                embed.set_thumbnail(url=i["icons"]["icon"])
                embed.add_field(name="Description", value=i["description"], inline=False)
                id = i["id"]
                embed.add_field(name="ID:", value=f"{id}\n**({len(id)})**", inline=False)
                embed.add_field(name="Type", value=i["backendType"], inline=False)
                embed.add_field(name="Rarity", value=i["rarity"], inline=False)
                temp = i["gameplayTags"]
                embed.add_field(name="gameplayTags", value=f"```json\n{str(temp)}```", inline=False)
                temp = i["path"]
                embed.add_field(name="Path", value=f"```json\n{temp}```", inline=False)
                await ctx.author.send(embed=embed)


def setup(client):
    client.add_cog(cosmetics(client))

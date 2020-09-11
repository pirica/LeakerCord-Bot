import asyncio
import math
import os
import random
import sys
import traceback

import aiofiles
import aiohttp
import discord
from PIL import Image
from discord.ext import commands

from Settings import SETTINGS, book

client = commands.Bot(command_prefix=[".", "-", ">"])  # , shard_count=3)
client.remove_command("help")


async def check(ctx):
    if ctx.author.id == 640235175007223814:
        return True
    else:
        return False


@client.command()
@commands.has_role(741331981857587341)
async def refresh(ctx):
    try:
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        os.system("git fetch")
        await ctx.send("Successfull downloaded the Bot. Restarting now...")
        os.system("service leaker restart")
    except Exception as ex:
        await ctx.send(ex)


@client.command()
async def export(ctx, path: str):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://benbotfn.tk/api/v1/exportAsset?path={path}") as response:
            if response.status == 404:
                return await ctx.send("I cannot find this.")
            if response.status != 200:
                return await ctx.send(str(response.status) + ": Error")
            if response.status == 200:
                with open(f"response.{str(response.content_type).split('/')[1]}", "wb") as f:
                    f.write(await response.read())
                file = discord.File(f"response.{str(response.content_type).split('/')[1]}")
                await ctx.send(file=file)


@client.command(aliases=["export_p", "exportp"])
async def export_properties(ctx, path: str):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://benbotfn.tk/api/v1/assetProperties?path={path}") as response:
            if response.status == 404:
                return await ctx.send("I cannot find this.")
            if response.status != 200:
                return await ctx.send(str(response.status) + ": Error")
            if response.status == 200:
                with open(f"response.{str(response.content_type).split('/')[1]}", "wb") as f:
                    f.write(await response.read())
                file = discord.File(f"response.{str(response.content_type).split('/')[1]}")
                await ctx.send(file=file)


@client.command(aliases=["find"])
async def searchpath(ctx, path: str):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://benbotfn.tk/api/v1/files/search?path={path}&matchMethod=contains") as response:
            if response.status == 404:
                return await ctx.send("I cannot find this.")
            if response.status != 200:
                return await ctx.send(str(response.status) + ": Error")
            if response.status == 200:
                new = await response.json()
                if new is []:
                    return await ctx.send("I cannot find this.")
                string = ""
                for i in new:
                    string += i + "\n"
                pages = book.TextPages(ctx, string)
                await pages.paginate()


@client.command()
async def map(ctx):
    embeds = []
    embed = discord.Embed(color=SETTINGS.embedsuccess, title=f"Fortnite-Map (Fortniteapi.io)")
    embed.set_image(url="https://media.fortniteapi.io/images/map.png")
    embed.set_footer(text="Click on the Image to load the new image.")
    embeds.append(embed)
    embed = discord.Embed(color=SETTINGS.embedsuccess, title=f"Fortnite-Map (Fortnite-API.com)")
    embed.set_image(url="https://fortnite-api.com/images/br/map.png")
    embed.set_footer(text="Click on the Image to load the new image.")
    embeds.append(embed)
    await ctx.send(embeds=embeds)


@client.event
async def on_ready():
    if SETTINGS.test is True:
        await client.change_presence(activity=discord.Game(name="in the Testarea"))
    else:
        await client.change_presence(activity=discord.Game(name="made by @AcNono_"))
    print("Discord Client ready")
    channel = client.get_channel(748885612777701386)
    await channel.send("Leaker Bot is now ready")


for cogpath in os.listdir("cogs"):
    try:
        if cogpath.endswith(".py"):
            client.load_extension(f'cogs.{cogpath[:-3]}')
            print(f'Loaded {cogpath}')
    except Exception as ex:
        print(f'Something wen\'t wrong while loading {cogpath}\nError: {ex}\n\n')


@client.command(aliases=["disable"])
@commands.check(check)
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.message.channel.send(f"Unloaded {extension}", delete_after=7)


@client.command(aliases=["enable"])
@commands.check(check)
async def load(ctx, extension=None):
    client.load_extension(f"cogs.{extension}")
    await ctx.message.channel.send(f"Loaded {extension}", delete_after=7)


@client.command()
@commands.check(check)
async def reload(ctx, extension):
    client.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Reloaded {extension}", delete_after=7)


@client.command(aliases=["updatecogs"])
@commands.check(check)
async def reloadall(ctx):
    embed = discord.Embed(title=f"__cog System__", description=f"**I refreshed the following cogs:**", color=0x1df221)
    errors = []
    try:
        for cog in os.listdir('cogs'):
            if cog.endswith(".py"):
                client.unload_extension(f"cogs.{cog[:-3]}")
        await asyncio.sleep(1)
        for cog in os.listdir('cogs'):
            if cog.endswith(".py"):
                client.load_extension(f"cogs.{cog[:-3]}")
                embed.add_field(name=f"``{cog}``", value=f"--------")
    except Exception as ex:
        print(ex)
        errors.append(ex)
    if errors:
        str = ""
        for i in errors:
            str += f"{i}\n"
        await embed.add_field(name=f"Errors:", value=f"{str}")
    await ctx.send(embed=embed, delete_after=15)


@client.command()
@commands.check(check)
async def cogs(ctx):
    embed = discord.Embed(title=f"Cog System", description=f"Cogs:")
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            embed.add_field(name=f"``{filename}``", value="--------------", inline=False)
    await ctx.send(embed=embed)


loop = asyncio.get_event_loop()
loop.create_task(client.start(SETTINGS.TOKEN, bot=True))
try:
    loop.run_forever()
finally:
    loop.stop()

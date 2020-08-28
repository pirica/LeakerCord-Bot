import argparse
import shlex

import aiohttp
import discord
from discord.ext import commands

import Settings.SETTINGS
import book


class Arguments(argparse.ArgumentParser):
    def error(self, message):
        raise RuntimeError(message)


class searchcosmetic(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def searchcosmetic(self, ctx, *, args: str = None):
        if args is not None:
            parser = Arguments(add_help=False, allow_abbrev=False)
            parser.add_argument('-name', nargs='+')
            parser.add_argument('-lang', nargs='+')
            parser.add_argument('-rarity', nargs='+')
            parser.add_argument('-unseenFor', nargs='+')
            parser.add_argument('-id', nargs='+')
            # https://fortnite-api.com/v2/cosmetics/br/search/all
            try:
                args = parser.parse_args(shlex.split(args))
            except Exception as e:
                await ctx.send(str(e))
                return

            parameter = "?"

            if args.name:
                name = ""
                for i in args.name:
                    if i != args.name[len(args.name) - 1]:
                        name += f"{i}+"
                    else:
                        name += f"{i}"
                parameter += f"&name={name}"

            if args.lang:
                parameter += f"&language={args.lang[0].lower()}"

            if args.rarity:
                parameter += f"&rarity={args.rarity[0].lower()}"

            if args.unseenFor:
                parameter += f"&unseenFor={args.unseenFor[0].lower()}"

            if args.id:
                parameter += f"&id={args.id[0].lower()}"

            async with aiohttp.ClientSession() as session:
                async with session.get(
                        url=f"https://fortnite-api.com/v2/cosmetics/br/search{parameter}&matchMethod=contains") as response:
                    jsondata = await response.json()
                    print(response.status)
                    print(jsondata)
                    if response.status == 404:
                        return await ctx.send(f"Item not found.\n```txt\n" + jsondata["error"] + "```")
                    elif response.status == 200:
                        i = jsondata["data"]
                        embed = discord.Embed(color=Settings.SETTINGS.embedcolor)
                        embed.set_author(name=i["name"])
                        try:
                            embed.set_thumbnail(url=i["images"]["icon"])
                        except:
                            try:
                                embed.set_thumbnail(url=i["images"]["smallIcon"])
                            except:
                                try:
                                    embed.set_thumbnail(url=i["images"]["featured"])
                                except:
                                    try:
                                        embed.set_thumbnail(url=i["images"]["other"])
                                    except:
                                        pass
                        try:
                            embed.add_field(name="ID:", value=i["id"] + " (**" + str(len(i["id"])) + "**)",
                                            inline=False)
                        except:
                            pass
                        try:
                            embed.add_field(name="Description:", value=i["description"], inline=False)
                        except:
                            pass
                        try:
                            embed.add_field(name="Rarity:", value=i["rarity"]["displayValue"], inline=False)
                        except:
                            pass
                        try:
                            embed.add_field(name="Introduction:", value=i["introduction"]["text"], inline=False)
                        except:
                            pass
                        try:
                            hist = "```\n"
                            for i2 in i["shopHistory"]:
                                i2 = i2.split("T")
                                i2 = i2[0].split("-")
                                hist += f"{i2[2]}.{i2[1]}.{i2[0]}\n"
                            hist += "```"
                            embed.add_field(name="shopHistory", value=hist, inline=False)
                        except:
                            pass
                        variants = False
                        try:
                            if i["variants"]:
                                variants = True
                        except Exception as ex:
                            print(ex)
                            pass
                        if variants is True:
                            embed.set_footer(text="React with the Check Button to see the Variants.")

                        msg = await ctx.send(embed=embed)
                        if variants is True:
                            await msg.add_reaction("✅")
                            p = await self.client.wait_for("raw_reaction_add", timeout=120,
                                                           check=lambda p: p.user_id == ctx.author.id and str(
                                                               p.emoji) == "✅" and p.channel_id == ctx.channel.id)
                            var = ""
                            if i["variants"]:
                                for i2 in i["variants"]:
                                    mainname = i2["type"].lower()
                                    var += f"{mainname}\n"
                                    for i3 in i2["options"]:
                                        name = i3["name"]
                                        image = i3["image"]
                                        var += f"{name}:\n{image}\n\n"
                                    var += "\n\n"
                            pages = book.TextPages(ctx, var)
                            await pages.paginate()
                        return
                    else:
                        await ctx.send(
                            f"Error\n" + str(jsondata["status"]) + "\n```txt\n" + jsondata["error"] + "```")
                        return
        else:
            await ctx.send(
                "Please give me a valid Argument.\n\n```s!search -name Renegade Raider -lang en -rarity "
                "epic -unseenFor 120```")


def setup(client):
    client.add_cog(searchcosmetic(client))

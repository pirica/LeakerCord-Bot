import asyncio
import json

import aiomysql
import discord
import tweepy
from discord.ext import commands

from Settings import SETTINGS


class twitterbot(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not isinstance(payload, discord.RawReactionActionEvent):
            pass
        if not isinstance(self.client, discord.ext.commands.Bot):
            pass
        if payload.channel_id == 742817471286738955 and payload.message_id == 742818510320959509:
            user = self.client.get_user(payload.user_id)

            myuser = await aiomysql.connect(host='peely.de', port=3306,
                                            user='new', password='NonoDEV3011@@', db='peely',
                                            autocommit=True)
            mydb = await myuser.cursor()
            await mydb.execute("SET NAMES utf8mb4")
            await mydb.execute("SELECT * from twittersettings WHERE userid=%s", (user.id,))
            data = await mydb.fetchone()
            await myuser.commit()
            await mydb.close()
            myuser.close()
            if not data:

                msg = await user.send(embed=discord.Embed(color=SETTINGS.embedcolor, title=f"Twitter Bot Configurator",
                                                          description=f"Do you have already a own Twitter Developer App? (https://developer.twitter.com/en/apps)"))
                await msg.add_reaction("✅")
                await msg.add_reaction("❌")
                r, u = await self.client.wait_for("reaction_add",
                                                  check=lambda r, u: u.id == user.id and r.message.id == msg.id)
                if str(r.emoji) == "❌":
                    return await user.send(embed=discord.Embed(color=SETTINGS.embederror,
                                                               description=f"You need to have a Developer Account and a App."))
                else:
                    msg = await user.send(embed=discord.Embed(color=SETTINGS.embedsuccess,
                                                              description=f"You need your foure API Keys. Do you have them ready?"))
                    await msg.add_reaction("✅")
                    await msg.add_reaction("❌")
                    r, u = await self.client.wait_for("reaction_add",
                                                      check=lambda r, u: u.id == user.id and r.message.id == msg.id)
                    if str(r.emoji) == "❌":
                        return await user.send(embed=discord.Embed(color=SETTINGS.embederror,
                                                                   description=f"You need your API Keys ready."))
                    else:
                        await user.send(
                            embed=discord.Embed(color=SETTINGS.embedcolor,
                                                description="Please send me now your API key"))
                        apikey = (await self.client.wait_for("message", check=lambda m: m.author.id == user.id)).content
                        await user.send(embed=discord.Embed(color=SETTINGS.embedcolor,
                                                            description="Please send me now your API secret key"))
                        apisecretkey = (
                            await self.client.wait_for("message", check=lambda m: m.author.id == user.id)).content
                        await user.send(embed=discord.Embed(color=SETTINGS.embedcolor,
                                                            description="Please send me now your API Access token"))
                        apiaccesstoken = (
                            await self.client.wait_for("message", check=lambda m: m.author.id == user.id)).content
                        await user.send(embed=discord.Embed(color=SETTINGS.embedcolor,
                                                            description="Please send me now your API Access token secret"))
                        apiaccesstokensecret = (
                            await self.client.wait_for("message", check=lambda m: m.author.id == user.id)).content
                        try:
                            myuser = await aiomysql.connect(host='peely.de', port=3306,
                                                            user='new', password='NonoDEV3011@@', db='peely',
                                                            autocommit=True)
                            mydb = await myuser.cursor()
                            await mydb.execute("SET NAMES utf8mb4")
                            await mydb.execute("DELETE FROM twitteruser WHERE userid=%s", (user.id,))
                            await mydb.execute("INSERT INTO twitteruser VALUE (%s, %s, %s, %s, %s)",
                                               (user.id, apikey, apisecretkey, apiaccesstoken, apiaccesstokensecret))
                            await myuser.commit()
                            await mydb.close()
                            myuser.close()
                            await user.send(
                                embed=discord.Embed(color=SETTINGS.embedcolor,
                                                    description="Your Bot was sucessfull registered. "
                                                                "Setup it with >settings in the Leaker Cord")
                            )

                        except tweepy.error.TweepError as ex:
                            return await user.send(embed=discord.Embed(color=SETTINGS.embederror,
                                                                       description=f"Failed to login into your "
                                                                                   f"Twitter Account. {ex}"))
            else:
                msg = await user.send(embed=discord.Embed(color=SETTINGS.embederror,
                                                          description="You have already a Bot. Do you want to delete it?"))
                await msg.add_reaction("✅")
                await self.client.wait_for("reaction_add", timeout=120,
                                           check=lambda p, u: u.id == user.id)
                try:
                    myuser = await aiomysql.connect(host='peely.de', port=3306,
                                                    user='new', password='NonoDEV3011@@', db='peely',
                                                    autocommit=True)
                    mydb = await myuser.cursor()
                    await mydb.execute("SET NAMES utf8mb4")
                    await mydb.execute("DELETE from twittersettings WHERE userid=%s", (user.id,))
                    await mydb.execute("DELETE from twitteruser WHERE userid=%s", (user.id,))
                    await myuser.commit()
                    await mydb.close()
                    myuser.close()
                    await user.send(embed=discord.Embed(color=SETTINGS.embedsuccess,
                                                        description="Deleted your Twitter Bot."), delete_after=15)
                except:
                    await msg.delete()

    async def save(self, ctx, settings):
        print(f"Save, {ctx.author.name}")
        myuser = await aiomysql.connect(host='peely.de', port=3306,
                                        user='new', password='NonoDEV3011@@', db='peely',
                                        autocommit=True)
        mydb = await myuser.cursor()
        await mydb.execute("SET NAMES utf8mb4")
        await mydb.execute("DELETE from twittersettings WHERE userid=%s", (ctx.author.id,))
        await mydb.execute("INSERT INTO twittersettings VALUE (%s, %s)", (str(settings), ctx.author.id,))
        await myuser.commit()
        await mydb.close()
        myuser.close()
        return

    @commands.command()
    async def settings(self, ctx):
        if self.client.get_guild(741330991863562383).get_role(741335249778114681) in ctx.author.roles:
            myuser = await aiomysql.connect(host='peely.de', port=3306,
                                            user='new', password='NonoDEV3011@@', db='peely',
                                            autocommit=True)
            mydb = await myuser.cursor()
            await mydb.execute("SET NAMES utf8mb4")
            await mydb.execute("SELECT * from twittersettings WHERE userid=%s", (ctx.author.id,))
            data = await mydb.fetchone()
            await myuser.commit()
            await mydb.close()
            myuser.close()
            if not data:
                settings = {
                    "background_url": "https://img.freepik.com/vektoren-kostenlos/hintergrund-mit-farbverlauf-in-gruentoenen_23-2148363157.jpg?size=626&ext=jpg",
                    "sac": "",
                    "leaks": "False",
                    "shop": "False",
                    "news": "False",
                    "staging": "False",
                    "blogposts": "False",
                    "bugmessage": "False",
                    "featuredislands": "False"
                }
            else:
                string = str(data[0]).replace("'", "\"")
                settings = json.loads(string)
            while True:
                await self.save(ctx, settings)
                embed = discord.Embed(color=SETTINGS.embedcolor, title="Settings for your Twitter Bot",
                                      description=f"1️⃣ Leaks = {settings['leaks']}\n"
                                                  f"2️⃣ Shop = {settings['shop']}\n"
                                                  f"3️⃣ News Feed = {settings['news']}\n"
                                                  f"4️⃣ Staging Server = {settings['staging']}\n"
                                                  f"5️⃣ Blogposts = {settings['blogposts']}\n"
                                                  f"6️⃣ Bug-Message = {settings['bugmessage']}\n"
                                                  f"7️⃣ Featured Islands = {settings['featuredislands']}")
                embed.set_footer(text="React with the right Icon, to change the Settings.")
                try:
                    await msg.edit(embed=embed)
                except:
                    msg = await ctx.send(embed=embed)
                await msg.add_reaction("1️⃣")
                await msg.add_reaction("2️⃣")
                await msg.add_reaction("3️⃣")
                await msg.add_reaction("4️⃣")
                await msg.add_reaction("5️⃣")
                await msg.add_reaction("6️⃣")
                await msg.add_reaction("7️⃣")
                try:
                    payload, user_p = await self.client.wait_for("reaction_add", timeout=120,
                                                                 check=lambda p, u: u.id == ctx.author.id)
                except asyncio.TimeoutError:
                    try:
                        await msg.clear_reactions()
                    except:
                        pass
                    await self.save(ctx, settings)
                    return
                if str(payload.emoji) in SETTINGS.liste.values():
                    for i in SETTINGS.liste:
                        if SETTINGS.liste[i] == str(payload.emoji):
                            key = "leaks"
                            if i == "one":
                                key = "leaks"
                            elif i == "two":
                                key = "shop"
                            elif i == "three":
                                key = "news"
                            elif i == "four":
                                key = "staging"
                            elif i == "five":
                                key = "blogposts"
                            elif i == "six":
                                key = "bugmessage"
                            elif i == "seven":
                                key = "featuredislands"
                            try:
                                await msg.clear_reactions()
                            except:
                                pass
                            await msg.edit(embed=discord.Embed(color=SETTINGS.embedcolor,
                                                               description=f"Do you want to enable (🟢) or disable (🔴) this Feature?"))
                            await msg.add_reaction("🟢")
                            await msg.add_reaction("🔴")
                            try:
                                payload, user_p = await self.client.wait_for("reaction_add", timeout=120,
                                                                             check=lambda p, u: u.id == ctx.author.id)
                                await msg.clear_reactions()
                            except asyncio.TimeoutError:
                                await msg.clear_reactions()
                                await self.save(ctx, settings)
                                return
                            if str(payload.emoji) == "🔴":
                                settings[key] = "False"
                            else:
                                settings[key] = "True"
                            await msg.edit(embed=discord.Embed(color=SETTINGS.embedcolor,
                                                               description=f"The System was successfully changed to **{settings[key]}**"),
                                           delete_after=10)
                            await msg.add_reaction("↩️")
                            try:
                                payload, user_p = await self.client.wait_for("reaction_add", timeout=120,
                                                                             check=lambda p, u: u.id == ctx.author.id)
                                await msg.clear_reactions()
                            except asyncio.TimeoutError:
                                await msg.clear_reactions()
                                await self.save(ctx, settings)
                                return
                await self.save(ctx, settings)
        else:
            await ctx.send(
                embed=discord.Embed(color=SETTINGS.embederror, description="You dont have Permissions to create a Bot"))


def setup(client):
    client.add_cog(twitterbot(client))

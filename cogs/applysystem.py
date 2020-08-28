import discord
from discord.ext import commands

import Settings.SETTINGS


class applysystem(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not isinstance(payload, discord.RawReactionActionEvent):
            pass
        if not isinstance(self.client, discord.ext.commands.Bot):
            pass
        if payload.channel_id == 742371054558773268 and payload.message_id == 742687706907410468:
            guild = self.client.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            await user.send(embed=discord.Embed(color=Settings.SETTINGS.embedcolor,
                                                title="Leaker Application",
                                                description=
                                                f"""Hello {user.name},
Please send me your Social Media Account Links.
"""))
            ans = await self.client.wait_for("message", check=lambda m: m.author.id == user.id)
            await user.send(embed=discord.Embed(color=Settings.SETTINGS.embedsuccess,
                                                title="Leaker Application",
                                                description=f"Thank you, for your time. We will check your Accounts soon"))
            channel = self.client.get_channel(742809662814027777)
            await channel.send(
                embed=discord.Embed(color=Settings.SETTINGS.embedcolor, title=f"New Leaker Application",
                                    description=f"{user.name}#{user.discriminator} | {user.mention}\n\n{ans.content}"))

    @commands.command()
    async def accept(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.send("Please tag a Member")
        await member.send(embed=discord.Embed(color=Settings.SETTINGS.embedsuccess, title="Leaker Application",
                                              description=f"You are now Leaker on the {ctx.guild.name} Discord"))
        await member.add_roles(ctx.guild.get_role(741335249778114681))
        await ctx.send(embed=discord.Embed(color=Settings.SETTINGS.embedsuccess,
                                           description=f"Sucessfull added {member.name} the Role(s)"))

    @commands.command(aliases=["reject"])
    async def decline(self, ctx, member: discord.Member = None, *, reason: str = None):
        if member is None:
            return await ctx.send("Please tag a Member")
        await member.send(embed=discord.Embed(color=Settings.SETTINGS.embederror, title="Leaker Application",
                                              description=f"You don't meet our requirements\n\n{reason}"))
        await ctx.send(
            embed=discord.Embed(color=Settings.SETTINGS.embedsuccess, description=f"Sucessfull rejected {member.name}"))


def setup(client):
    client.add_cog(applysystem(client))

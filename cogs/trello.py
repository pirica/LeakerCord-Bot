import json

import traceback
from datetime import datetime

import aiofiles
import aiohttp
import discord
from discord.ext import commands, tasks

from Settings import SETTINGS


class trello(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.check.start()
        except Exception as ex:
            print(ex)
            self.check.stop()
            self.check.start()

    @tasks.loop(seconds=30)
    async def check(self):
        old = json.loads(
            await (await aiofiles.open('Cache/trello.json', encoding="cp437", errors='ignore', mode='r')).read())
        async with aiohttp.ClientSession() as session:
            async with session.get("https://trello.com/1/Boards/Bs7hgkma?lists=open&list_fields=name%2Cclosed%2CidBoard%2Cpos%2Csubscribed%2Climits%2CcreationMethod%2CsoftLimit&cards=visible&card_attachments=cover&card_stickers=true&card_fields=badges%2Cclosed%2CdateLastActivity%2Cdesc%2CdescData%2Cdue%2CdueComplete%2CdueReminder%2CidAttachmentCover%2CidList%2CidBoard%2CidMembers%2CidShort%2CidLabels%2Climits%2Cname%2Cpos%2CshortUrl%2CshortLink%2Csubscribed%2Curl%2ClocationName%2Caddress%2Ccoordinates%2Ccover%2CisTemplate%2Cstart%2Clabels&card_checklists=none&enterprise=true&enterprise_fields=displayName&members=all&member_fields=activityBlocked%2CavatarUrl%2Cbio%2CbioData%2Cconfirmed%2CfullName%2CidEnterprise%2CidMemberReferrer%2Cinitials%2CmemberType%2CnonPublic%2Cproducts%2Curl%2Cusername&membersInvited=all&membersInvited_fields=activityBlocked%2CavatarUrl%2Cbio%2CbioData%2Cconfirmed%2CfullName%2CidEnterprise%2CidMemberReferrer%2Cinitials%2CmemberType%2CnonPublic%2Cproducts%2Curl%2Cusername&memberships_orgMemberType=true&checklists=none&organization=true&organization_fields=name%2CdisplayName%2Cdesc%2CdescData%2Curl%2Cwebsite%2Cprefs%2Cmemberships%2ClogoHash%2Cproducts%2Climits%2CidEnterprise&organization_tags=true&organization_enterprise=true&organization_disable_mock=true&myPrefs=true&fields=name%2Cclosed%2CdateLastActivity%2CdateLastView%2CdatePluginDisable%2CenterpriseOwned%2CidOrganization%2Cprefs%2CpremiumFeatures%2CshortLink%2CshortUrl%2Curl%2CcreationMethod%2CidEnterprise%2Cdesc%2CdescData%2CidTags%2Cinvitations%2Cinvited%2ClabelNames%2Climits%2Cmemberships%2CpowerUps%2Csubscribed%2CtemplateGallery&pluginData=true&organization_pluginData=true") as response:
                new = await response.json()
        await (await aiofiles.open('Cache/trello.json', encoding="cp437", errors='ignore', mode='w+')).write(
            json.dumps(new, indent=2))
        for i in new["cards"]:
            already = False
            for i2 in old["cards"]:
                if i["dateLastActivity"] == i2["dateLastActivity"]:
                    already = True
            if already is False:
                embed = discord.Embed(
                    color=SETTINGS.embedcolor, title=i["name"])
                try:
                    embed.add_field(name=f"Last Activity: {i['dateLastActivity'].split('T')[0]}\n\n",
                                    value=f"{i['desc']}")
                except:
                    pass
                try:
                    embed.add_field(
                        name="Tags:", value=f"{i['labels'][0]['name']}, {i['labels'][1]['name']}")
                except:
                    pass
                try:
                    embed.add_field(
                        name="Link:", value=f"{i['shortUrl']}")
                except:
                    pass
                await self.client.get_channel(742373428345962567).send(embed=embed)

    def cog_unload(self):
        self.check.stop()
        try:
            self.client.unload_extension("cogs.fn-trello")
        except:
            pass
        try:
            self.client.load_extension("cogs.fn-trello")
        except:
            pass


def setup(client):
    client.add_cog(trello(client))

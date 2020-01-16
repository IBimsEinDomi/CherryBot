""""
MIT License

Copyright (c) 2020 Dominik Büttner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import discord
from discord.ext import commands
import datetime
from pytz import timezone
import traceback
import random
import asyncio
from config import CONFIG, SV_NEWS
from config.GAMES import __games__, __gamesTimer__
import codecs

client = discord.Client()
__version__ = '0.4.5.1'
mit_license = codecs.open(".\config\MIT_license", "r", encoding="utf-8")


@client.event
async def on_ready():
    if client.user.id == 664831660235292714:
        client.dev = "Aktiviert"
    else:
        client.dev = "Deaktiviert"
    client.gamesLoop = asyncio.ensure_future(_randomGame())
    print("Der Bot wurde aktiviert")
    print(f'Bot Name: {client.user.name}')
    print(f'Discord Version: {discord.__version__}')
    print(f'Bot Version: {__version__}')
    client.AppInfo = await client.application_info()
    print(f'Owner: {client.AppInfo.owner}')


@client.event
async def on_error(event, *args, **kwargs):
    if client.dev:
        traceback.print_exc()
    else:
        embed = discord.Embed(title=':x: Event Fehler', colour=0xe74c3c)  # Red
        embed.add_field(name='Event', value=event)
        embed.description = '```py\n%s\n```' % traceback.format_exc()
        embed.timestamp = datetime.datetime.utcnow()
        try:
            await client.AppInfo.owner.send(embed=embed)
        except:
            pass


@client.event
async def _randomGame():
    while True:
        guildCount = len(client.guilds)
        memberCount = len(list(client.get_all_members()))
        randomGame = random.choice(__games__)
        await client.change_presence(activity=discord.Activity(type=randomGame[0],
                                                               name=randomGame[1].format(guilds=guildCount,
                                                                                         members=memberCount)))
        await asyncio.sleep(random.choice(__gamesTimer__))
        if CONFIG.clientLogout == True:
            await client.change_presence(status=discord.Status.do_not_disturb,
                                         activity=discord.Game(name="Bot deaktiviert"))
            break


def _currenttime():
    return datetime.datetime.now(timezone('Europe/Berlin')).strftime('%H:%M:%S')


@client.event
async def on_guild_join(guild):
    embed = discord.Embed(title=':white_check_mark: Zum Server hinzugefügt', color=0x2ecc71,
                          description="Server Name: " + str(guild.name) +
                                      "\nServer ID: " + str(guild.id) +
                                      "\nServer Besitzer: " + str(guild.owner.mention) +
                                      "\nServer Region: " + str(guild.region))
    embed.add_field(name="Mitglieder", value=str(guild.member_count) + " Mitglieder")
    CreateDateYear = str(guild.created_at)[0:4]
    CreateDateMonth = str(guild.created_at)[5:7]
    CreateDateDay = str(guild.created_at)[8:10]
    CreateDateTime = str(guild.created_at)[11:16]
    embed.add_field(name="Erstellt am",
                    value=CreateDateDay + "." + CreateDateMonth + "." + CreateDateYear + " um " + CreateDateTime + " Uhr")
    embed.set_thumbnail(url=guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()
    await client.AppInfo.owner.send(embed=embed)


@client.event
async def on_guild_remove(guild):
    embed = discord.Embed(title=':x: Vom Server entfernt', color=0xe74c3c,
                          description="Server Name: " + str(guild.name) +
                                      "\nServer ID: " + str(guild.id) +
                                      "\nServer Besitzer: " + str(guild.owner.mention) +
                                      "\nServer Region: " + str(guild.region))
    embed.add_field(name="Mitglieder", value=str(guild.member_count) + " Mitglieder")
    CreateDateYear = str(guild.created_at)[0:4]
    CreateDateMonth = str(guild.created_at)[5:7]
    CreateDateDay = str(guild.created_at)[8:10]
    CreateDateTime = str(guild.created_at)[11:16]
    embed.add_field(name="Erstellt am",
                    value=CreateDateDay + "." + CreateDateMonth + "." + CreateDateYear + " um " + CreateDateTime + " Uhr")
    embed.set_thumbnail(url=guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()
    await client.AppInfo.owner.send(embed=embed)


@client.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        if message.author.id == client.AppInfo.owner.id:
            if message.content.startswith(CONFIG.PREFIX + "sv-id"):
                if len(message.content) == 25:
                    serverID = message.content[7:25]
                    if str.isdigit(serverID):
                        if client.get_guild(int(serverID)):
                            guildWithID = client.get_guild(int(serverID))
                            if guildWithID.id in CONFIG.SupportLicenseServer:
                                serverLicense = "Unterstützer Lizenz"
                            elif guildWithID.id in CONFIG.AllowedServer:
                                serverLicense = "Standard Lizenz"
                            else:
                                serverLicense = "Keine Lizenz"
                            embed = discord.Embed(title=':white_check_mark: Server gefunden', color=0x2ecc71,
                                                  description="Server Name: " + str(guildWithID.name) +
                                                              "\nServer ID: " + str(guildWithID.id) +
                                                              "\nServer Besitzer: " + str(guildWithID.owner.mention) +
                                                              "\nServer Region: " + str(guildWithID.region) +
                                                              "\nLizenz: " + serverLicense)
                            embed.add_field(name="Mitglieder", value=str(guildWithID.member_count) + " Mitglieder")
                            CreateDateYear = str(guildWithID.created_at)[0:4]
                            CreateDateMonth = str(guildWithID.created_at)[5:7]
                            CreateDateDay = str(guildWithID.created_at)[8:10]
                            CreateDateTime = str(guildWithID.created_at)[11:16]
                            embed.add_field(name="Erstellt am",
                                            value=CreateDateDay + "." + CreateDateMonth + "." + CreateDateYear + " um " + CreateDateTime + " Uhr")
                            embed.set_thumbnail(url=guildWithID.icon_url)
                            embed.timestamp = datetime.datetime.utcnow()
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                        else:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(":x: Dieser Server existiert nicht, "
                                                       "oder ich bin auf diesem Server nicht autorisiert!")
                    else:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(":x: Bitte benutze **" + CONFIG.PREFIX + "sv-id [ServerID]**")
                elif len(message.content) != 25:
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(":x: Bitte benutze **" + CONFIG.PREFIX + "sv-id [ServerID]**")

            if message.content.startswith(CONFIG.PREFIX + 'stop'):
                if CONFIG.clientLogout == False:
                    embed = discord.Embed(title="", description="Der Bot wird deaktiviert...", color=0xe74c3c)
                    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Bot deaktiviert"))
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(embed=embed)
                    CONFIG.clientLogout = True
                else:
                    embed = discord.Embed(title="", description=":x: Der Bot ist schon deaktiviert", color=0xff0000)
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(embed=embed)
            if message.content.startswith(CONFIG.PREFIX + 'login'):
                if CONFIG.clientLogout == True:
                    embed = discord.Embed(title="", description="Der Bot wird aktiviert...", color=0x2ecc71)
                    client.gamesLoop = asyncio.ensure_future(_randomGame())
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(embed=embed)
                    CONFIG.clientLogout = False
                else:
                    embed = discord.Embed(title="", description=":x: Das geht nur, wenn der Bot deaktiviert ist", color=0xff0000)
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="", description=":x: Hey, ich bin nur ein Bot und kann noch nicht darauf antworten", color=0xff0000)
            if not message.author.bot:
                await message.channel.trigger_typing()
                await asyncio.sleep(0.5)
                await message.author.send(embed=embed)

    else:
        if message.guild.id in CONFIG.AllowedServer:
            if message.content.startswith(CONFIG.PREFIX + 'stop'):
                client.AppInfo = await client.application_info()
                if message.author.id == client.AppInfo.owner.id:
                    if CONFIG.clientLogout == False:
                        embed = discord.Embed(title="", description="Der Bot wird deaktiviert...", color=0xe74c3c)
                        await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Bot deaktiviert"))
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                        CONFIG.clientLogout = True
                    else:
                        embed = discord.Embed(title="", description=":x: Der Bot ist schon deaktiviert", color=0xff0000)
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title="", description=":x: Hey, dafür hast du keine Rechte!", color=0xff0000)
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(embed=embed)
            if message.content.startswith(CONFIG.PREFIX + 'login'):
                client.AppInfo = await client.application_info()
                if message.author.id == client.AppInfo.owner.id:
                    if CONFIG.clientLogout == True:
                        embed = discord.Embed(title="", description="Der Bot wird aktiviert...", color=0x2ecc71)
                        client.gamesLoop = asyncio.ensure_future(_randomGame())
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                        CONFIG.clientLogout = False
                    else:
                        embed = discord.Embed(title="", description=":x: Das geht nur, wenn der Bot deaktiviert ist", color=0xff0000)
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title="", description=":x: Hey, dafür hast du keine Rechte!", color=0xff0000)
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(embed=embed)

            if CONFIG.clientLogout == False:
                if message.content.startswith(CONFIG.PREFIX + 'sv-news'):
                    if message.guild.id in SV_NEWS.newsID:
                        patchChannelID = SV_NEWS.newsID.get(message.guild.id)[0:18]
                        patchMessageID = SV_NEWS.newsID.get(message.guild.id)[19:37]
                        try:
                            patchChannel = message.guild.get_channel(int(patchChannelID))
                            try:
                                patchMessage = await patchChannel.fetch_message(int(patchMessageID))
                                embed = discord.Embed(title="", description="", color=0x00ff00)
                                embed.add_field(name="Neuigkeiten", value=patchMessage.content, inline=False)
                                embed.set_footer(text="Server News von " + message.guild.name, icon_url=client.user.avatar_url, )
                                embed.set_thumbnail(url=message.guild.icon_url)
                                embed.timestamp = datetime.datetime.utcnow()
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(":x: Diese Nachricht wurde gelöscht!")
                        except:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(":x: Dieser Channel wurde gelöscht!")
                    else:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(":x: Es wurde keine Nachricht eingestellt!")

                if message.content.startswith(CONFIG.PREFIX + 'set-news'):
                    if message.author.guild_permissions.manage_guild:
                        if len(message.content) == 47:
                            channelID = message.content[10:28]
                            messageID = message.content[29:47]
                            if str.isdigit(channelID) & str.isdigit(messageID):
                                if message.guild.get_channel(int(channelID)):
                                    try:
                                        await message.guild.get_channel(int(channelID)).fetch_message(int(messageID))
                                        try:
                                            sv_news = open(".\config\SV_NEWS.py", "w")
                                            try:
                                                try:
                                                    SV_NEWS.newsID.pop(message.guild.id)
                                                    SV_NEWS.newsID.update({message.guild.id: str(channelID) + "(" + str(messageID) + ")"})
                                                    __newDictionary = SV_NEWS.newsID.copy()
                                                    __newDictionary = str(__newDictionary).replace("{", "{\n ")
                                                    __newDictionary = str(__newDictionary).replace(",", ",\n")
                                                    __newDictionary = str(__newDictionary).replace("}", "\n}")
                                                    sv_news.write("newsID = " + str(__newDictionary))
                                                    await message.channel.trigger_typing()
                                                    await asyncio.sleep(0.5)
                                                    await message.channel.send(":white_check_mark: Erfolgreich gesetzt")
                                                except:
                                                    SV_NEWS.newsID.update({message.guild.id: str(channelID) + "(" + str(messageID) + ")"})
                                                    __newDictionary = SV_NEWS.newsID.copy()
                                                    __newDictionary = str(__newDictionary).replace("{", "{\n ")
                                                    __newDictionary = str(__newDictionary).replace(",", ",\n")
                                                    __newDictionary = str(__newDictionary).replace("}", "\n}")
                                                    sv_news.write("newsID = " + str(__newDictionary))
                                                    await message.channel.trigger_typing()
                                                    await asyncio.sleep(0.5)
                                                    await message.channel.send(":white_check_mark: Erfolgreich gesetzt")
                                            except:
                                                await message.channel.trigger_typing()
                                                await asyncio.sleep(0.5)
                                                await message.channel.send(":x: Konfig konnte nicht gespeichert werden!")
                                        except:
                                            await message.channel.trigger_typing()
                                            await asyncio.sleep(0.5)
                                            await message.channel.send(":x: Datei wurde nicht gefunden!")
                                    except:
                                        await message.channel.trigger_typing()
                                        await asyncio.sleep(0.5)
                                        await message.channel.send(":x: Die Nachrichten-ID ist ungültig!")
                                else:
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(":x: Die Kanal-ID ist ungültig!")
                            else:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(":x: Bitte benutze **" + CONFIG.PREFIX + "set-news [Kanal-ID] [Nachrichten-ID]**")
                        else:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(":x: Bitte benutze **" + CONFIG.PREFIX + "set-news [Kanal-ID] [Nachrichten-ID]**")
                    else:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(":x: Keine Rechte!")

                if message.content.startswith(CONFIG.PREFIX + "bot-info"):
                    client.AppInfo = await client.application_info()
                    latency = str(client.latency)[0:4]
                    embed = discord.Embed(title="Bot Informationen",
                                          description="Bot-Name: " + client.user.name + "\nBot-ID: " + str(
                                              client.user.id) + "\nDev Mode: " + client.dev + "\nDiscord Version: " + str(
                                              discord.__version__) +
                                                      "\nBot Version: " + str(
                                              __version__) + "\nPing: " + latency + "ms" + "\nPrefix: **&**" + "\nBot Developer: " + str(
                                              client.AppInfo.owner.mention) + "\nBot-Sprache: :flag_de: German, Deutsch",
                                          color=0xffffff)
                    embed.set_thumbnail(url=client.user.avatar_url)
                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(embed=embed)

                if message.content.startswith(CONFIG.PREFIX + "sv-info"):
                    if message.guild.id in CONFIG.SupportLicenseServer:
                        serverLicense = "Unterstützer Lizenz"
                    elif message.guild.id in CONFIG.AllowedServer:
                        serverLicense = "Standard Lizenz"
                    else:
                        serverLicense = "Keine Lizenz"
                    client.AppInfo = await client.application_info()
                    embed = discord.Embed(title="Server Informationen",
                                          description="Server Name: " + str(message.guild.name) + "\nServer ID: " + str(
                                              message.guild.id) +
                                                      "\nServerbesitzer: " + str(
                                              message.guild.owner.mention) + "\nServer Region: " + str(
                                              message.guild.region) + "\nLizenz: " + str(serverLicense), color=0xffffff)
                    embed.add_field(name="Mitglieder", value=str(message.guild.member_count) + " Mitglieder")
                    CreateDateYear = str(message.guild.created_at)[0:4]
                    CreateDateMonth = str(message.guild.created_at)[5:7]
                    CreateDateDay = str(message.guild.created_at)[8:10]
                    CreateDateTime = str(message.guild.created_at)[11:16]
                    embed.add_field(name="Erstellt am",
                                    value=CreateDateDay + "." + CreateDateMonth + "." + CreateDateYear + " um " + CreateDateTime + " Uhr")
                    embed.set_footer(text="Server Info von " + message.guild.name, icon_url=client.user.avatar_url)
                    embed.set_thumbnail(url=message.guild.icon_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(embed=embed)

                if message.content.startswith(CONFIG.PREFIX + "whois"):
                    if len(message.content) == 6:
                        member = message.author
                    try:
                        if not len(message.content) == 6:
                            member = message.mentions[0]
                    except:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(":x: Bitte benutze **" + CONFIG.PREFIX + "whois <@User#1234>**")
                        return

                    __JoinPos__ = ""
                    if member.joined_at is None:
                        __JoinPos__ = "Ich konnte dein Beitrittdatum nicht feststellen"
                        return
                    __JoinPos__ = sum(
                        m.joined_at < member.joined_at for m in message.guild.members if m.joined_at is not None)
                    if __JoinPos__ == 0:
                        __JoinPos__ = "Besitzer"

                    AuthorGuildJoinDate = str(member.joined_at)[8:10] + "." + str(member.joined_at)[5:7] + "." + str(
                        member.joined_at)[0:4] + " um " + str(member.joined_at)[11:16] + " Uhr"
                    AuthorRegisterDate = str(member.created_at)[8:10] + "." + str(member.created_at)[5:7] + "." + str(
                        member.created_at)[0:4] + " um " + str(member.created_at)[11:16] + " Uhr"

                    role_name = [role.mention for role in member.roles]
                    role_list = ', '.join(role_name)[24:]
                    role_amount = role_list.count("@")
                    if len(role_list) <= 25:
                        role_list = "\n:x: Keine Rollen auf dem Server"

                    __AllPerms = ""
                    if member.guild_permissions.administrator:
                        __AllPerms += "Administrator, "
                    if member.guild_permissions.manage_guild:
                        __AllPerms += "Server verwalten, "
                    if member.guild_permissions.manage_webhooks:
                        __AllPerms += "Webhooks verwalten, "
                    if member.guild_permissions.manage_roles:
                        __AllPerms += "Rollen verwalten, "
                    if member.guild_permissions.manage_emojis:
                        __AllPerms += "Emojis verwalten, "
                    if member.guild_permissions.manage_channels:
                        __AllPerms += "Kanäle verwalten, "
                    if member.guild_permissions.manage_messages:
                        __AllPerms += "Nachrichten verwalten, "
                    if member.guild_permissions.ban_members:
                        __AllPerms += "Mitglieder bannen, "
                    if member.guild_permissions.kick_members:
                        __AllPerms += "Mitglieder kicken, "
                    if member.guild_permissions.manage_nicknames:
                        __AllPerms += "Nicknamen verwalten, "
                    if member.guild_permissions.change_nickname:
                        __AllPerms += "Nicknamen ändern"
                    if __AllPerms == "":
                        __AllPerms = ":x: Keine Rechte auf dem Server"
                    embed = discord.Embed(title="", description="Name: " + str(member.mention) +
                                                                "\nID: " + str(member.id) +
                                                                "\nBeigetreten: " + str(AuthorGuildJoinDate) +
                                                                "\nJoin Position: " + str(__JoinPos__) +
                                                                "\nRegistriert: " + str(AuthorRegisterDate) +
                                                                f'\nRollen [{role_amount}]: {role_list}' +
                                                                f' \nBerechtigungen: \n{__AllPerms}', color=0xffffff)
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_author(name=member, icon_url=member.avatar_url)
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(embed=embed)

                if message.content.startswith(CONFIG.PREFIX + "ping"):
                    latency = str(client.latency)[0:4]
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send("Bot Ping = " + latency + "ms")

                if message.content.startswith(CONFIG.PREFIX + "invite"):
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(message.author.mention + ", der Einladungslink wurde dir zugeschickt.")
                    embed = discord.Embed(title="", description="Hier kannst du mich zu deinem Server einladen:\n"
                                                                "http://bit.ly/361uYxI\n"
                                                                "\nBedenke aber das du eine Lizenz brauchst. Lizenzen kannst du bei **" + client.AppInfo.owner.mention + "** kaufen.",
                                          color=0xffffff)
                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    if not message.author.bot:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.author.send(embed=embed)

                if message.content.startswith(CONFIG.PREFIX + "src"):
                    embed = discord.Embed(title="", description="Hier findest du meinen Source Code:"
                                                                "\nhttps://github.com/IBimsEinMystery/ServerMod"
                                                                "\n\n**Dieser Source Code steht unter Lizenz:**"
                                                                "\n```" + mit_license.read() + "```", color=0xffffff)
                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await message.channel.trigger_typing()
                    await asyncio.sleep(0.5)
                    await message.channel.send(embed=embed)

                if message.content.startswith(CONFIG.PREFIX + "kick"):
                    if message.author.guild_permissions.kick_members:
                        try:
                            member = message.mentions[0]
                            try:
                                if not client.user.mentioned_in(member):
                                    try:
                                        if not message.guild.owner in message.mentions:
                                            try:
                                                await member.kick(reason=None)
                                                await message.channel.trigger_typing()
                                                await asyncio.sleep(0.5)
                                                await message.channel.send(":white_check_mark: Du hast **" + str(member) + "** gekickt")
                                            except:
                                                await message.channel.trigger_typing()
                                                await asyncio.sleep(0.5)
                                                await message.channel.send(":x: Ich darf das nicht!")
                                        else:
                                            await message.channel.trigger_typing()
                                            await asyncio.sleep(0.5)
                                            await message.channel.send(":x: Du kannst denn Besitzer dieses Servers nicht kicken!")
                                    except:
                                        await message.channel.trigger_typing()
                                        await asyncio.sleep(0.5)
                                        await message.channel.send(":x: Du kannst denn Besitzer dieses Servers nicht kicken!")
                                else:
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(":x: Ich kann mich nicht selber kicken!")
                            except:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(":x: Ich kann mich nicht selber kicken!")
                        except:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(":x: Bitte benutze **" + CONFIG.PREFIX + "kick [@User#1234]**!")
                    else:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(":x: Keine Rechte!")

            if client.user.mentioned_in(message) and message.mention_everyone is False:
                if not message.author.bot:
                    if message.content.startswith((CONFIG).PREFIX + "stop"):
                        return
                    if message.content.startswith((CONFIG).PREFIX + "login"):
                        return
                    if message.content.startswith((CONFIG).PREFIX + "sv-news"):
                        return
                    if message.content.startswith((CONFIG).PREFIX + "set-news"):
                        return
                    if message.content.startswith((CONFIG).PREFIX + "bot-info"):
                        return
                    if message.content.startswith((CONFIG).PREFIX + "sv-info"):
                        return
                    if message.content.startswith((CONFIG).PREFIX + "whois"):
                        return
                    if message.content.startswith((CONFIG).PREFIX + "ping"):
                        return
                    if message.content.startswith((CONFIG).PREFIX + "invite"):
                        return
                    if message.content.startswith((CONFIG).PREFIX + "src"):
                        return
                    if message.content.startswith((CONFIG).PREFIX + "kick"):
                        return
                    if message.content.startswith("Hallo"):
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send('Hallo ' + message.author.mention)
                        return
                    else:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send('Meine Prefix ist **' + CONFIG.PREFIX + '** ' + message.author.mention)


        else:
            if client.user.mentioned_in(message) and message.mention_everyone is False:
                client.AppInfo = await client.application_info()
                embed = discord.Embed(title="Keine Lizenz", description=":x: Hey, dieser Server hat keine Lizenz! "
                                                                        "Für eine Lizenz wende dich\nbitte an " + client.AppInfo.owner.mention,
                                      color=0xff0000)
                embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()
                await message.channel.trigger_typing()
                await asyncio.sleep(0.5)
                await message.channel.send(embed=embed)


client.run(CONFIG.TOKEN)

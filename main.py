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
from config import CONFIG
from config.GAMES import __games__, __gamesTimer__
import codecs

client = discord.Client()
__version__ = '0.3.9.1'
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
        embed = discord.Embed(title=':x: Event Fehler', colour=0xe74c3c) #Red
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
        await client.change_presence(activity=discord.Activity(type=randomGame[0], name=randomGame[1].format(guilds = guildCount, members = memberCount)))
        await asyncio.sleep(random.choice(__gamesTimer__))
        if CONFIG.clientLogout == True:
            await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Bot deaktiviert"))
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
    embed.add_field(name="Erstellt am", value=CreateDateDay + "." + CreateDateMonth + "." + CreateDateYear + " um " + CreateDateTime + " Uhr")
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
                            await message.channel.send(embed=embed)
                        else:
                            await message.channel.send(":x: Dieser Server existiert nicht, "
                                                       "oder ich bin auf diesem Server nicht autorisiert!")
                    else:
                        await message.channel.send(":x: Bitte benutze **" + CONFIG.PREFIX + "sv-id [ServerID]**")
                elif len(message.content) != 25:
                    await message.channel.send(":x: Bitte benutze **" + CONFIG.PREFIX + "sv-id [ServerID]**")

            if message.content.startswith(CONFIG.PREFIX + 'stop'):
                if CONFIG.clientLogout == False:
                    embed = discord.Embed(title="", description="Der Bot wird deaktiviert...", color=0xe74c3c)
                    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Bot deaktiviert"))
                    await message.channel.send(embed=embed)
                    CONFIG.clientLogout = True
                else:
                    embed = discord.Embed(title="", description=":x: Der Bot ist schon deaktiviert", color=0xff0000)
                    await message.channel.send(embed=embed)
            if message.content.startswith(CONFIG.PREFIX + 'login'):
                if CONFIG.clientLogout == True:
                    embed = discord.Embed(title="", description="Der Bot wird aktiviert...", color=0x2ecc71)
                    client.gamesLoop = asyncio.ensure_future(_randomGame())
                    await message.channel.send(embed=embed)
                    CONFIG.clientLogout = False
                else:
                    embed = discord.Embed(title="", description=":x: Das geht nur, wenn der Bot deaktiviert ist", color=0xff0000)
                    await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="", description=":x: Hey, ich bin nur ein Bot und kann noch nicht darauf antworten", color=0xff0000)
            if not message.author.bot:
                await message.author.send(embed=embed)

    else:
        if message.guild.id in CONFIG.AllowedServer:
            if message.content.startswith(CONFIG.PREFIX + 'stop'):
                client.AppInfo = await client.application_info()
                if message.author.id == client.AppInfo.owner.id:
                    if CONFIG.clientLogout == False:
                        embed = discord.Embed(title="", description="Der Bot wird deaktiviert...", color=0xe74c3c)
                        await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Bot deaktiviert"))
                        await message.channel.send(embed=embed)
                        CONFIG.clientLogout = True
                    else:
                        embed = discord.Embed(title="", description=":x: Der Bot ist schon deaktiviert", color=0xff0000)
                        await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title="", description=":x: Hey, dafür hast du keine Rechte!", color=0xff0000)
                    await message.channel.send(embed=embed)
            if message.content.startswith(CONFIG.PREFIX + 'login'):
                    client.AppInfo = await client.application_info()
                    if message.author.id == client.AppInfo.owner.id:
                        if CONFIG.clientLogout == True:
                            embed = discord.Embed(title="", description="Der Bot wird aktiviert...", color=0x2ecc71)
                            client.gamesLoop = asyncio.ensure_future(_randomGame())
                            await message.channel.send(embed=embed)
                            CONFIG.clientLogout = False
                        else:
                            embed = discord.Embed(title="",description=":x: Das geht nur, wenn der Bot deaktiviert ist", color=0xff0000)
                            await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title="", description=":x: Hey, dafür hast du keine Rechte!", color=0xff0000)
                        await message.channel.send(embed=embed)

            if CONFIG.clientLogout == False:
                if message.content.startswith(CONFIG.PREFIX + 'sv-news'):
                    embed = discord.Embed(title="", description="", color=0x00ff00)
                    embed.add_field(name="Neuigkeiten", value="Hey, @here!\n"
                     "Wir haben die Verlassen Nachrichten deaktiviert & die Privaten Nachrichten beim Beitritt unseres Servers aktiviert."
                    "Da viele sich beim Beitritt die Nachricht in <#649178318674984960> nicht durchlesen, wo alles erklärt ist wie ihr die benötigten Rechte "
                    "bekommt mit der dazugehörigen Rolle. Werden wir diese Nachricht künftig auch privat schicken lassen. ", inline=False)
                    embed.set_footer(text="Server News von Thundercraft", icon_url=client.user.avatar_url,)
                    embed.set_thumbnail(url=message.guild.icon_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await message.channel.send(embed=embed)

                if message.content.startswith(CONFIG.PREFIX + 'Hallo'):
                    await message.channel.send('Hallo ' + message.author.mention)

                if client.user.mentioned_in(message) and message.mention_everyone is False:
                    if not message.author.bot:
                        await message.channel.send('Meine Prefix ist **' + CONFIG.PREFIX + '** ' + message.author.mention)

                if message.content.startswith(CONFIG.PREFIX + "bot-info"):
                    client.AppInfo = await client.application_info()
                    latency = str(client.latency)[0:4]
                    embed = discord.Embed(title="Bot Informationen", description="Bot-Name: " + client.user.name + "\nBot-ID: " + str(client.user.id) + "\nDev Mode: " + client.dev + "\nDiscord Version: " + str(discord.__version__) +
                    "\nBot Version: " + str(__version__) + "\nPing: " + latency + "ms" + "\nPrefix: **&**" + "\nBot Developer: " + str(client.AppInfo.owner.mention) + "\nBot-Sprache: :flag_de: German, Deutsch", color=0xffffff)
                    embed.set_thumbnail(url=client.user.avatar_url)
                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await message.channel.send(embed=embed)

                if message.content.startswith(CONFIG.PREFIX + 'set-patch'):
                    if message.author.id == 354191516979429376:
                        embed = discord.Embed(title="", description=":x: Noch nicht Verfügbar",color=0xff0000)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title="", description=":x: Hey, dafür hast du keine Rechte!", color=0xff0000)
                        await message.channel.send(embed=embed)

                if message.content.startswith(CONFIG.PREFIX + "sv-info"):
                    if message.guild.id in CONFIG.SupportLicenseServer:
                        serverLicense = "Unterstützer Lizenz"
                    elif message.guild.id in CONFIG.AllowedServer:
                        serverLicense = "Standard Lizenz"
                    else:
                        serverLicense = "Keine Lizenz"
                    client.AppInfo = await client.application_info()
                    embed = discord.Embed(title="Server Informationen", description="Server Name: " + str(message.guild.name) + "\nServer ID: " + str(message.guild.id) +
                    "\nServerbesitzer: " + str(message.guild.owner.mention) + "\nServer Region: " + str(message.guild.region) + "\nLizenz: " + str(serverLicense), color=0xffffff)
                    embed.add_field(name="Mitglieder", value=str(message.guild.member_count) + " Mitglieder")
                    CreateDateYear = str(message.guild.created_at)[0:4]
                    CreateDateMonth = str(message.guild.created_at)[5:7]
                    CreateDateDay = str(message.guild.created_at)[8:10]
                    CreateDateTime = str(message.guild.created_at)[11:16]
                    embed.add_field(name="Erstellt am", value=CreateDateDay + "." + CreateDateMonth + "." + CreateDateYear + " um " + CreateDateTime + " Uhr")
                    embed.set_footer(text="Server Info von " + message.guild.name, icon_url=client.user.avatar_url)
                    embed.set_thumbnail(url=message.guild.icon_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await message.channel.send(embed=embed)

                if message.content.startswith(CONFIG.PREFIX + "whois"):
                     member = message.author
                     __JoinPos__ = ""
                     if member.joined_at is None:
                         __JoinPos__ = "Could not locate your join date"
                         return
                     __JoinPos__ = sum(
                         m.joined_at < member.joined_at for m in message.guild.members if m.joined_at is not None)
                     embed = discord.Embed(title="", description=str(message.author) + "\n" + message.author.mention, color=0xffffff)
                     AuthorGuildJoinDate = str(message.author.joined_at)[8:10] + "." + str(message.author.joined_at)[5:7] + "." + str(message.author.joined_at)[0:4] + " um " + str(message.author.joined_at)[11:16] + " Uhr"
                     AuthorRegisterDate = str(message.author.created_at)[8:10] + "." + str(message.author.created_at)[5:7] + "." + str(message.author.created_at)[0:4] + " um " + str(message.author.created_at)[11:16] + " Uhr"
                     embed.add_field(name="Server beigetreten", value=AuthorGuildJoinDate)
                     embed.add_field(name="Join Position", value="Du hast als **" + str(__JoinPos__) + ". Mitglied** denn Server betreten")
                     embed.add_field(name="Registriert bei Discord", value=AuthorRegisterDate)
                     embed.set_thumbnail(url=message.author.avatar_url)
                     embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                     embed.timestamp = datetime.datetime.utcnow()
                     await message.channel.send(embed=embed)

                if message.content.startswith(CONFIG.PREFIX + "ping"):
                    latency = str(client.latency)[0:4]
                    await message.channel.send("Bot Ping = " + latency + "ms")

                if message.content.startswith(CONFIG.PREFIX + "invite"):
                    await message.channel.send(message.author.mention + ", der Einladungslink wurde dir zugeschickt.")
                    embed = discord.Embed(title="", description="Hier kannst du mich zu deinem Server einladen:\n"
                    "https://discordapp.com/oauth2/authorize?client_id=664831660235292714&scope=bot&permissions=67632230\n"
                    "\nBedenke aber das du eine Lizenz brauchst. Lizenzen kannst du bei **" + client.AppInfo.owner.mention + "** kaufen.", color=0xffffff)
                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    if not message.author.bot:
                        await message.author.send(embed=embed)

                if message.content.startswith(CONFIG.PREFIX + "src"):
                    embed = discord.Embed(title="", description="Hier findest du meinen Source Code:"
                    "\nhttps://github.com/IBimsEinMystery/ServerPatches"
                    "\n\n**Dieser Source Code steht unter Lizenz:**"
                    "\n```" + mit_license.read() + "```", color=0xffffff)
                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await message.channel.send(embed=embed)

        else:
            if client.user.mentioned_in(message) and message.mention_everyone is False:
                client.AppInfo = await client.application_info()
                embed = discord.Embed(title="Keine Lizenz", description=":x: Hey, dieser Server hat keine Lizenz! "
                "Für eine Lizenz wende dich\nbitte an " + client.AppInfo.owner.mention, color=0xff0000)
                embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()
                await message.channel.send(embed=embed)

client.run(CONFIG.TOKEN)

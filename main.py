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
import datetime
from pytz import timezone
import traceback
import random
import asyncio
from config import CONFIG, SV_NEWS, UserInGameName
from config.GAMES import __games__, __gamesTimer__
import codecs
import os

client = discord.Client()
__version__ = '1.5'
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
THIS_FILE = os.path.join(THIS_FOLDER, 'MIT.txt')
mit_license = codecs.open(THIS_FILE, "r", encoding="utf-8")
client.logoutMessageID = "NOTHING"

#on_ready
@client.event
async def on_ready():
    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                      + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
    print(__printDateTime + "Der Bot wurde aktiviert")
    print(__printDateTime + f'Bot Name: {client.user.name}')
    print(__printDateTime + f'Discord Version: {discord.__version__}')
    print(__printDateTime + f'Bot Version: {__version__}')
    client.AppInfo = await client.application_info()
    print(__printDateTime + f'Owner: {client.AppInfo.owner}')
    client.gamesLoop = asyncio.ensure_future(_randomGame())
    print(__printDateTime + "Aktivität wurde aktiviert")


#on_error
@client.event
async def on_error(event, *args, **kwargs):
    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
    embed = discord.Embed(title='Event Fehler', color=0xff0000)  # Red
    embed.add_field(name='Event', value=event)
    embed.description = '```py\n%s\n```' % traceback.format_exc()
    embed.timestamp = datetime.datetime.utcnow()
    try:
        await client.AppInfo.owner.send(embed=embed)
        print(__printDateTime + "ERROR:")
        traceback.print_exc()
        return
    except:
        pass
    traceback.print_exc()

#_randomGame()
@client.event
async def _randomGame():
    while True:
        guildCount = len(client.guilds)
        memberCount = len(list(client.get_all_members()))
        randomGame = random.choice(__games__)
        await client.change_presence(activity=discord.Activity(type=randomGame[0], name=randomGame[1].format(guilds=guildCount, members=memberCount)))
        await asyncio.sleep(random.choice(__gamesTimer__))
        if CONFIG.clientLogout == True:
            await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Bot deaktiviert"))
            break

#on_guild_join
@client.event
async def on_guild_join(guild):
    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
    embed = discord.Embed(title=':white_check_mark: Zum Server hinzugefügt', color=0x2ecc71,
    description="Server Name: " + str(guild.name) +"\nServer ID: " + str(guild.id) +
    "\nServer Besitzer: " + str(guild.owner) + "\nServer Region: " + str(guild.region))
    embed.add_field(name="Mitglieder", value=str(guild.member_count) + " Mitglieder")
    CreateDateYear = str(timezone('Europe/Berlin').fromutc(guild.created_at))[0:4]
    CreateDateMonth = str(timezone('Europe/Berlin').fromutc(guild.created_at))[5:7]
    CreateDateDay = str(timezone('Europe/Berlin').fromutc(guild.created_at))[8:10]
    CreateDateTime = str(timezone('Europe/Berlin').fromutc(guild.created_at))[11:16]
    embed.add_field(name="Erstellt am", value=CreateDateDay + "." + CreateDateMonth + "." + CreateDateYear + " um " + CreateDateTime + " Uhr")
    embed.set_thumbnail(url=guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()
    await client.AppInfo.owner.send(embed=embed)
    print(__printDateTime + "Zum Server hinzugefügt")
    
#on_guild_remove
@client.event
async def on_guild_remove(guild):
    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
    embed = discord.Embed(title=':x: Vom Server entfernt', color=0xe74c3c,
    description="Server Name: " + str(guild.name) + "\nServer ID: " + str(guild.id) +
    "\nServer Besitzer: " + str(guild.owner) + "\nServer Region: " + str(guild.region))
    embed.add_field(name="Mitglieder", value=str(guild.member_count) + " Mitglieder")
    CreateDateYear = str(timezone('Europe/Berlin').fromutc(guild.created_at))[0:4]
    CreateDateMonth = str(timezone('Europe/Berlin').fromutc(guild.created_at))[5:7]
    CreateDateDay = str(timezone('Europe/Berlin').fromutc(guild.created_at))[8:10]
    CreateDateTime = str(timezone('Europe/Berlin').fromutc(guild.created_at))[11:16]
    embed.add_field(name="Erstellt am",
    value=CreateDateDay + "." + CreateDateMonth + "." + CreateDateYear + " um " + CreateDateTime + " Uhr")
    embed.set_thumbnail(url=guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()
    await client.AppInfo.owner.send(embed=embed)
    print(__printDateTime + "Vom Server entfernt")
    print(guild.created_at.replace.astimezone(timezone('Europe/Berlin')))

#on_disconnect
@client.event
async def on_disconnect():
    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
    logoutMessageID = ""
    print(__printDateTime + "Verbindung getrennt")

#on_resumed
@client.event
async def on_resumed():
    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "

    print(__printDateTime + "Verbindung wiederhergestellt")

#on_connect
@client.event
async def on_connect():
    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
    print(__printDateTime + "Mit Discord verbunden")

#on_message
@client.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        if message.author.id == client.AppInfo.owner.id:
            #sv-id
                if message.content.startswith(CONFIG.PREFIX + "sv-id"):
                    args = message.content.split(" ")
                    if len(args) == 2:
                        serverID = args[1]
                        if str.isdigit(serverID):
                            if client.get_guild(int(serverID)):
                                guildWithID = client.get_guild(int(serverID))
                                embed = discord.Embed(title="", description="Der Bot wird gestartet...", color=0x2ecc71)
                                embed = discord.Embed(title=':white_check_mark: Server gefunden', color=0x2ecc71,
                                                 description="Server Name: " + str(guildWithID.name) +
                                                             "\nServer ID: " + str(guildWithID.id) +
                                                             "\nServer Besitzer: " + str(guildWithID.owner) +
                                                             "\nServer Region: " + str(guildWithID.region))
                                embed.add_field(name="Mitglieder", value=str(guildWithID.member_count) + " Mitglieder")
                                CreateDateYear = str(timezone('Europe/Berlin').fromutc(guildWithID.created_at))[0:4]
                                CreateDateMonth = str(timezone('Europe/Berlin').fromutc(guildWithID.created_at))[5:7]
                                CreateDateDay = str(timezone('Europe/Berlin').fromutc(guildWithID.created_at))[8:10]
                                CreateDateTime = str(timezone('Europe/Berlin').fromutc(guildWithID.created_at))[11:16]
                                embed.add_field(name="Erstellt am", value=CreateDateDay + "." + CreateDateMonth + "." + CreateDateYear + " um " + CreateDateTime + " Uhr")
                                embed.set_thumbnail(url=guildWithID.icon_url)
                                embed.timestamp = datetime.datetime.utcnow()
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            else:
                                embed = discord.Embed(title="", color=0xff0000, description="Server nicht gefunden!")
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                        else:
                            embed = discord.Embed(title="", color=0xff0000, description="Das ist keine gültige ServerID")
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title="", color=0xff0000, description="Bitte benutze **" + CONFIG.PREFIX + "sv-id [ServerID]**")
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                        
            #dm
                if message.content.startswith(CONFIG.PREFIX + "dm"):
                    args = message.content.split(" ")
                    try:
                        dmUserID = message.raw_mentions[0]
                        dmMessage = message.content.replace(args[0] + " " + args[1], "")
                        try:
                            dmEmbed = discord.Embed(title="", description="" + dmMessage, color=random.randint(0, 0xffffff))
                            dmEmbed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                            dmEmbed.timestamp=datetime.datetime.utcnow()
                            sendEmbed = discord.Embed(title="", description="Erfolgreich gesendet", color=0x2ecc71)
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await client.get_user(dmUserID).send(embed=dmEmbed)
                            await message.channel.send(embed=sendEmbed)
                            
                            
                        except:
                            embed = discord.Embed(title="", description="Nachricht konnte nicht zugestellt werden", color=0xff0000)
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                    except:
                        embed = discord.Embed(title="", description="Bitte benutze **" + CONFIG.PREFIX + "dm [@User#1234] [Nachricht]**", color=0xff0000)
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                                   
            #stop
                if message.content.startswith(CONFIG.PREFIX + 'stop'):
                    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
                    if CONFIG.clientLogout == False:
                        embed = discord.Embed(title="", description="Der Bot wird gestoppt...", color=0xe74c3c)
                        await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Bot gestoppt"))
                        CONFIG.clientLogout = True
                        print(__printDateTime + "Bot gestoppt")
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title="", description="Der Bot ist schon gestoppt", color=0xff0000)
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    
            #start
                if message.content.startswith(CONFIG.PREFIX + 'start'):
                    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
                    if CONFIG.clientLogout == True:
                        embed = discord.Embed(title="", description="Der Bot wird gestartet...", color=0x2ecc71)
                        client.gamesLoop = asyncio.ensure_future(_randomGame())
                        CONFIG.clientLogout = False
                        print(__printDateTime + "Bot gestartet")
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title="", description="Der Bot ist schon gestartet", color=0xff0000)
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    
            #logout
                if message.content.startswith(CONFIG.PREFIX + 'logout'):
                    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
                    await message.add_reaction("\U00002705")
                    await message.add_reaction("\U0000274c")
                    client.logoutMessageID = message.id
                    
                    @client.event
                    async def on_reaction_add(reaction, user):
                        DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                        __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[
                                                                                                    17:19] + " " \
                                        + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(
                            DateTime.year) + " \xbb "
                        if reaction.message.author.id == client.AppInfo.owner.id:
                            if reaction.message.id == client.logoutMessageID:
                                if user.id == client.AppInfo.owner.id:
                                    if reaction.emoji == '\U00002705':
                                        logOut = discord.Embed(title="", color=0xe74c3c, description="Abmeldung erfolgt")
                                        await message.channel.send(embed=logOut)
                                        print(__printDateTime + "Abmeldung")
                                        client.logoutMessageID = "NOTHING"
                                        await asyncio.sleep(2)
                                        await client.change_presence(status=discord.Status.offline)
                                        await client.logout()
                                    if reaction.emoji == '\U0000274c':
                                        logOutCancel = discord.Embed(title="", color=0xe74c3c, description="Abmeldung abgebrochen")
                                        await message.channel.send(embed=logOutCancel)
                                        client.logoutMessageID = "NOTHING"
                                    
        #PrivateMessage
        else:
            embed = discord.Embed(title="", description="Hey, ich bin nur ein Bot und nehme keine Privaten Nachrichten an!", color=random.randint(0, 0xffffff))
            if not message.author.bot:
                await message.channel.trigger_typing()
                await asyncio.sleep(0.5)
                await message.author.send(embed=embed)
    
    #ServerCommands
    else:
        #stop
            if message.content.startswith(CONFIG.PREFIX + 'stop'):
                if message.author.id == client.AppInfo.owner.id:
                    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
                    if CONFIG.clientLogout == False:
                        embed = discord.Embed(title="", description="Der Bot wird gestoppt...", color=0xe74c3c)
                        print(__printDateTime + "Bot gestoppt")
                        try:
                            await message.channel.trigger_typing()
                            await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Bot gestoppt"))
                            CONFIG.clientLogout = True
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                        except:
                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                            if not message.author.bot:
                                message.author.send(embed=embed)
                    else:
                        embed = discord.Embed(title="", description="Der Bot ist schon gestoppt", color=0xff0000)
                        try:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                        except:
                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                            if not message.author.bot:
                                message.author.send(embed=embed)
                else:
                    embed = discord.Embed(title="", description="Hey " + message.author.mention + ", dafür hast du keine Rechte!", color=0xff0000)
                    try:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    except:
                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                            if not message.author.bot:
                                message.author.send(embed=embed)
                
        #start
            if message.content.startswith(CONFIG.PREFIX + 'start'):
                if message.author.id == client.AppInfo.owner.id:
                    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
                    if CONFIG.clientLogout == True:
                        embed = discord.Embed(title="", description="Der Bot wird gestartet...", color=0x2ecc71)
                        try:
                            await message.channel.trigger_typing()
                            client.gamesLoop = asyncio.ensure_future(_randomGame())
                            CONFIG.clientLogout = False
                            print(__printDateTime + "Bot gestartet")
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                        except:
                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                            if not message.author.bot:
                                message.author.send(embed=embed)
                    else:
                        embed = discord.Embed(title="", description="Der Bot ist schon gestartet", color=0xff0000)
                        try:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                        except:
                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                            if not message.author.bot:
                                message.author.send(embed=embed)
                else:
                    embed = discord.Embed(title="", description="Hey " + message.author.mention + ", dafür hast du keine Rechte!", color=0xff0000)
                    try:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    except:
                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                            if not message.author.bot:
                                message.author.send(embed=embed)
                
        #logout
            if message.content.startswith(CONFIG.PREFIX + 'logout'):
                if message.author.id == client.AppInfo.owner.id:
                    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
                    try:
                        await message.add_reaction("\U00002705")
                        await message.add_reaction("\U0000274c")
                        client.logoutMessageID = message.id
                    except:
                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Reaktionen zu benutzen. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                            if not message.author.bot:
                                message.author.send(embed=embed)
                    
                    @client.event
                    async def on_reaction_add(reaction, user):
                        DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                        __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[
                                                                                                    17:19] + " " \
                                        + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(
                            DateTime.year) + " \xbb "
                        if reaction.message.author.id == client.AppInfo.owner.id:
                            if reaction.message.id == client.logoutMessageID:
                                if (user.id == client.AppInfo.owner.id) | (user.id == client.user.id):
                                    if user.id == client.AppInfo.owner.id:
                                        if reaction.emoji == '\U00002705':
                                            logOut = discord.Embed(title="", color=0xe74c3c, description="Abmeldung erfolgt")
                                            try:
                                                await message.channel.send(embed=logOut)
                                                print(__printDateTime + "Abmeldung")
                                                client.logoutMessageID = "NOTHING"
                                                await asyncio.sleep(2)
                                                await client.change_presence(status=discord.Status.offline)
                                                await client.logout()
                                            except:
                                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                                if not message.author.bot:
                                                    message.author.send(embed=embed)
                                        if reaction.emoji == '\U0000274c':
                                            logOutCancel = discord.Embed(title="", color=0xe74c3c, description="Abmeldung abgebrochen")
                                            try:
                                                await message.channel.send(embed=logOutCancel)
                                                client.logoutMessageID = "NOTHING"
                                            except:
                                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                                if not message.author.bot:
                                                    message.author.send(embed=embed)
                                else:
                                    if reaction.emoji == '\U00002705':
                                        await message.remove_reaction('\U00002705', user)
                                    if reaction.emoji == '\U0000274c':
                                        await message.remove_reaction('\U0000274c', user)
                else:
                    embed = discord.Embed(title="", description="Hey " + message.author.mention + ", dafür hast du keine Rechte!", color=0xff0000)
                    try:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    except:
                        embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                        if not message.author.bot:
                            message.author.send(embed=embed)
                                
        #BotAn
            if CONFIG.clientLogout == False:
            #sv-news
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
                                try:
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(embed=embed)
                                except:
                                    embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                    if not message.author.bot:
                                        message.author.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Diese Nachricht wurde gelöscht!", color=0xff0000)
                                try:
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(embed=embed)
                                except:
                                    embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                    if not message.author.bot:
                                        message.author.send(embed=embed)
                        except:
                            embed = discord.Embed(title="", description="Dieser Channel wurde gelöscht!", color=0xff0000)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                    else:
                        embed = discord.Embed(title="", description="Es wurde keine Nachricht eingestellt!", color=0xff0000)
                        try:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                        except:
                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                            if not message.author.bot:
                                message.author.send(embed=embed)
    
            #set-news
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
                                                    embed = discord.Embed(title="", description=":white_check_mark: Erfolgreich gesetzt", color=0x2ecc71)
                                                    SV_NEWS.newsID.pop(message.guild.id)
                                                    SV_NEWS.newsID.update({message.guild.id: str(channelID) + "(" + str(messageID) + ")"})
                                                    __newDictionary = SV_NEWS.newsID.copy()
                                                    __newDictionary = str(__newDictionary).replace("{", "{\n ")
                                                    __newDictionary = str(__newDictionary).replace(",", ",\n")
                                                    __newDictionary = str(__newDictionary).replace("}", "\n}")
                                                    sv_news.write("newsID = " + str(__newDictionary))
                                                    try:
                                                        await message.channel.trigger_typing()
                                                        await asyncio.sleep(0.5)
                                                        await message.channel.send(embed=embed)
                                                    except:
                                                        embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                                        if not message.author.bot:
                                                            message.author.send(embed=embed)
                                                except:
                                                    embed = discord.Embed(title="", description=":white_check_mark: Erfolgreich gesetzt", color=0x2ecc71)
                                                    SV_NEWS.newsID.update({message.guild.id: str(channelID) + "(" + str(messageID) + ")"})
                                                    __newDictionary = SV_NEWS.newsID.copy()
                                                    __newDictionary = str(__newDictionary).replace("{", "{\n ")
                                                    __newDictionary = str(__newDictionary).replace(",", ",\n")
                                                    __newDictionary = str(__newDictionary).replace("}", "\n}")
                                                    sv_news.write("newsID = " + str(__newDictionary))
                                                    try:
                                                        await message.channel.trigger_typing()
                                                        await asyncio.sleep(0.5)
                                                        await message.channel.send(embed=embed)
                                                    except:
                                                        embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                                        if not message.author.bot:
                                                            message.author.send(embed=embed)
                                            except:
                                                embed = discord.Embed(title="", description="Konfig konnte nicht gespeichert werden!", color=0xff0000)
                                                try:
                                                    await message.channel.trigger_typing()
                                                    await asyncio.sleep(0.5)
                                                    await message.channel.send(embed=embed)
                                                except:
                                                    embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                                    if not message.author.bot:
                                                        message.author.send(embed=embed)
                                        except:
                                            embed = discord.Embed(title="", description="Datei wurde nicht gefunden!", color=0xff0000)
                                            try:
                                                await message.channel.trigger_typing()
                                                await asyncio.sleep(0.5)
                                                await message.channel.send(embed=embed)
                                            except:
                                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                                if not message.author.bot:
                                                    message.author.send(embed=embed)
                                    except:
                                        embed = discord.Embed(title="", description="Die Nachrichten-ID ist ungültig!", color=0xff0000)
                                        try:
                                            await message.channel.trigger_typing()
                                            await asyncio.sleep(0.5)
                                            await message.channel.send(embed=embed)
                                        except:
                                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                            if not message.author.bot:
                                                message.author.send(embed=embed)
                                else:
                                    embed = discord.Embed(title="", description="Die Kanal-ID ist ungültig!", color=0xff0000)
                                    try:
                                        await message.channel.trigger_typing()
                                        await asyncio.sleep(0.5)
                                        await message.channel.send(embed=embed)
                                    except:
                                        embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                        if not message.author.bot:
                                            message.author.send(embed=embed)
                            else:
                                embed = discord.Embed(title="", description="Bitte benutze **" + CONFIG.PREFIX + "set-news [Kanal-ID] [Nachrichten-ID]**", color=0xff0000)
                                try:
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(embed=embed)
                                except:
                                    embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                    if not message.author.bot:
                                        message.author.send(embed=embed)
                        else:
                            embed = discord.Embed(title="", description="Bitte benutze **" + CONFIG.PREFIX + "set-news [Kanal-ID] [Nachrichten-ID]**", color=0xff0000)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                    else:
                        embed = discord.Embed(title="", description="Hey " + message.author.mention + ", dafür hast du keine Rechte!", color=0xff0000)
                        try:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                        except:
                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                            if not message.author.bot:
                                message.author.send(embed=embed)
                        
            #bot-info
                if message.content.startswith(CONFIG.PREFIX + "bot-info"):
                    client.AppInfo = await client.application_info()
                    latency = str(client.latency)[0:4]
                    embed = discord.Embed(title="Bot Informationen", 
                    description="Bot-Name: " + client.user.name + "\nBot-ID: " + str(client.user.id) + 
                    "\nBot-Version: " + str(__version__) + "\nPing: " + latency + "ms" + "\nPrefix: **" + CONFIG.PREFIX + "**" + "\nAktive Server: " + str(len(client.guilds)) + 
                    " Server\nBot-Developer: " + str(client.AppInfo.owner.mention) + "\nBot-Sprache: :flag_de: German, Deutsch", color=0xe43d53)
                    embed.set_thumbnail(url=client.user.avatar_url)
                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    try:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    except:
                        embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                        if not message.author.bot:
                            message.author.send(embed=embed)
                    
            #sv-info
                if message.content.startswith(CONFIG.PREFIX + "sv-info"):
                    if str(message.guild.member_count) == "1":
                        members = " Mitglied"
                    else:
                        members = " Mitglieder"
                        
                    role_name = [role.mention for role in message.guild.roles]
                    role_name = role_name[1:]
                    role_name.reverse()
                    role_list = ', '.join(role_name)
                    role_amount = role_list.count("@")
                    client.AppInfo = await client.application_info()
                    embed = discord.Embed(title=str(message.guild.name),
                    description="Server Name: " + str(message.guild.name) + "\nServer ID: " + str(message.guild.id) +
                    "\nServerbesitzer: " + str(message.guild.owner.mention) + "\nServer Region: " + str(message.guild.region), color=0xffffff)
                    embed.add_field(name="Mitglieder", value=str(message.guild.member_count) + members)
                    CreateDateYear = str(timezone('Europe/Berlin').fromutc(message.guild.created_at))[0:4]
                    CreateDateMonth = str(timezone('Europe/Berlin').fromutc(message.guild.created_at))[5:7]
                    CreateDateDay = str(timezone('Europe/Berlin').fromutc(message.guild.created_at))[8:10]
                    CreateDateTime = str(timezone('Europe/Berlin').fromutc(message.guild.created_at))[11:16]
                    embed.add_field(name="Erstellt am", value=CreateDateDay + "." + CreateDateMonth + "." + CreateDateYear + " um " + CreateDateTime + " Uhr")
                    embed.add_field(name="Rollen [" + str(role_amount) + "]", value=role_list, inline=False)
                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                    embed.set_thumbnail(url=message.guild.icon_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    try:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    except:
                        embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                        if not message.author.bot:
                            message.author.send(embed=embed)
            
            #whois
                if message.content.startswith(CONFIG.PREFIX + "whois"):
                    if len(message.content) == 6:
                        member = message.author
                    try:
                        if not len(message.content) == 6:
                            member = message.mentions[0]
                    except:
                        embed = discord.Embed(title="", description="Bitte benutze **" + CONFIG.PREFIX + "whois <@User#1234>**", color=0xff0000)
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                        return
                    __JoinPos__ = ""
                    if member.joined_at is None:
                        __JoinPos__ = "Konnte das Beitrittsdatum nicht feststellen"
                        return
                    __JoinPos__ = sum(timezone('Europe/Berlin').fromutc(m.joined_at) < timezone('Europe/Berlin').fromutc(member.joined_at) for m in message.guild.members if m.joined_at is not None)
                    if __JoinPos__ == 0:
                        __JoinPos__ = "Besitzer"
                    AuthorGuildJoinDate = str(timezone('Europe/Berlin').fromutc(member.joined_at))[8:10] + "." + str(timezone('Europe/Berlin').fromutc(member.joined_at))[5:7] + "." + str(timezone('Europe/Berlin').fromutc(member.joined_at))[0:4] + " um " + str(timezone('Europe/Berlin').fromutc(member.joined_at))[11:16] + " Uhr"
                    AuthorRegisterDate = str(timezone('Europe/Berlin').fromutc(member.created_at))[8:10] + "." + str(timezone('Europe/Berlin').fromutc(member.created_at))[5:7] + "." + str(timezone('Europe/Berlin').fromutc(member.created_at))[0:4] + " um " + str(timezone('Europe/Berlin').fromutc(member.created_at))[11:16] + " Uhr"
                    role_name = [role.mention for role in member.roles]
                    role_name = role_name[1:]
                    role_name.reverse()
                    role_list = ', '.join(role_name)
                    role_amount = role_list.count("@")
                    if len(role_list) <= 25:
                        role_list = "\nKeine Rollen auf dem Server"
                    
                    color = member.top_role.color
                    client.AppInfo = await client.application_info()
                    if member.id == client.user.id:
                        color=0xe43d53
                    
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
                        __AllPerms = "Keine Rechte auf dem Server"
                    embed = discord.Embed(title="", description="Name: " + str(member.mention) +
                                                                "\nID: " + str(member.id) +
                                                                "\nBeigetreten: " + str(AuthorGuildJoinDate) +
                                                                "\nJoin Position: " + str(__JoinPos__) +
                                                                "\nRegistriert: " + str(AuthorRegisterDate) +
                                                                f'\nRollen [{role_amount}]: {role_list}' +
                                                                f' \nBerechtigungen: \n{__AllPerms}', color=color)
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_author(name=member, icon_url=member.avatar_url)
                    try:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    except:
                        embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                        if not message.author.bot:
                            message.author.send(embed=embed)
            
            #ping
                if message.content.startswith(CONFIG.PREFIX + "ping"):
                    latency = str(client.latency)[0:4]
                    embed=discord.Embed(title="", description="Bot Ping = " + latency + "ms", color=0xe43d53)
                    try:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    except:
                        embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                        if not message.author.bot:
                            message.author.send(embed=embed)
                    
            #invite
                if message.content.startswith(CONFIG.PREFIX + "invite"):
                    embed=discord.Embed(title="", description=message.author.mention + ", der Einladungslink wurde dir zugeschickt.", color=0xe43d53)
                    try:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                        embed = discord.Embed(title="", description="Hier kannst du mich zu deinem Server einladen:\nhttps://bit.ly/2wlXDC3", color=0xe43d53)
                        embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                        embed.timestamp = datetime.datetime.utcnow()
                        if not message.author.bot:
                            await message.author.send(embed=embed)
                    except:
                        embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                        if not message.author.bot:
                            message.author.send(embed=embed)
                        
            #src
                if message.content.startswith(CONFIG.PREFIX + "src"):
                    embed = discord.Embed(title="", description="Hier findest du meinen Source Code:"
                                                                "\nhttps://github.com/IBimsEinDomi/CherryBot", color=0xe43d53)
                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    try:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    except:
                        embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                        if not message.author.bot:
                            message.author.send(embed=embed)
            
            #kick
                if message.content.startswith(CONFIG.PREFIX + "kick"):
                    DateTime = datetime.datetime.now(timezone('Europe/Berlin'))
                    __printDateTime = str(DateTime)[11:13] + ":" + str(DateTime)[14:16] + ":" + str(DateTime)[17:19] + " " \
                                    + str(DateTime)[8:10] + "." + str(DateTime)[5:7] + "." + str(DateTime.year) + " \xbb "
                    if message.author.guild_permissions.kick_members:
                        try:
                            memberKick = message.mentions[0]
                            author = message.author
                            argsLenght = len(str(CONFIG.PREFIX) + "kick @" + str(client.user)) + 3
                            messageMention = message.content[0:argsLenght]
                            try:
                                if not str(client.user.id) in messageMention:
                                    try:
                                        if not str(message.guild.owner.id) in message.mentions:
                                            try:
                                                embed=discord.Embed(title="", description=":white_check_mark: Du hast " + memberKick.mention + " gekickt", color=0x2ecc71)
                                                try:
                                                    await memberKick.kick(reason=str(message.author) + " hat " + str(memberKick) + " entfernt")
                                                    await message.channel.trigger_typing()
                                                    await asyncio.sleep(0.5)
                                                    await message.channel.send(embed=embed)
                                                    print(__printDateTime + str(author) + " hat " + str(memberKick) + " von " + message.guild.name + "(" +  str(message.guild.id) + ")" + " gekickt")
                                                except:
                                                    embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                                    if not message.author.bot:
                                                        message.author.send(embed=embed)
                                            except:
                                                embed=discord.Embed(title="", description="Ich habe keine Rechte zum kicken", color=0xff0000)
                                                try:
                                                    await message.channel.trigger_typing()
                                                    await asyncio.sleep(0.5)
                                                    await message.channel.send(embed=embed)
                                                except:
                                                    embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                                    if not message.author.bot:
                                                        message.author.send(embed=embed)
                                        else:
                                            embed=discord.Embed(title="", description="Du kannst denn Besitzer dieses Servers nicht kicken!", color=0xff0000)
                                            try:
                                                await message.channel.trigger_typing()
                                                await asyncio.sleep(0.5)
                                                await message.channel.send(embed=embed)
                                            except:
                                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                                if not message.author.bot:
                                                    message.author.send(embed=embed)
                                    except:
                                        embed=discord.Embed(title="", description="Du kannst denn Besitzer dieses Servers nicht kicken!", color=0xff0000)
                                        try:
                                            await message.channel.trigger_typing()
                                            await asyncio.sleep(0.5)
                                            await message.channel.send(embed=embed)
                                        except:
                                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                            if not message.author.bot:
                                                message.author.send(embed=embed)
                                else:
                                    embed=discord.Embed(title="", description="Ich kann mich nicht selber kicken!", color=0xff0000)
                                    try:
                                        await message.channel.trigger_typing()
                                        await asyncio.sleep(0.5)
                                        await message.channel.send(embed=embed)
                                    except:
                                        embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                        if not message.author.bot:
                                            message.author.send(embed=embed)
                            except:
                                embed=discord.Embed(title="", description="Ich kann mich nicht selber kicken!", color=0xff0000)
                                try:
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(embed=embed)
                                except:
                                    embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                    if not message.author.bot:
                                        message.author.send(embed=embed)
                        except:
                            embed=discord.Embed(title="", description="Bitte benutze **" + CONFIG.PREFIX + "kick [@User#1234]**!", color=0xff0000)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                    else:
                        embed = discord.Embed(title="", description="Hey " + message.author.mention + ", dafür hast du keine Rechte!", color=0xff0000)
                        try:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                        except:
                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                            if not message.author.bot:
                                message.author.send(embed=embed)
                
            #uplay
                if(message.content.startswith(CONFIG.PREFIX + "uplay")):
                    args = message.content.split(" ")
                    if len(args) == 1:
                            member = message.author
                    elif len(args) == 2 and str(args[1]) == "unlink":
                        member = message.author
                        if member.id in UserInGameName.uplay:
                            try:
                                uplay = codecs.open(".\\config\\UserInGameName.py", "w")
                                UserInGameName.uplay.pop(message.author.id)
                                newFileUplay = str(UserInGameName.uplay.copy())
                                newFileUplay = newFileUplay.replace("{", "{\n ")
                                newFileUplay = newFileUplay.replace(",", ",\n")
                                newFileUplay = newFileUplay.replace("}", "\n}")
                                newFileSteam = str(UserInGameName.steam.copy())
                                newFileSteam = newFileSteam.replace("{", "{\n ")
                                newFileSteam = newFileSteam.replace(",", ",\n")
                                newFileSteam = newFileSteam.replace("}", "\n}")
                                newFileEpic = str(UserInGameName.epicgames.copy())
                                newFileEpic = newFileEpic.replace("{", "{\n ")
                                newFileEpic = newFileEpic.replace(",", ",\n")
                                newFileEpic = newFileEpic.replace("}", "\n}")
                                uplay.write("uplay = " + newFileUplay)
                                uplay.write("\nsteam = " + newFileSteam)
                                uplay.write("\nepicgames = " + newFileEpic)
                                embed = discord.Embed(title="", description="Die Verknüpfung wurde gelöscht", color=0x2ecc71)
                                try:
                                    await message.channel.send(embed=embed)
                                except:
                                    embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                    if not message.author.bot:
                                        message.author.send(embed=embed)
                            except:
                                embed=discord.Embed(title="", description="Es trat ein Fehler auf!\nBitte versuche es später erneut", color=0xff0000)
                                embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                embed.timestamp=datetime.datetime.utcnow()
                                try:
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(embed=embed)
                                except:
                                    embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                    if not message.author.bot:
                                        message.author.send(embed=embed)
                            return
                        else:
                            embed=discord.Embed(title="", description="Du hast keine Verknüpfung für Uplay", color=0x0070FF)
                            embed.set_footer(text="Uplay", icon_url="https://pics.computerbase.de/7/7/5/8/3/logo-256.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                            return
                    elif len(args) >= 2:
                        try:
                            member = message.mentions[0]
                        except:
                            embed = discord.Embed(title="", description="Bitte benutze **" + CONFIG.PREFIX + "uplay <@User#1234/unlink>**", color=0xff0000)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                            return
                    
                    if not client.user.id == member.id:
                        if member.id in UserInGameName.uplay:
                            UserName = UserInGameName.uplay.get(member.id).replace("|Oe|", "Ö").replace("|oe|", "ö").replace("|Ue|", "Ü").replace("|ue|", "ü").replace("|Ae|", "Ä").replace("|ae|", "ä")
                            embed=discord.Embed(title="", description="Name: " + UserName, color=0x0070FF)
                            embed.set_footer(text="Uplay", icon_url="https://pics.computerbase.de/7/7/5/8/3/logo-256.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                        elif not member.id in UserInGameName.uplay and len(args) >= 2:
                            embed=discord.Embed(title="", description=member.mention + " muss erst seinen\nAccount mit `" + CONFIG.PREFIX + "register uplay [Name]`\nverknüpfen", color=0x0070FF)
                            embed.set_footer(text="Uplay", icon_url="https://pics.computerbase.de/7/7/5/8/3/logo-256.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                        else:
                            embed=discord.Embed(title="", description="Du musst erst deinen\nAccount mit `" + CONFIG.PREFIX + "register uplay [Name]`\nverknüpfen", color=0x0070FF)
                            embed.set_footer(text="Uplay", icon_url="https://pics.computerbase.de/7/7/5/8/3/logo-256.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                    else:
                        embed=discord.Embed(title="", description="Mich gibt es nicht auf Uplay", color=0x0070FF)
                        embed.set_footer(text="Uplay", icon_url="https://pics.computerbase.de/7/7/5/8/3/logo-256.png")
                        embed.timestamp=datetime.datetime.utcnow()
                        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                        try:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                        except:
                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                            if not message.author.bot:
                                message.author.send(embed=embed)
                      
            #steam        
                if(message.content.startswith(CONFIG.PREFIX + "steam")):
                    args = message.content.split(" ")
                    if len(args) == 1:
                            member = message.author
                    elif len(args) == 2 and str(args[1]) == "unlink":
                        member = message.author
                        if member.id in UserInGameName.uplay:
                            try:
                                steam = codecs.open(".\\config\\UserInGameName.py", "w")
                                UserInGameName.steam.pop(message.author.id)
                                newFileUplay = str(UserInGameName.uplay.copy())
                                newFileUplay = newFileUplay.replace("{", "{\n ")
                                newFileUplay = newFileUplay.replace(",", ",\n")
                                newFileUplay = newFileUplay.replace("}", "\n}")
                                newFileSteam = str(UserInGameName.steam.copy())
                                newFileSteam = newFileSteam.replace("{", "{\n ")
                                newFileSteam = newFileSteam.replace(",", ",\n")
                                newFileSteam = newFileSteam.replace("}", "\n}")
                                newFileEpic = str(UserInGameName.epicgames.copy())
                                newFileEpic = newFileEpic.replace("{", "{\n ")
                                newFileEpic = newFileEpic.replace(",", ",\n")
                                newFileEpic = newFileEpic.replace("}", "\n}")
                                steam.write("uplay = " + newFileUplay)
                                steam.write("\nsteam = " + newFileSteam)
                                steam.write("\nepicgames = " + newFileEpic)
                                embed = discord.Embed(title="", description="Die Verknüpfung wurde gelöscht", color=0x2ecc71)
                                try:
                                    await message.channel.send(embed=embed)
                                except:
                                    embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                    if not message.author.bot:
                                        message.author.send(embed=embed)
                            except:
                                embed=discord.Embed(title="", description="Es trat ein Fehler auf!\nBitte versuche es später erneut", color=0xff0000)
                                embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                embed.timestamp=datetime.datetime.utcnow()
                                try:
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(embed=embed)
                                except:
                                    embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                    if not message.author.bot:
                                        message.author.send(embed=embed)
                            return
                        else:
                            embed=discord.Embed(title="", description="Du hast keine Verknüpfung für Steam", color=0x091936)
                            embed.set_footer(text="Steam", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2000px-Steam_icon_logo.svg.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                            return
                    elif len(args) >= 2:
                        try:
                            member = message.mentions[0]
                        except:
                            embed = discord.Embed(title="", description="Bitte benutze **" + CONFIG.PREFIX + "steam <@User#1234/unlink>**", color=0xff0000)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                            return
                    
                    if not client.user.id == member.id:
                        if member.id in UserInGameName.steam:
                            UserName = UserInGameName.steam.get(member.id).replace("|Oe|", "Ö").replace("|oe|", "ö").replace("|Ue|", "Ü").replace("|ue|", "ü").replace("|Ae|", "Ä").replace("|ae|", "ä")
                            embed=discord.Embed(title="", description="Name: " + UserName, color=0x091936)
                            embed.set_footer(text="Steam", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2000px-Steam_icon_logo.svg.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                        elif not member.id in UserInGameName.steam and len(args) >= 2:
                            embed=discord.Embed(title="", description=member.mention + " muss erst seinen\nAccount mit `" + CONFIG.PREFIX + "register steam [Name]`\nverknüpfen", color=0x091936)
                            embed.set_footer(text="Steam", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2000px-Steam_icon_logo.svg.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                        else:
                            embed=discord.Embed(title="", description="Du musst erst deinen\nAccount mit `" + CONFIG.PREFIX + "register steam [Name]`\nverknüpfen", color=0x091936)
                            embed.set_footer(text="Steam", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2000px-Steam_icon_logo.svg.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                    else:
                        embed=discord.Embed(title="", description="Mich gibt es nicht auf Steam", color=0x091936)
                        embed.set_footer(text="Steam", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2000px-Steam_icon_logo.svg.png")
                        embed.timestamp=datetime.datetime.utcnow()
                        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                        try:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                        except:
                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                            if not message.author.bot:
                                message.author.send(embed=embed)
                    
            #epicgames
                if(message.content.startswith(CONFIG.PREFIX + "epicgames")):
                    args = message.content.split(" ")
                    if len(args) == 1:
                            member = message.author
                    elif len(args) == 2 and str(args[1]) == "unlink":
                        member = message.author
                        if member.id in UserInGameName.uplay:
                            try:
                                epic = codecs.open(".\\config\\UserInGameName.py", "w")
                                UserInGameName.steam.pop(message.author.id)
                                newFileUplay = str(UserInGameName.uplay.copy())
                                newFileUplay = newFileUplay.replace("{", "{\n ")
                                newFileUplay = newFileUplay.replace(",", ",\n")
                                newFileUplay = newFileUplay.replace("}", "\n}")
                                newFileSteam = str(UserInGameName.steam.copy())
                                newFileSteam = newFileSteam.replace("{", "{\n ")
                                newFileSteam = newFileSteam.replace(",", ",\n")
                                newFileSteam = newFileSteam.replace("}", "\n}")
                                newFileEpic = str(UserInGameName.epicgames.copy())
                                newFileEpic = newFileEpic.replace("{", "{\n ")
                                newFileEpic = newFileEpic.replace(",", ",\n")
                                newFileEpic = newFileEpic.replace("}", "\n}")
                                epic.write("uplay = " + newFileUplay)
                                epic.write("\nsteam = " + newFileSteam)
                                epic.write("\nepicgames = " + newFileEpic)
                                embed = discord.Embed(title="", description="Die Verknüpfung wurde gelöscht", color=0x2ecc71)
                                try:
                                    await message.channel.send(embed=embed)
                                except:
                                    embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                    if not message.author.bot:
                                        message.author.send(embed=embed)
                            except:
                                embed=discord.Embed(title="", description="Es trat ein Fehler auf!\nBitte versuche es später erneut", color=0xff0000)
                                embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                embed.timestamp=datetime.datetime.utcnow()
                                try:
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(embed=embed)
                                except:
                                    embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                    if not message.author.bot:
                                        message.author.send(embed=embed)
                            return
                        else:
                            embed=discord.Embed(title="", description="Du hast keine Verknüpfung für Epic Games", color=0x2F2D2E)
                            embed.set_footer(text="Epic Games", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Epic_Games_logo.svg/2000px-Epic_Games_logo.svg.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                            return
                    elif len(args) >= 2:
                        try:
                            member = message.mentions[0]
                        except:
                            embed = discord.Embed(title="", description="Bitte benutze **" + CONFIG.PREFIX + "epicgames <@User#1234>**", color=0xff0000)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                            return
                    if not client.user.id == member.id:
                        if member.id in UserInGameName.epicgames:
                            UserName = UserInGameName.epicgames.get(member.id).replace("|Oe|", "Ö").replace("|oe|", "ö").replace("|Ue|", "Ü").replace("|ue|", "ü").replace("|Ae|", "Ä").replace("|ae|", "ä")
                            embed=discord.Embed(title="", description="Name: " + UserName, color=0x2F2D2E)
                            embed.set_footer(text="Epic Games", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Epic_Games_logo.svg/2000px-Epic_Games_logo.svg.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                        elif not member.id in UserInGameName.epicgames and len(args) >= 2:
                            embed=discord.Embed(title="", description=member.mention + " muss erst seinen\nAccount mit `" + CONFIG.PREFIX + "register epicgames [Name]`\nverknüpfen", color=0x2F2D2E)
                            embed.set_footer(text="Epic Games", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Epic_Games_logo.svg/2000px-Epic_Games_logo.svg.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                        else:
                            embed=discord.Embed(title="", description="Du musst erst deinen\nAccount mit `" + CONFIG.PREFIX + "register epicgames [Name]`\nverknüpfen", color=0x2F2D2E)
                            embed.set_footer(text="Epic Games", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Epic_Games_logo.svg/2000px-Epic_Games_logo.svg.png")
                            embed.timestamp=datetime.datetime.utcnow()
                            embed.set_author(name=member.name, icon_url=member.avatar_url)
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                    else:
                        embed=discord.Embed(title="", description="Mich gibt es nicht auf Epic Games", color=0x2F2D2E)
                        embed.set_footer(text="Epic Games", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Epic_Games_logo.svg/2000px-Epic_Games_logo.svg.png")
                        embed.timestamp=datetime.datetime.utcnow()
                        embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                        try:
                            await message.channel.trigger_typing()
                            await asyncio.sleep(0.5)
                            await message.channel.send(embed=embed)
                        except:
                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                            if not message.author.bot:
                                message.author.send(embed=embed)
                    
            #register
                if(message.content.startswith(CONFIG.PREFIX + "register")):
                    if len(message.content) >= 10: 
                        args = message.content.split(" ")
                        if args[1] == "uplay":
                            if len(message.content) >= 16:
                                UserName = str(args[2]).replace("Ö", "|Oe|").replace("ö", "|oe|").replace("Ü", "|Ue|").replace("ü", "|ue|").replace("Ä", "|Ae|").replace("ä", "|ae|")
                                if len(message.content) <= 16 + len(args[2]):
                                    try:
                                        uplay = codecs.open(".\\config\\UserInGameName.py", "w")
                                        if message.author.id in UserInGameName.uplay:
                                            UserInGameName.uplay.pop(message.author.id)
                                            UserInGameName.uplay.update({message.author.id: UserName})
                                            newFileUplay = str(UserInGameName.uplay.copy())
                                            newFileUplay = newFileUplay.replace("{", "{\n ")
                                            newFileUplay = newFileUplay.replace(",", ",\n")
                                            newFileUplay = newFileUplay.replace("}", "\n}")
                                            newFileSteam = str(UserInGameName.steam.copy())
                                            newFileSteam = newFileSteam.replace("{", "{\n ")
                                            newFileSteam = newFileSteam.replace(",", ",\n")
                                            newFileSteam = newFileSteam.replace("}", "\n}")
                                            newFileEpic = str(UserInGameName.epicgames.copy())
                                            newFileEpic = newFileEpic.replace("{", "{\n ")
                                            newFileEpic = newFileEpic.replace(",", ",\n")
                                            newFileEpic = newFileEpic.replace("}", "\n}")
                                            uplay.write("uplay = " + newFileUplay)
                                            uplay.write("\nsteam = " + newFileSteam)
                                            uplay.write("\nepicgames = " + newFileEpic)
                                            embed=discord.Embed(title="", description=":white_check_mark: Erfolgreich gesetzt", color=0x2ecc71)
                                            embed.set_footer(text="Uplay: " + args[2], icon_url="https://pics.computerbase.de/7/7/5/8/3/logo-256.png")
                                            embed.timestamp=datetime.datetime.utcnow()
                                            try:
                                                await message.channel.trigger_typing()
                                                await asyncio.sleep(0.5)
                                                await message.channel.send(embed=embed)
                                            except:
                                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                                if not message.author.bot:
                                                    message.author.send(embed=embed)
                                        else:
                                            UserInGameName.uplay.update({message.author.id: UserName})
                                            newFileUplay = str(UserInGameName.uplay.copy())
                                            newFileUplay = newFileUplay.replace("{", "{\n ")
                                            newFileUplay = newFileUplay.replace(",", ",\n")
                                            newFileUplay = newFileUplay.replace("}", "\n}")
                                            newFileSteam = str(UserInGameName.steam.copy())
                                            newFileSteam = newFileSteam.replace("{", "{\n ")
                                            newFileSteam = newFileSteam.replace(",", ",\n")
                                            newFileSteam = newFileSteam.replace("}", "\n}")
                                            newFileEpic = str(UserInGameName.epicgames.copy())
                                            newFileEpic = newFileEpic.replace("{", "{\n ")
                                            newFileEpic = newFileEpic.replace(",", ",\n")
                                            newFileEpic = newFileEpic.replace("}", "\n}")
                                            uplay.write("uplay = " + newFileUplay)
                                            uplay.write("\nsteam = " + newFileSteam)
                                            uplay.write("\nepicgames = " + newFileEpic)
                                            embed=discord.Embed(title="", description=":white_check_mark: Erfolgreich gesetzt", color=0x2ecc71)
                                            embed.set_footer(text="Uplay: " + args[2], icon_url="https://pics.computerbase.de/7/7/5/8/3/logo-256.png")
                                            embed.timestamp=datetime.datetime.utcnow()
                                            try:
                                                await message.channel.trigger_typing()
                                                await asyncio.sleep(0.5)
                                                await message.channel.send(embed=embed)
                                            except:
                                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                                if not message.author.bot:
                                                    message.author.send(embed=embed)
                                    except:
                                        embed=discord.Embed(title="", description="Es trat ein Fehler auf!\nBitte versuche es später erneut", color=0xff0000)
                                        embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                        embed.timestamp=datetime.datetime.utcnow()
                                        try:
                                            await message.channel.trigger_typing()
                                            await asyncio.sleep(0.5)
                                            await message.channel.send(embed=embed)
                                        except:
                                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                            if not message.author.bot:
                                                message.author.send(embed=embed)
                                else:
                                    embed=discord.Embed(title="", description="Der Name darf keine Leerzeichen enthalten!", color=0xff0000)
                                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                    embed.timestamp=datetime.datetime.utcnow()
                                    try:
                                        await message.channel.trigger_typing()
                                        await asyncio.sleep(0.5)
                                        await message.channel.send(embed=embed)
                                    except:
                                        embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                        if not message.author.bot:
                                            message.author.send(embed=embed)
                            else:
                                embed=discord.Embed(title="", description="Bitte benutze **&register uplay [Name]**", color=0xff0000)
                                embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                embed.timestamp=datetime.datetime.utcnow()
                                try:
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(embed=embed)
                                except:
                                    embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                    if not message.author.bot:
                                        message.author.send(embed=embed)
                                
                        elif args[1] == "steam":
                            if len(message.content) >= 16:
                                UserName = str(args[2]).replace("Ö", "|Oe|").replace("ö", "|oe|").replace("Ü", "|Ue|").replace("ü", "|ue|").replace("Ä", "|Ae|").replace("ä", "|ae|")
                                if len(message.content) <= 16 + len(args[2]):
                                    try:
                                        steam = codecs.open(".\\config\\UserInGameName.py", "w")
                                        if message.author.id in UserInGameName.steam:
                                            UserInGameName.steam.pop(message.author.id)
                                            UserInGameName.steam.update({message.author.id: UserName})
                                            newFileUplay = str(UserInGameName.uplay.copy())
                                            newFileUplay = newFileUplay.replace("{", "{\n ")
                                            newFileUplay = newFileUplay.replace(",", ",\n")
                                            newFileUplay = newFileUplay.replace("}", "\n}")
                                            newFileSteam = str(UserInGameName.steam.copy())
                                            newFileSteam = newFileSteam.replace("{", "{\n ")
                                            newFileSteam = newFileSteam.replace(",", ",\n")
                                            newFileSteam = newFileSteam.replace("}", "\n}")
                                            newFileEpic = str(UserInGameName.epicgames.copy())
                                            newFileEpic = newFileEpic.replace("{", "{\n ")
                                            newFileEpic = newFileEpic.replace(",", ",\n")
                                            newFileEpic = newFileEpic.replace("}", "\n}")
                                            steam.write("uplay = " + newFileUplay)
                                            steam.write("\nsteam = " + newFileSteam)
                                            steam.write("\nepicgames = " + newFileEpic)
                                            embed=discord.Embed(title="", description=":white_check_mark: Erfolgreich gesetzt", color=0x2ecc71)
                                            embed.set_footer(text="Steam: " + args[2], icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2000px-Steam_icon_logo.svg.png")
                                            embed.timestamp=datetime.datetime.utcnow()
                                            try:
                                                await message.channel.trigger_typing()
                                                await asyncio.sleep(0.5)
                                                await message.channel.send(embed=embed)
                                            except:
                                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                                if not message.author.bot:
                                                    message.author.send(embed=embed)
                                        else:
                                            UserInGameName.steam.update({message.author.id: UserName})
                                            newFileUplay = str(UserInGameName.uplay.copy())
                                            newFileUplay = newFileUplay.replace("{", "{\n ")
                                            newFileUplay = newFileUplay.replace(",", ",\n")
                                            newFileUplay = newFileUplay.replace("}", "\n}")
                                            newFileSteam = str(UserInGameName.steam.copy())
                                            newFileSteam = newFileSteam.replace("{", "{\n ")
                                            newFileSteam = newFileSteam.replace(",", ",\n")
                                            newFileSteam = newFileSteam.replace("}", "\n}")
                                            newFileEpic = str(UserInGameName.epicgames.copy())
                                            newFileEpic = newFileEpic.replace("{", "{\n ")
                                            newFileEpic = newFileEpic.replace(",", ",\n")
                                            newFileEpic = newFileEpic.replace("}", "\n}")
                                            steam.write("uplay = " + newFileUplay)
                                            steam.write("\nsteam = " + newFileSteam)
                                            steam.write("\nepicgames = " + newFileEpic)
                                            embed=discord.Embed(title="", description=":white_check_mark: Erfolgreich gesetzt", color=0x2ecc71)
                                            embed.set_footer(text="Steam: " + args[2], icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2000px-Steam_icon_logo.svg.png")
                                            embed.timestamp=datetime.datetime.utcnow()
                                            try:
                                                await message.channel.trigger_typing()
                                                await asyncio.sleep(0.5)
                                                await message.channel.send(embed=embed)
                                            except:
                                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                                if not message.author.bot:
                                                    message.author.send(embed=embed)
                                    except:
                                        embed=discord.Embed(title="", description="Es trat ein Fehler auf!\nBitte versuche es später erneut", color=0xff0000)
                                        embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                        embed.timestamp=datetime.datetime.utcnow()
                                        try:
                                            await message.channel.trigger_typing()
                                            await asyncio.sleep(0.5)
                                            await message.channel.send(embed=embed)
                                        except:
                                            embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                            if not message.author.bot:
                                                message.author.send(embed=embed)
                                else:
                                    embed=discord.Embed(title="", description="Der Name darf keine Leerzeichen enthalten!", color=0xff0000)
                                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                    embed.timestamp=datetime.datetime.utcnow()
                                    try:
                                        await message.channel.trigger_typing()
                                        await asyncio.sleep(0.5)
                                        await message.channel.send(embed=embed)
                                    except:
                                        embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                        if not message.author.bot:
                                            message.author.send(embed=embed)
                            else:
                                embed=discord.Embed(title="", description="Bitte benutze **&register steam [Name]**", color=0xff0000)
                                embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                embed.timestamp=datetime.datetime.utcnow()
                                try:
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(embed=embed)
                                except:
                                    embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                    if not message.author.bot:
                                        message.author.send(embed=embed)
                              
                        elif args[1] == "epicgames":
                            if len(message.content) >= 20:
                                UserName = str(args[2]).replace("Ö", "|Oe|").replace("ö", "|oe|").replace("Ü", "|Ue|").replace("ü", "|ue|").replace("Ä", "|Ae|").replace("ä", "|ae|")
                                if len(message.content) <= 20 + len(args[2]):
                                    try:
                                        epic = codecs.open(".\\config\\UserInGameName.py", "w")
                                        if message.author.id in UserInGameName.uplay:
                                            UserInGameName.epicgames.pop(message.author.id)
                                            UserInGameName.epicgames.update({message.author.id: UserName})
                                            newFileUplay = str(UserInGameName.uplay.copy())
                                            newFileUplay = newFileUplay.replace("{", "{\n ")
                                            newFileUplay = newFileUplay.replace(",", ",\n")
                                            newFileUplay = newFileUplay.replace("}", "\n}")
                                            newFileSteam = str(UserInGameName.steam.copy())
                                            newFileSteam = newFileSteam.replace("{", "{\n ")
                                            newFileSteam = newFileSteam.replace(",", ",\n")
                                            newFileSteam = newFileSteam.replace("}", "\n}")
                                            newFileEpic = str(UserInGameName.epicgames.copy())
                                            newFileEpic = newFileEpic.replace("{", "{\n ")
                                            newFileEpic = newFileEpic.replace(",", ",\n")
                                            newFileEpic = newFileEpic.replace("}", "\n}")
                                            epic.write("uplay = " + newFileUplay)
                                            epic.write("\nsteam = " + newFileSteam)
                                            epic.write("\nepicgames = " + newFileEpic)
                                            embed=discord.Embed(title="", description=":white_check_mark: Erfolgreich gesetzt", color=0x2ecc71)
                                            embed.set_footer(text="Epic Games: " + args[2], icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Epic_Games_logo.svg/2000px-Epic_Games_logo.svg.png")
                                            embed.timestamp=datetime.datetime.utcnow()
                                            try:
                                                await message.channel.trigger_typing()
                                                await asyncio.sleep(0.5)
                                                await message.channel.send(embed=embed)
                                            except:
                                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                                if not message.author.bot:
                                                    message.author.send(embed=embed)
                                        else:
                                            UserInGameName.epicgames.update({message.author.id: UserName})
                                            newFileUplay = str(UserInGameName.uplay.copy())
                                            newFileUplay = newFileUplay.replace("{", "{\n ")
                                            newFileUplay = newFileUplay.replace(",", ",\n")
                                            newFileUplay = newFileUplay.replace("}", "\n}")
                                            newFileSteam = str(UserInGameName.steam.copy())
                                            newFileSteam = newFileSteam.replace("{", "{\n ")
                                            newFileSteam = newFileSteam.replace(",", ",\n")
                                            newFileSteam = newFileSteam.replace("}", "\n}")
                                            newFileEpic = str(UserInGameName.epicgames.copy())
                                            newFileEpic = newFileEpic.replace("{", "{\n ")
                                            newFileEpic = newFileEpic.replace(",", ",\n")
                                            newFileEpic = newFileEpic.replace("}", "\n}")
                                            epic.write("uplay = " + newFileUplay)
                                            epic.write("\nsteam = " + newFileSteam)
                                            epic.write("\nepicgames = " + newFileEpic)
                                            embed=discord.Embed(title="", description=":white_check_mark: Erfolgreich gesetzt", color=0x2ecc71)
                                            embed.set_footer(text="Epic Games: " + args[2], icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Epic_Games_logo.svg/2000px-Epic_Games_logo.svg.png")
                                            embed.timestamp=datetime.datetime.utcnow()
                                            try:
                                                await message.channel.trigger_typing()
                                                await asyncio.sleep(0.5)
                                                await message.channel.send(embed=embed)
                                            except:
                                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                                if not message.author.bot:
                                                    message.author.send(embed=embed)
                                    except:
                                        embed=discord.Embed(title="", description="Es trat ein Fehler auf!\nBitte versuche es später erneut", color=0xff0000)
                                        embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                        embed.timestamp=datetime.datetime.utcnow()
                                        try:
                                            await message.channel.trigger_typing()
                                            await asyncio.sleep(0.5)
                                            await message.channel.send(embed=embed)
                                        except:
                                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                                if not message.author.bot:
                                                    message.author.send(embed=embed)
                                else:
                                    embed=discord.Embed(title="", description="Der Name darf keine Leerzeichen enthalten!", color=0xff0000)
                                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                    embed.timestamp=datetime.datetime.utcnow()
                                    try:
                                        await message.channel.trigger_typing()
                                        await asyncio.sleep(0.5)
                                        await message.channel.send(embed=embed)
                                    except:
                                        embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                        if not message.author.bot:
                                            message.author.send(embed=embed)
                            else:
                                embed=discord.Embed(title="", description="Bitte benutze **&register epicgames [Name]**", color=0xff0000)
                                embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                                embed.timestamp=datetime.datetime.utcnow()
                                try:
                                    await message.channel.trigger_typing()
                                    await asyncio.sleep(0.5)
                                    await message.channel.send(embed=embed)
                                except:
                                    embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                    if not message.author.bot:
                                        message.author.send(embed=embed)
                        
                        else:
                            embed=discord.Embed(title="", description="Bitte benutze **&register [uplay/steam/epicgames] [Name]**", color=0xff0000)
                            embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                            embed.timestamp=datetime.datetime.utcnow()
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send(embed=embed)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
            
            #help
                if message.content.startswith(CONFIG.PREFIX + "help"):
                    embed = discord.Embed(title="", color=0xe43d53, description="[Über CherryBot](https://cherrybot.gitbook.io/cherrybot/)\n"
                                          + "[Befehle](https://cherrybot.gitbook.io/cherrybot/befehle)\n[FAQ](https://cherrybot.gitbook.io/cherrybot/faq)\n[Lade CherryBot ein](https://discordapp.com/oauth2/authorize?client_id=664831660235292714&scope=bot&response_type=code&redirect_uri=https://discord.gg/ZMDJKUf&permissions=543818)\n"
                                          + "[CherryBot auf GitHub](https://github.com/IBimsEinMystery/CherryBot)\n[Unterstütze mich](https://www.paypal.me/dominik1711)\n[Vote für CherryBot](https://top.gg/bot/664831660235292714/vote)")
                    embed.set_author(name="CherryBot Hilfe Menü", icon_url=client.user.avatar_url)
                    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
                    embed.timestamp=datetime.datetime.utcnow()
                    try:
                        await message.channel.trigger_typing()
                        await asyncio.sleep(0.5)
                        await message.channel.send(embed=embed)
                    except:
                        embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                        if not message.author.bot:
                            message.author.send(embed=embed)
                
                            
            #RespondOnPing
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
                        if message.content.startswith((CONFIG).PREFIX + "uplay"):
                            return
                        if message.content.startswith((CONFIG).PREFIX + "steam"):
                            return
                        if message.content.startswith((CONFIG).PREFIX + "epicgames"):
                            return
                        if message.content.startswith("Hallo"):
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send('Hallo ' + message.author.mention)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)
                            return
                        else:
                            try:
                                await message.channel.trigger_typing()
                                await asyncio.sleep(0.5)
                                await message.channel.send('Meine Prefix ist **' + CONFIG.PREFIX + '** ' + message.author.mention)
                            except:
                                embed = discord.Embed(title="", description="Ich habe keine Rechte um Nachrichten zu senden. Bitte gebe einen Administrator über dieses Problem bescheid.", color=0xff0000)
                                if not message.author.bot:
                                    message.author.send(embed=embed)


client.run(CONFIG.TOKEN)

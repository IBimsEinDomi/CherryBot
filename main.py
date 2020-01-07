import discord
import datetime
import time
import random
import asyncio
from config import CONFIG
from config.GAMES import __games__, __gamesTimer__

client = discord.Client()
__version__ = '0.3.1'

@client.event
async def on_ready():
    if client.user.id == 657169769589374977:
        client.dev = "Aktiviert"
    else:
        client.dev = "Deaktiviert"
    client.gamesLoop = asyncio.ensure_future(_randomGame())
    print("Der Bot wurde aktiviert")
    print(f'Bot Name: {client.user.name}')
    print(f'Discord Version: {discord.__version__}')
    print(f'Bot Version: {__version__}')

async def _randomGame():
    while True:
        guildCount = len(client.guilds)
        memberCount = len(list(client.get_all_members()))
        randomGame = random.choice(__games__)
        await client.change_presence(activity=discord.Activity(type=randomGame[0], name=randomGame[1].format(guilds = guildCount, members = memberCount)))
        await asyncio.sleep(__gamesTimer__)

@client.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        embed = discord.Embed(title="", description=":x: Hey, ich bin nur ein Bot und kann noch nicht darauf antworten", color=0xff0000)
        await message.author.send(embed=embed)
    else:
        if message.guild.id == CONFIG.AllowedServer[1]:
            if message.content.startswith(CONFIG.PREFIX + 'stop'):
                client.AppInfo = await client.application_info()
                if message.author.id == client.AppInfo.owner.id:
                    if CONFIG.clientLogout == False:
                        embed = discord.Embed(title="", description="Der Bot wird deaktiviert...", color=0xff0000)
                        await client.change_presence(status=discord.Status.idle, activity=discord.Game(name="Zurzeit nicht erreichbar"))
                        embed.set_footer(text="Server Patches",
                        icon_url=client.user.avatar_url, )
                        embed.timestamp = datetime.datetime.utcnow()
                        await message.channel.send(embed=embed)
                        CONFIG.clientLogout = True
                    else:
                        embed = discord.Embed(title="", description=":x: Der Bot ist schon aus", color=0xff0000)
                        await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title="", description=":x: Hey, dafür hast du keine Rechte!", color=0xff0000)
                    embed.set_footer(text="Server Patches",
                    icon_url=client.user.avatar_url, )
                    embed.timestamp = datetime.datetime.utcnow()
                    await message.channel.send(embed=embed)
            if message.content.startswith(CONFIG.PREFIX + 'login'):
                    client.AppInfo = await client.application_info()
                    if message.author.id == client.AppInfo.owner.id:
                        if CONFIG.clientLogout == True:
                            embed = discord.Embed(title="", description="Der Bot wird aktiviert...", color=0x00ff00)
                            embed.set_footer(text="Server Patches",
                            icon_url=client.user.avatar_url, )
                            embed.timestamp = datetime.datetime.utcnow()
                            await client.change_presence(status=discord.Status.online, activity=discord.Game(name=activity))
                            await message.channel.send(embed=embed)
                            CONFIG.clientLogout = False
                        else:
                            embed = discord.Embed(title="",description=":x: Das geht nur, wenn der Bot deaktiviert ist", color=0xff0000)
                            await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title="", description=":x: Hey, dafür hast du keine Rechte! ", color=0xff0000)
                        embed.set_footer(text="Server Patches",
                        icon_url=client.user.avatar_url, )
                        embed.timestamp = datetime.datetime.utcnow()
                        await message.channel.send(embed=embed)

            if CONFIG.clientLogout == False:
                if message.content.startswith(CONFIG.PREFIX + 'sv-patch'):
                    embed = discord.Embed(title="", description="", color=0x00ff00)
                    embed.add_field(name="Neuigkeiten", value="Hey, @here!\n"
                     "Wir haben die Verlassen Nachrichten deaktiviert & die Privaten Nachrichten beim Beitritt unseres Servers aktiviert."
                    "Da viele sich beim Beitritt die Nachricht in <#649178318674984960> nicht durchlesen, wo alles erklärt ist wie ihr die benötigten Rechte "
                    "bekommt mit der dazugehörigen Rolle. Werden wir diese Nachricht künftig auch privat schicken lassen. ", inline=False)
                    embed.set_footer(text="Server News von Thundercraft",
                    icon_url=client.user.avatar_url,)
                    embed.set_thumbnail(url=message.guild.icon_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await message.channel.send(embed=embed)

                if message.content.startswith(CONFIG.PREFIX + 'noPerms'):
                    embed = discord.Embed(title="", description=":x: Hey, dafür hast du keine Rechte!",color=0xff0000)
                    await message.channel.send(embed=embed)

                if message.content.startswith(CONFIG.PREFIX + 'Hallo'):
                    await message.channel.send('Hallo ' + message.author.mention)

                if client.user.mentioned_in(message) and message.mention_everyone is False:
                    await message.channel.send('Meine Prefix ist **&** ' + message.author.mention)
                if message.content.startswith("prefix"):
                    await message.channel.send('Meine Prefix ist **&** ' + message.author.mention)

                if message.content.startswith(CONFIG.PREFIX + "bot-info"):
                    client.AppInfo = await client.application_info()
                    embed = discord.Embed(title="Bot Informationen", description="Bot-Name: " + client.user.name + "\nBot-ID: " + str(client.user.id) + "\nDev Mode: " + client.dev + "\nDiscord Version: " + str(discord.__version__) +
                    "\nBot Version: " + str(__version__) + "\nBot Developer: " + str(client.AppInfo.owner) + "\nBot-Sprache: :flag_de: German, Deutsch" + "\nPrefix: **&**", color=0x00ff00)
                    embed.set_thumbnail(url=client.user.avatar_url)
                    embed.set_footer(text="Server Patches", icon_url=client.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await message.channel.send(embed=embed)

                if message.content.startswith(CONFIG.PREFIX + 'set-patch'):
                    if message.author.id == 354191516979429376:
                        embed = discord.Embed(title="", description="",color=0xff0000)
                        await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(title="", description=":x: Hey, dafür hast du keine Rechte!",
                                              color=0xff0000)
                        embed.set_footer(text="Server Patches",
                                         icon_url=client.user.avatar_url, )
                        embed.timestamp = datetime.datetime.utcnow()
                        await message.channel.send(embed=embed)

                if message.content.startswith(CONFIG.PREFIX + "sv-info"):
                    if (message.guild.id == 479691134482776066) | (message.guild.id == 657578121163309069):
                        serverLicense = "Supporter Lizenz"
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
                     embed = discord.Embed(title="", description=str(message.author) + "\n" + message.author.mention, color=0xffffff)
                     AuthorGuildJoinDate = str(message.author.joined_at)[8:10] + "." + str(message.author.joined_at)[5:7] + "." + str(message.author.joined_at)[0:4] + " um " + str(message.author.joined_at)[11:16] + " Uhr"
                     AuthorRegisterDate = str(message.author.created_at)[8:10] + "." + str(message.author.created_at)[5:7] + "." + str(message.author.created_at)[0:4] + " um " + str(message.author.created_at)[11:16] + " Uhr"
                     embed.add_field(name="Server beigetreten", value=AuthorGuildJoinDate)
                     embed.add_field(name="Join Position", value="Zurzeit noch nicht verfügbar")
                     embed.add_field(name="Registriert bei Discord", value=AuthorRegisterDate)
                     embed.set_thumbnail(url=message.author.avatar_url)
                     embed.set_footer(text="Server Patches", icon_url=client.user.avatar_url)
                     embed.timestamp = datetime.datetime.utcnow()
                     await message.channel.send(embed=embed)

                if message.content.startswith(CONFIG.PREFIX + "ping"):
                    latency = str(client.latency)[0:4]
                    await message.channel.send("Bot Ping = " + latency + "ms")

        else:
            if message.content.startswith(CONFIG.PREFIX):
                client.AppInfo = await client.application_info()
                embed = discord.Embed(title="Keine Lizenz", description=":x: Hey, dieser Server hat keine Lizenz! Für eine Lizenz wende dich\nbitte an " + str(client.AppInfo.owner), color=0xff0000)
                embed.set_footer(text="Server Patches", icon_url=client.user.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()
                await message.channel.send(embed=embed)



client.run(CONFIG.TOKEN)
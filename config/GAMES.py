import discord

__games__ = [
    (discord.ActivityType.playing, 'mit Python'),
    (discord.ActivityType.watching, 'über {guilds} Server'),
    (discord.ActivityType.watching, 'über {members} Mitglieder'),
    (discord.ActivityType.listening, '&bot-info')
]
__gamesTimer__ = 2 * 60

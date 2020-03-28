![Avatar](CherryBot-Banner.png)
=====================

[![Python3](https://img.shields.io/badge/python-3.8-blue.svg)](https://github.com/IBimsEinMystery/CherryBot)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/IBimsEinMystery/CherryBot/master/LICENSE)
[![Discord Server](https://img.shields.io/badge/Support-Discord%20Server-blue.svg)](https://discord.gg/ZMDJKUf)

Commands List
-------------
**Info:** Prefix `&`

### Generell ###

Befehle | Beschreibung
----------------|--------------
`help` | Zeigt eine Liste aller öffentlichen Befehle
`bot-info` | Zeigt dir Infos über den Bot an
`ping` | Zeigt dir den Ping zwischen Bot und Discord an
`invite` | Schickt dir einen Einladungslink für den Bot
`src` | Schickt den GitHub Link zum Bot
`set-news [Kanal-ID] [Nachrichten-ID]` | Setzt die Nachricht für die News
`sv-news` | Zeigt dir die News Nachricht
`sv-info` | Zeigt dir infos über den Server an
`whois <@User#1234>` | Zeigt dir Infos über User
`kick [@User#1234]` | Kickt den angegebenen User vom Server
`register [uplay/steam/epicgames] [Name]` | Verknüpft euren Nickname mit eurem Discord Account
`uplay <@User#1234/unlink>` | Zeigt euren oder vom User den Uplay Namen an, oder entfernt die Verknüpfung
`steam <@User#1234/unlink>` | Zeigt euren oder vom User den Steam Namen an, oder entfernt die Verknüpfung
`epicgames <@User#1234/unlink>` | Zeigt euren oder vom User den Epic Games Namen an, oder entfernt die Verknüpfung


Starten
-------------
Entweder ihr startet das Script direkt über `python3.8 main.py` oder erstellt eine systemd unit:

    [Unit]
    Description=CherryBot Discord Bot
    After=multi-user.target
    [Service]
    WorkingDirectory=/home/cherry/CherryBot
    Environment="PYTHONHASHSEED=0"
    User=cherry
    Group=cherry
    ExecStart=/usr/bin/python3.8 /home/cherry/CherryBot/main.py
    Type=idle
    Restart=on-failure
    RestartSec=15
    TimeoutStartSec=15

    [Install]
    WantedBy=multi-user.target

Nach `/etc/systemd/system/discord.service` kopieren und anpassen. Nicht vergessen die Unit zu starten via `sudo systemctl start discord.service` bzw. Autostart via `sudo systemctl enable discord.service`.


Einstellungen
-------------
Vor dem Start muss im Ordner `config` eine Datei namens `config.py` verändert werden werden:

    TOKEN = "DEIN BOT TOKEN"
    PREFIX = "&"
    clientLogout = False

In `games.py` kann man die Titel der "Spiele Presence" anpassen. Platzhalter wie `{guilds}` oder `{members}` sind möglich.

    __games__ = [
    (discord.ActivityType.playing, 'mit Python'),
    (discord.ActivityType.watching, 'auf {guilds} Server'),
    (discord.ActivityType.watching, 'auf {members} Mitglieder'),
    (discord.ActivityType.listening, '&help')
    ]
    __gamesTimer__ = [
        2 * 60,
        1 * 35,
        2 * 27,
        3 * 23,
        5 * 9
    ]

Support
-------------
Falls ihr Hilfe benötigt kommt auf meinen Discord Server: `https://discord.gg/ZMDJKUf`

Was ihr benötigt
-------------

    python = 3.7 oder besser
    discord.py = 1.0 oder besser
    aiohttp
    websockets
    chardet
    pytz
    pillow

License
-------------
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

# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
#

"""
Lyrics Plugin Syntax:
       .lyrics <aritst name> - <song nane>
"""
import os
import lyricsgenius
import random

from userbot.events import register
from userbot import CMD_HELP, LOGS, GENIUS

"""Genius(lyrics) staff"""
GApi = GENIUS
genius = lyricsgenius.Genius(GApi)


@register(outgoing=True, pattern="^.lyrics(?: |$)(.*)")
async def lyrics(lyric):
    if r"-" in lyric.text:
        pass
    else:
        return await lyric.edit("`Aborted: Please use '-' as divider for **<artist> "
                                "& <song name>**`\neg: `Nicki Minaj - Super Bass`")

    if GApi is None:
        return await lyric.edit(
            "`Provide genius access token to Heroku Var first kthxbye!`")
    else:
        try:
            args = lyric.text.split('.lyrics')[1].split('-')
            artist = args[0].strip(' ')
            song = args[1].strip(' ')
        except Exception:
            return await lyric.edit("`LMAO please provide artist and song names`")

    if len(args) < 1:
        return await lyric.edit("`Please provide artist and song names`")

    await lyric.edit(f"`Searching lyrics for {artist} - {song}...`")

    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None

    if songs is None:
        return await lyric.edit(f"Song **{artist} - {song}** not found!")
    if len(songs.lyrics) > 4096:
        await lyric.edit("`Lyrics is too big, view the file to see it.`")
        with open("lyrics.txt", "w+") as f:
            f.write(f"Search query: \n{artist} - {song}\n\n{songs.lyrics}")
        await lyric.client.send_file(
            lyric.chat_id,
            "lyrics.txt",
            reply_to=lyric.id,
            )
        os.remove("lyrics.txt")
    else:
        await lyric.edit(f"**Search query**: \n`{artist} - {song}`\n\n```{songs.lyrics}```")
    return


@register(outgoing=True, pattern="^.iff$")
async def pressf(f):
    """Pays respects"""
    args = f.text.split()
    arg = (f.text.split(' ', 1))[1] if len(args) > 1 else None
    if len(args) == 1:
        r = random.randint(0, 3)
        LOGS.info(r)
        if r == 0:
            await f.edit("┏━━━┓\n┃┏━━┛\n┃┗━━┓\n┃┏━━┛\n┃┃\n┗┛")
        elif r == 1:
            await f.edit("╭━━━╮\n┃╭━━╯\n┃╰━━╮\n┃╭━━╯\n┃┃\n╰╯")
        else:
            arg = "F"
    if arg is not None:
        out = ""
        F_LENGTHS = [5, 1, 1, 4, 1, 1, 1]
        for line in F_LENGTHS:
            c = max(round(line / len(arg)), 1)
            out += (arg * c) + "\n"
        await f.edit("`" + out + "`")


CMD_HELP.update({
    "lyrics":
    ">`.lyrics <artist name> - <song name>`"
    "\nUsage: Get lyrics for song"
})

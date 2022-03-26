#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author: Kharidiron
@File: NowPlaying.py
@Time: 2022-03-26 02:20 UTC
@Desc: Providing Discord with some presence for non-supported games and applications.
"""

import asyncio
import json

import nest_asyncio
from pypresence import Presence
import PySimpleGUI as sg

nest_asyncio.apply()

State = {"connected": False}
with open('discord-ids.json') as json_file:
    Systems = json.load(json_file)

layout = [
    [sg.Text("Discord Rich Presence Setter")],
    [sg.HSeparator()],
    [sg.Text("System:", size=10),
     sg.OptionMenu(values=tuple(Systems.keys()), size=15, key='-system-'),
     sg.Button("Change system")],
    [sg.Text("Game:", size=10), sg.InputText(size=30, key='-game-')],
    [sg.Text("Status:", size=10), sg.InputText(size=30, key='-state-')],
    [sg.Text(size=50, key='-status-')],
    [sg.HSeparator()],
    [sg.Button("Submit"), sg.Push(), sg.Button("Quit")],
]
window = sg.Window("NowPlaying", layout)


async def set_or_update(client, values):
    if not State["connected"]:
        client.client_id = Systems[values['-system-']]
        client.connect()
        State["connected"] = True

    window['-status-'].update('')
    client.update(details=values['-game-'], state=values['-state-'])


def check(values):
    if not values['-system-']:
        window['-status-'].update('You must specify a system before attempting to set a status',
                                  text_color='red')
        return False
    if not values['-game-'] or not values['-state-']:
        window['-status-'].update('You must specify a game and status',
                                  text_color='red')
        return False
    return True


async def gui_loop(client):
    while True:
        event, values = window.read()

        if event == "Quit" or event == sg.WIN_CLOSED:
            break
        if event == "Change system":
            if not check(values):
                continue

            client.clear()
            State["connected"] = False

            await set_or_update(client, values)
        if event == "Submit":
            if not check(values):
                continue

            await set_or_update(client, values)

    window.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    RPC = Presence("", loop=loop)

    try:
        asyncio.run(gui_loop(RPC))
    except Exception as e:
        print(e)
    finally:
        loop.close()

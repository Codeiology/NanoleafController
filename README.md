# NanoleafController

Sends JSON payloads to your Nanoleaf panel shapes to control them from the command line!

# Setup

Before you start, it will give you an inital setup program. Make sure you enter all the values *PERFECTLY.

`pip3 install -r requirements.txt`
`python3 nanoleaf.py`

*only tested on macOS

# Features

Changing scenes

Changing brightness

Viewing device info

Viewing scene list

Send your own JSON payloads!

# Custom JSON payloads

This tool allows you to send custom JSON payloads!

A list of custom payload ideas:

Change scene: API endpoint `effects`. Payload: `{"select": "(scene name)"}`

Change brightness: API endpoint `state`. Payload: `{"brightness": {"value": (percentage number brightness)}}`

Turn on/off: API endpoint `state`. Payload: `{"on": {"value": (true/false)}}

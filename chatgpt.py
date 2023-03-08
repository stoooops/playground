#!/usr/bin/env python3
# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import sys
from typing import List

import openai

first_msg = "hello"
if len(sys.argv) > 1:
    first_msg = " ".join(sys.argv[1:])

messages = [
    {
        "role": "system",
        "content": "You are a command-line interface to an AI assistant.",
    },
    {"role": "user", "content": "Say ACK."},
    {
        "role": "assistant",
        "content": "ACK.",
    },
    {"role": "user", "content": first_msg},
]

ANSII = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "greenbold": "\033[1;32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "bluebold": "\033[1;34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m",
    "lightgreen": "\033[92m",
    "gray": "\033[90m",
}
NC = "\033[0m"

ai_color = "greenbold"
ai_text_color = "gray"
user_color = "bluebold"

while True:
    try:
        # call API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        msg = response["choices"][0]["message"]
        messages.append(msg)
        role = msg["role"].replace("assistant", "bot")
        content = msg["content"]
        print(f"{ANSII[ai_color]}{role}{NC}: {ANSII[ai_text_color]}{content}{NC}\n")
        # reply
        reply_lines: List[str] = []
        while True:
            prefix = ""
            if len(reply_lines) == 0:
                prefix = f"{ANSII[user_color]}You: {NC}"
            line = input(prefix)
            if not line:  # empty line
                break
            reply_lines.append(line)

        reply = "\n".join(reply_lines)
        messages.append({"role": "user", "content": reply})
    except KeyboardInterrupt:
        break

#!/usr/bin/env python

import socket
import time
import re
import os

from config import *

s = socket.socket()
s.connect((host, port))
s.send("PASS {}\r\n".format(token).encode("utf-8"))
s.send("NICK {}\r\n".format(name).encode("utf-8"))
s.send("JOIN {}\r\n".format(channel).encode("utf-8"))

chatExpr=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
output = open("../ticker.txt", "w")

writtenChars = 0

while True:
    response = s.recv(1024).decode("utf-8")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
    else:
        if 'PRIVMSG' in response:
            username = re.search(r"\w+", response).group(0) # return the entire match
            message = chatExpr.sub("", response)
            username = username.rstrip()
            message = message.rstrip()

            print (username + ": " + message)

            if writtenChars > 450:
                output.seek(0)
                output.truncate()
                writtenChars = 0
                print ("Output File Truncated")

            outputStr = username.upper() + ": " + message.upper() + "   "
            writtenChars += len(outputStr)
            output.write(outputStr)
            output.flush()
            os.fsync(output.fileno())
        else:
            print ("Twitch System: " + response)


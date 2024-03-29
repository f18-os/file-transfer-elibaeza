#! /usr/bin/env python3

# Echo client program
import socket, sys, re

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50000"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)
responds = 0

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()
try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)
    
    print("Please choose an option:\n")
    responds = input()
    print(responds)
    
try: #open input file
    inputFile = open("mySendMsg.txt", 'rb')
    message = inputFile.read(1024).decode() #remove newline \n
    message = message.strip()
    message = str.encode(message) #encode back to bytes
    framedSend(s, message, debug) #send the message from the file
    inputFile.close()
    print("sent:", message)
    print("received:", framedReceive(s, debug))
    
except IOError:
    print("File does not exist in this directory")

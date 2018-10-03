#! /usr/bin/env python3

import sys, os, socket
sys.path.append("../lib")       # for params
import params
messageLines= list()

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50000),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            payload = framedReceive(sock, debug)
            if debug: print("rec'd: ", payload)
            if not payload:
                if debug: print("child exiting")
                sys.exit(0)
            payload += b"!"             # make emphatic!
            framedSend(sock, payload, debug)
            if (len(payload)>100): #check if payloads length is lager than 100
                print ("Message too large")
                sock.close()
            else: #write to a file in the server
                messageLines.append(payload.decode())
                try:
                    outputFile = open("myRecievedMsg.txt", 'w')
                    
                    for line in messageLines:
                        outputFile.write(line + '\n')
                    outputFile.close()
                    print ("recieved: ", payload)
                except IOError:
                    print("Something went wrong")
    sock.close()

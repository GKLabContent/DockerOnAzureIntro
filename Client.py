#! /usr/bin/python3

#This file serves as a test client for the MessageServer.py script
#There are two message types that can be tested:
#1 - Ping.  This returns the local IP address and server name of the message server
#2 - Load Test. This runs a load test on the server for a specified number of minutes.
import socket
import os
import json
import sys, getopt

class TCP:
    def sendMessage(self,payload,host,port):
        self.s = socket.socket()
        self.host = host
        self.s.connect((host,port))
        self.s.sendall(payload.encode())
        return self.getResponse(0)

    def getResponse(self,timeOut):
        result = self.s.recv(8192)
        if result != "":
            return result.decode()
        else:
            return "No data"

    def close(self):
        self.s.close()

if __name__ == "__main__":
    tcp = TCP()
    argsv = sys.argv[1:]
    host = ""
    port = 0
    command = ""
    minutes = ""
    try:
        opts, args = getopt.getopt(argsv,"a:p:c:m:",["address=","port=","command=","minutes="])
    except getopt.GetoptError:
        print('Usage: Client.py -a <address> -p <port> -c <command> -m <minutes>')
        sys.exit(2)
    for opt,arg in opts:
        if opt in ("-a","--address"):
            host = arg
        elif opt in ("-p","--port"):
            port = int(arg)
        elif opt in ("-c", "--command"):
            command = arg
        elif opt in ("-m", "--minutes"):
            minutes = arg
    if host == "":
        host = input("Enter remotehost address (IP or DNS): ")
    if port == 0:
        port = int(input("Enter a port number:"))
    if command == "":
        command = input("Enter a command (1 = echo, 2 = load): ")
    if command == "2":
        if minutes == "":
            minutes = input("Enter the number of minutes for load: ")
        command += minutes
    print(tcp.sendMessage(command,host,port))

        

#!/usr/bin/python3

#This script runs a "messaging service".  It accepts a TCP request over
#port 8080 and returns a response.  There are two command messages that
#the message server supports - ping (1) and load test (2).
import asyncore
import socket, sys, struct, os
import uuid
import datetime
from multiprocessing import Process, Pool
import json

tcpPort = 8080

def wasteProcessor(endTime):
    lcv = 0
    now = datetime.datetime.now()
    while now < endTime:
        lcv = lcv + 1
        lcv = lcv % 100000
        now = datetime.datetime.now()

def getips():
    ips = []
    results = os.popen('ip addr | grep "inet " | grep -v "host"').read().strip().split("\n")
    for r in results:
        ips.append(r.split(" ")[1].split("/")[0])
    return ips
                       
def get_details():
    result = "IPv4 Addresses: "
    for ip in getips():
        result += ip + ";"
    result +=  "\n Computer Name: {}".format(socket.gethostname())
    return result

def save_message(data):
    directory = "/data/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    now = datetime.datetime.now()
    fileName = directory + socket.gethostname() + now.strftime("%Y%m%dT%H%M%S.%f")
    command = data[0]
    payload = data[1:]
    with open(fileName, 'w') as f:
        f.write(json.dumps({'command':command, 'payload':payload}))
    

class TCPHandler(asyncore.dispatcher_with_send):
    def __init__(self,sock,addr):
        asyncore.dispatcher_with_send.__init__(self,sock)
        self.data = ""
        self.addr = addr[0]

    def handle_read(self):
        print("Receiving TCP data ...")
        data = self.recv(8192)
        if data:
            data = data.decode()
            command = data[0]
			#write message to disk
            save_message(data)
            if command == '1':
                #Process echo
                message = get_details()
            else:
                #Process Load
                payload = data[1:]
                if payload.isnumeric():
                    now = datetime.datetime.now()
                    delta = int(payload)
                    if delta > 10:
                        delta = 10
                    if delta < 1:
                        delta = 1
                    endtime = now + datetime.timedelta(minutes=delta)
                    pool = Pool(processes=6)
                    [pool.apply_async(wasteProcessor,(endtime,)) for i in range(5)]
                    
                    message = "Processed load for {0} minutes from {1} to {2} \n {3}".format(payload,now,endtime, get_details())
                else:
                    message = "Processing load - invalid data: {0} \n {3}".format(payload, get_details())
            result = "Received {0} \n Processed {1}".format(command, message)
            self.sendall(result.encode())
        else:
            self.close()

class TCPServer(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', tcpPort))
        self.listen(5)
        print("TCP listening on port {}".format(tcpPort))

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print('Incoming connection from {}'.format(repr(addr)))
            handler = TCPHandler(sock, addr)



if __name__ == "__main__":
    
    tserver = TCPServer()

    asyncore.loop()
    print("Past loop")

FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install -y python python3 nano

COPY MessageServer.py /usr/msgsvr/ 
COPY MessageServer.sh /usr/msgsvr/ 
COPY msgsvrstart.sh /etc/init.d

RUN chmod +x /usr/msgsvr/MessageServer.py
RUN chmod +x /usr/msgsvr/MessageServer.sh


CMD ["/usr/msgsvr/MessageServer.py"]
mkdir /usr/msgsvr
cp MessageServer.py /usr/msgsvr
cp utils.py /usr/msgsvr
cp msgsvrstart.sh /etc/init.d

chmod +x /usr/msgsvr/MessageServer.py
chmod +x /etc/init.d/msgsvrstart.sh

update-rc.d msgsvrstart.sh defaults
/usr/msgsvr/MessageServer.py &

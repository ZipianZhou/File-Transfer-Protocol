import socket
import json
import struct
import os

client_dir='/Users/michelle.zhou/PycharmProjects/FTP/main/CLIENT_DIR/archive'

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("127.0.0.1",8084))

def get(filename):
    pack_bt = client.recv(4)
    header_length = struct.unpack('i', pack_bt)[0]
    header_js = client.recv(header_length)
    header = json.loads(header_js)
    totalsize = header.get("file_size")
    print(totalsize)

    with open('%s/%s' % (client_dir, filename), 'wb') as f:
        cur_size = 0
        while cur_size < totalsize:
            rec = client.recv(1024)
            f.write(rec)
            cur_size += len(rec)

def upload(filename):
    header={
        'filename':filename,
        'file_size':os.path.getsize('%s/%s'%(client_dir,filename)),
        'md5':'xxdrxxxx'
    }
    header_bytes=json.dumps(header).encode('utf-8')
    header_send=struct.pack('i',len(header_bytes))
    client.send(header_send)
    client.send(header_bytes)

    with open('%s/%s'%(client_dir,filename),'rb') as f:
        for line in f:
            client.send(line)

while True:
    cmd=input(">>: ") #get test.txt
    result= cmd.split()[0]
    filename= cmd.split()[1]
    client.send(cmd.encode('utf-8'))
    if result == 'get':
        get(filename)
    if result == 'upload':
        upload(filename)



client.close()


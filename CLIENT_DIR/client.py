import socket
import json
import struct
import os

class client:
    def __init__(self):
        self.client_dir=os.path.dirname(os.path.abspath(__file__))+'/archive'

        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def start(self):
        self.client.connect(("127.0.0.1",8084))

    def get(self,filename):
        pack_bt = self.client.recv(4)
        header_length = struct.unpack('i', pack_bt)[0]
        header_js = self.client.recv(header_length).decode('utf-8')
        header = json.loads(header_js)
        totalsize = header.get("file_size")
        # print(totalsize)

        with open('%s/%s' % (self.client_dir, filename), 'wb') as f:
            cur_size = 0
            while cur_size < totalsize:
                rec = self.client.recv(1024)
                f.write(rec)
                cur_size += len(rec)

    def upload(self,filename):
        header={
            'filename':filename,
            'file_size':os.path.getsize('%s/%s'%(self.client_dir,filename)),
            'md5':'xxdrxxxx'
        }
        header_bytes=json.dumps(header).encode('utf-8')
        header_send=struct.pack('i',len(header_bytes))
        self.client.send(header_send)
        self.client.send(header_bytes)

        with open('%s/%s'%(self.client_dir,filename),'rb') as f:
            for line in f:
                self.client.send(line)

    def run(self):
        while True:
            cmd=input(">>: ") #get test.txt
            result= cmd.split()[0]
            filename= cmd.split()[1]
            self.client.send(cmd.encode('utf-8'))
            if result == 'get':
                self.get(filename)
            if result == 'upload':
                self.upload(filename)

    def close(self):
        self.client.close()


s=client()
s.start()
s.run()


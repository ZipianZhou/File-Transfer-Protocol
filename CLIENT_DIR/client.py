import socket
import json
import struct
import os
import time

class client:
    def __init__(self):
        self.client_dir=os.path.dirname(os.path.abspath(__file__))+'/archive'

        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    def start(self):
        self.client.connect(("127.0.0.1",8089))
        self.login_pack()

    def login_pack(self):
        name=input('UserId:')
        password=input('Password:')
        login_dict={
            'username':name,
            'password':password
        }
        login_bytes=json.dumps(login_dict).encode('utf-8')
        login_info=struct.pack('i',len(login_bytes))
        self.client.send(login_info)
        self.client.send(login_bytes)
        result=self.client.recv(4)
        result_length=struct.unpack('i',result)[0]
        result_bytes=self.client.recv(result_length).decode('utf-8')
        resultf=json.loads(result_bytes).get('login')
        if resultf == 'yes':
            pass
        else:
            self.login_pack()



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
                self.percentage(cur_size,totalsize)
            print ("")


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
        total_size=os.path.getsize('%s/%s'%(self.client_dir,filename))
        cur_size=total_size

        with open('%s/%s'%(self.client_dir,filename),'rb') as f:
            while cur_size>1024:
                self.client.send(f.read(1024))
                cur_size-=1024
            self.client.send(f.read(cur_size))

    def run(self):
        while True:
            cmd=input(">>: ") #get test.txt
            result= cmd.split(' ')[0]
            filename= cmd.split(' ')[1]
            self.client.send(cmd.encode('utf-8'))
            if result == 'get':
                self.get(filename)
            if result == 'upload':
                self.upload(filename)

    def percentage(self,real_size,all_size):
        print("{:5.2%}".format(real_size/all_size), end='\r')
        time.sleep(0.1)

    def close(self):
        self.client.close()


s=client()
s.start()
s.run()



import socket
import json
import os
import struct
import subprocess
import user

class server:

    def __init__(self):
        self.server_dir = os.path.dirname(os.path.abspath(__file__)) + '/shared'
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("127.0.0.1", 8089))
        self.dir = self.server_dir


    def start(self):
        print("starting server...")
        self.server.listen(5)


    def get(self,filename,conn):
        header = {
            "file_name": filename,
            "file_size": os.path.getsize("%s/%s" % (self.server_dir, filename)),
            "md5": 'xxcssxxx'
        }
        header_bt = json.dumps(header).encode('utf-8')
        pack_bt = struct.pack('i', len(header_bt))
        conn.send(pack_bt)
        conn.send(header_bt)
        total_size=os.path.getsize("%s/%s" % (self.server_dir, filename))
        cur_size=total_size
        print(type(cur_size))
        with open('%s/%s' % (self.server_dir, filename), 'rb') as f:
            # for line in f:
            #     conn.send(line)
            while cur_size>1024:
                conn.send(f.read(1024))
                cur_size-=1024
            conn.send(f.read(cur_size))


    def upload(self,filename,conn):
        header_bytes=conn.recv(4)
        header_length=struct.unpack('i', header_bytes)[0]
        header_json=conn.recv(header_length)
        header=json.loads(header_json)
        total_size=header.get('file_size')

        with open('%s/%s'%(self.server_dir,filename),'wb') as f:
            cur_rec=0
            while cur_rec < total_size:
                rec=conn.recv(1024)
                f.write(rec)
                cur_rec+=len(rec)

    def exexute(self):
        pass


    def run(self):
        conn, client_addr = self.server.accept()
        while True:
            login_dict=conn.recv(4)
            login_length=struct.unpack('i',login_dict)[0]
            login_info=conn.recv(login_length)
            login=json.loads(login_info)
            username=login.get('username')
            password=login.get('password')
            if user.login(username,password):
                value='yes'
                print('good')
                user_log = {
                    'login': value
                }
                user_bytes = json.dumps(user_log).encode('utf-8')
                user_send = struct.pack('i', len(user_bytes))
                conn.send(user_send)
                conn.send(user_bytes)
                while True:
                    try:
                        cmd=conn.recv(1024)
                        cmd=cmd.decode('utf-8').split()
                        option=cmd[0]
                        filename=cmd[1]
                        if not cmd: break
                        if option == 'get':
                            self.get(filename,conn)
                        if option == 'upload':
                            self.upload(filename,conn)

                    except ConnectionResetError:
                        break
            else:
                print('not good')
                value='no'
                user_log={
                    'login':value
                }
                user_bytes=json.dumps(user_log).encode('utf-8')
                user_send=struct.pack('i',len(user_bytes))
                conn.send(user_send)
                conn.send(user_bytes)




    def close(self,conn):
        conn.close()

        self.server.close()

s=server()
s.start()
s.run()
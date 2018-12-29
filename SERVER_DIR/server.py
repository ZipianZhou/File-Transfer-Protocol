import socket
import json
import os
import struct

class server:

    def __init__(self):
        self.server_dir = os.path.dirname(os.path.abspath(__file__)) + '/shared'
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("127.0.0.1", 8084))


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
        with open('%s/%s' % (self.server_dir, filename), 'rb') as f:
            for line in f:
                conn.send(line)


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

    def run(self):
        while True:
            conn, client_addr = self.server.accept()
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

    def close(self,conn):
        conn.close()

        self.server.close()

s=server()
s.start()
s.run()
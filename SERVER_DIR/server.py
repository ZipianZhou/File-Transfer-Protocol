import socket
import json
import os
import struct

server_dir="/Users/michelle.zhou/PycharmProjects/FTP/main/SERVER_DIR/shared"
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind(("127.0.0.1",8084))
server.listen(5)

print("starting server...")
conn,client_addr=server.accept()
def get(filename):
    header = {
        "file_name": filename,
        "file_size": os.path.getsize("%s/%s" % (server_dir, filename)),
        "md5": 'xxcssxxx'
    }
    header_bt = json.dumps(header).encode('utf-8')
    pack_bt = struct.pack('i', len(header_bt))
    conn.send(pack_bt)
    conn.send(header_bt)
    with open('%s/%s' % (server_dir, filename), 'rb') as f:
        for line in f:
            conn.send(line)

def upload(filename):
    header_bytes=conn.recv(4)
    header_length=struct.unpack('i', header_bytes)[0]
    header_json=conn.recv(header_length)
    header=json.loads(header_json)
    total_size=header.get('file_size')

    with open('%s/%s'%(server_dir,filename),'wb') as f:
        cur_rec=0
        while cur_rec < total_size:
            rec=conn.recv(1024)
            f.write(rec)
            cur_rec+=len(rec)


while True:
    try:
        cmd=conn.recv(1024)
        cmd=cmd.decode('utf-8').split()
        option=cmd[0]
        filename=cmd[1]
        if not cmd: break
        if option == 'get':
            get(filename)
        if option == 'upload':
            upload(filename)



    except ConnectionResetError:
        break

conn.close()

server.close()
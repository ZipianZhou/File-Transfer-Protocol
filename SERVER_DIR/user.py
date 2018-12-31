import hashlib
import time
import uuid
import configparser

#
# def generateId():
#     return hashlib.md5(str.encode(str(time.time()),"utf-8")).hexdigest()
#     # return uuid.uuid4().int >> 128
#
#
# print(generateId())


def login(username,password):
    conf = configparser.ConfigParser()
    conf.read('/Users/michelle.zhou/PycharmProjects/FTP/main/SERVER_DIR/config.ini')
    # print (conf.options("user1"))
    if username not in conf.keys():
        print('User has not yet registered.')
        return False
    else:
        realpass=conf[username]['password']
        if password != realpass:
            print('password failed')
            return False
        if password == realpass:
            print('login success!')
            return True



#
# print(conf['user1']['password'])
#

#
# for i in range(101):
#     print(str(i) + " %", end='\r')
#     time.sleep(0.1)
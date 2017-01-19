import socket
import random

MAX = 65535
target = '127.0.0.1'
port = 9999

def connect_server():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    sock.connect((target,port))
    
    data = check(sock,data='Hello')
    print data

    while True:
        data = raw_input("INPUT:")
        recv_data = check(sock=sock,data=data)
        print recv_data    #make sure server receive our data

        while True:
            sock.settimeout(99999999)
            data = sock.recv(MAX)  #receive data from server
            if random.random() < 0.5:
                print "Drop packet"
                continue   #make sure the packet will not be lost
            sock.send('Recevie')
            print data #print what server sent
            break


def check(sock=None,delay=0.1,longest_time=2,data=None):
    while True:
        sock.settimeout(delay)
        try:
            sock.send(data)
            recv_data = sock.recv(MAX)
        except socket.timeout:
            delay *= 2
            if delay > longest_time:
                raise RuntimeError('I think the Server is down')
        else:
            break
    
    return recv_data
    

if __name__ == "__main__":
    connect_server()
import socket
import random

MAX = 65535

def client_handle():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1',9999))
    
    while True:
        data,addr = sock.recvfrom(MAX)
        if random.random() < 0.5:
            print "Drop packet"
            continue
        print data
        sock.sendto(data,addr)
        break
    
    while True:
        sock.settimeout(9999999)
        data,addr = sock.recvfrom(MAX)
        if random.random() < 0.5:
            print "Drop packet"
            continue
        sock.sendto("Receive",addr)  #send "receive" to let client know we receivced
        print addr[0]+':'+data  #print what client sent

        data = raw_input('INPUT:')
        recv_data,addr = check(data=data,sock=sock,addr=addr) #send and receivce data
        print addr[0]+":"+recv_data #print recevie


def check(sock=None,delay=0.1,longest_time=2,data=None,addr=None):
    while True:
        sock.settimeout(delay)
        try:
            sock.sendto(data,addr)
            recv_data,address = sock.recvfrom(MAX)
        except socket.timeout:
            delay *= 2
            if delay > longest_time:
                raise RuntimeError('I think the Client is down')
        else:
            break
    
    return recv_data,address


if __name__ == "__main__":
    client_handle()
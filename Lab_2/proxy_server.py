#!/usr/bin/env python3
from ast import arg
import socket, sys
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def proxy_handler(conn, proxy, addr):
    full_data_proxy = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)
    proxy.sendall(full_data_proxy)
    time.sleep(0.5)
    proxy.shutdown(socket.SHUT_WR)
    full_data = b""
    while True:
        data = proxy.recv(4096)
        if not data:
            break
        full_data += data            
    conn.send(full_data)



def main():
    proxy_host = 'www.google.com'
    proxy_port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

            # create new socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as p:

                remote_ip = get_remote_ip(proxy_host)
                p.connect((remote_ip, proxy_port))


                #recieve data, wait a bit, then send it back
                process = Process(target=proxy_handler, arg=(conn, p, addr))
                process.daemon = True
                process.start()

            conn.close()

if __name__ == "__main__":
    main()

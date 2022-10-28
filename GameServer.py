#!/usr/bin/python3

import socket
import threading
import sys

if sys.argv[1].isdigit():
    SERVER_PORT = int(sys.argv[1]) #Parameter 1
else:
    print("Error: Listening port is not an integer")
    exit(1)
FILE_PATH = sys.argv[2] #Parameter 2

print(f"server port = {SERVER_PORT}, file path = {FILE_PATH}")

test = "/login kritik 11"
    
success = "1001 Authentication successful"
failure = "1002 Authentication failed"

def thd_func(client):
    connectionSocket, addr = client    
    msg = connectionSocket.recv(1024)
    msg = msg.decode()
    
    while msg != test:
    
        print(msg)
        
        connectionSocket.send(failure.encode())
        
        msg = connectionSocket.recv(1024)
        msg = msg.decode()
        # connectionSocket.close()
        
    connectionSocket.send(success.encode())
        
    connectionSocket.close()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind( ("", SERVER_PORT) )

serverSocket.listen(5)

print("The server is ready to receive")

while True:
    
    client = serverSocket.accept()
    newthd = threading.Thread(target=thd_func, args=(client,))
    newthd.start()
    
serverSocket.close()
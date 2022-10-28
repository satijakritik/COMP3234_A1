#!/usr/bin/python3

import socket
import sys

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST_NAME = sys.argv[1] #Parameter 1

if sys.argv[2].isdigit():
    SERVER_PORT = int(sys.argv[2]) #Parameter 2
else:
    print("Error: Server's listening port is not an integer")
    exit(1)

clientSocket.connect( (HOST_NAME, SERVER_PORT) )

auth = False

while auth == False:
# Get input for sending
    user_name = input("Please input your username: ")
    password = input("Please input your password: ")

    msg = f"/login {user_name} {password}"

    clientSocket.send(msg.encode())

    response = clientSocket.recv(1024)
    
    if response.decode() == "1001 Authentication successful":
        auth = True
    
    print(response.decode())
    
    

clientSocket.close()
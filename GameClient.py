#!/usr/bin/python3

import socket
import sys

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_name = sys.argv[1] #Parameter 1
server_port = int(sys.argv[2])

# if sys.argv[2].isdigit():
#     SERVER_PORT = int(sys.argv[2]) #Parameter 2
# else:
#     print("Error: Server's listening port is not an integer")
#     exit(1)

clientSocket.connect( (host_name, server_port) )

auth = False
in_game_hall = False

while auth == False:
# Get input for sending
    user_name = input("Please input your username:\n")
    password = input("Please input your password:\n")

    msg = f"/login {user_name} {password}"

    clientSocket.send(msg.encode())

    response = clientSocket.recv(1024)
    
    if response.decode() == "1001 Authentication successful":
        auth = True
        in_game_hall = True
    
    print(response.decode())
    
while in_game_hall:
    cmd = input("")
    clientSocket.send(cmd.encode())
    
    response = clientSocket.recv(1024)
    # response_code = (response.decode()).split()[0]
    
    if response.decode() == "4001 Bye bye":
        in_game_hall = False
        print(response.decode())
        print("Client ends")
        clientSocket.close()
        exit(1)
        
    if response.decode() == "3011 Wait":
        
        # response = clientSocket.recv(1024)
        print(response.decode())
        
        while response.decode() != "3012 Game started. Please guess true or false":
            response = clientSocket.recv(1024)
            # pass
        print(response.decode())
        cmd = input("")
        clientSocket.send(cmd.encode())
        
        response = clientSocket.recv(1024)
        # print(response.decode())
    
    if response.decode() == "3012 Game started. Please guess true or false":
        print(response.decode())
        cmd = input("")
        clientSocket.send(cmd.encode())
        
        response = clientSocket.recv(1024)
        # print(response.decode())
    
    print(response.decode())

clientSocket.close()
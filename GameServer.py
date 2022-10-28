#!/usr/bin/python3

import socket
import threading
import sys

#-----Global variables----#
STATES = {0: "OUT_OF_HOUSE", 1: "IN_THE_GAME_HALL", 2: "WAITING_IN_ROOM", 3: "PLAYING_A_GAME"}
NUM_OF_ROOMS = 5

server_port = int(sys.argv[1]) #Parameter 1
file_path = sys.argv[2] #Parameter 2

#-------------------------

# if sys.argv[1].isdigit():
#     server_port = int(sys.argv[1]) #Parameter 1
# else:
#     print("Error: Listening port is not an integer")
#     exit(1)

print(f"server port = {server_port}, file path = {file_path}")

def thd_func(client):
    connectionSocket, addr = client    
    msg = connectionSocket.recv(1024)
    msg = msg.decode()
    
    user_state = 0 #OUT_OF_HOUSE
    
    test = "/login kritik 11"
    success = "1001 Authentication successful"
    failure = "1002 Authentication failed"
    
    while msg != test:
    
        # print(msg)
        
        connectionSocket.send(failure.encode())
        
        msg = connectionSocket.recv(1024)
        msg = msg.decode()
        
    connectionSocket.send(success.encode())
    
    user_state = 1 #IN_THE_GAME_HALL
    
    # cmd_list = ["\list", "\enter", "\exit"]
    
    msg = connectionSocket.recv(1024)
    msg = msg.decode()
    
    exit = "4001 Bye bye"
    
    while msg != "/exit": #exit
        
        print(msg)
        
        connectionSocket.send(msg.encode())
        
        msg = connectionSocket.recv(1024)
        msg = msg.decode()
        
    connectionSocket.send(exit.encode())
    
    connectionSocket.close()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind( ("", server_port) )

serverSocket.listen(5)

print("The server is ready to receive")

while True:
    
    client = serverSocket.accept()
    newthd = threading.Thread(target=thd_func, args=(client,))
    newthd.start()
    
serverSocket.close()
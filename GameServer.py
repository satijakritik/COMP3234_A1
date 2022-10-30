#!/usr/bin/python3

import socket
import threading
import sys
import random

#-----Global variables----#
STATES = {0: "OUT_OF_HOUSE", 1: "IN_THE_GAME_HALL", 2: "WAITING_IN_ROOM", 3: "PLAYING_A_GAME"}
CMD_LIST_FOR_STATE = {0: ["/login"], 1: ["/exit", "/list", "/enter"], 2: [], 3: ["/guess"]}
NUM_OF_ROOMS = 5

server_port = int(sys.argv[1]) #Parameter 1
file_path = sys.argv[2] #Parameter 2
room_list = [0 for i in range(NUM_OF_ROOMS)]
room_member_list = {1: {}, 2: {}, 3: {}, 4: {}, 5: {}}
user_state = {}

with open(file_path) as file:
    user_data = [(line.rstrip()).split(":") for line in file]
    
print(user_data)

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
    cmd_args = msg.split()
    cmd = cmd_args[0] #/login
    user_name = cmd_args[1]
    password = cmd_args[2]
    
    success = "1001 Authentication successful"
    failure = "1002 Authentication failed"
    exit = "4001 Bye bye"
    
    user_state[client] = 0 #OUT_OF_HOUSE
    # print(room_list)

    game_over = False
    
    # user_state[client] = 0
    cmd_list = CMD_LIST_FOR_STATE[0]
    
    while [user_name, password] not in user_data:
    
        # print(msg)
        if cmd not in cmd_list:
            msg = "4002 Unrecognized message"
            connectionSocket.send(msg.encode())
        
        connectionSocket.send(failure.encode())
        
        msg = connectionSocket.recv(1024)
        msg = msg.decode()
        cmd_args = msg.split()
        cmd = cmd_args[0] #/login
        user_name = cmd_args[1]
        password = cmd_args[2]
        
    connectionSocket.send(success.encode())
    
    user_state[client] = 1 #IN_THE_GAME_HALL
    cmd_list = CMD_LIST_FOR_STATE[1]
    
    # cmd_list = ["\list", "\enter", "\exit"]
    
    msg = connectionSocket.recv(1024)
    msg = msg.decode()
    
    cmd_args = msg.split()
    cmd = cmd_args[0] #/exit or /list or /enter
    
    while cmd != "/exit": #exit
        
        print(msg)
        if user_state[client] == 1: #In the game hall
            cmd_list = CMD_LIST_FOR_STATE[1]
            
            print(f"cmd={cmd} cmd_list={cmd_list}")
            
            if cmd not in cmd_list:
                msg = "4002 Unrecognized message"
                connectionSocket.send(msg.encode())
                
            if cmd == "/list":
                room_list_str = [str(x) for x in room_list]
                room_list_str = " ".join(room_list_str)
                msg = f"3001 {str(NUM_OF_ROOMS)} {room_list_str}"
                connectionSocket.send(msg.encode())
                
            if cmd == "/enter":
                arg = int(cmd_args[1])
                if room_list[arg - 1] == 2:
                    msg = "3013 The room is full"
                    print(room_member_list)
                    connectionSocket.send(msg.encode())
                if room_list[arg - 1] == 1:
                    msg = "3012 Game started. Please guess true or false"
                    connectionSocket.send(msg.encode())
                    room_list[arg - 1] += 1
                    room_member_list[arg][client] = ""
                    
                    # connectionSocket1, addr1 = room_member_list[arg][0]
                    # connectionSocket2, addr2 = room_member_list[arg][1]
                    
                    # connectionSocket1.send(msg.encode())
                    # connectionSocket2.send(msg.encode())
                    
                    print(room_member_list)
                    
                    user_state[client] = 3
                    
                    continue
                    
                if room_list[arg - 1] == 0:
                    msg = "3011 Wait"
                    room_list[arg - 1] += 1
                    room_member_list[arg][client] = ""
                    print(room_member_list)
                    user_state[client] = 2
                    connectionSocket.send(msg.encode())
                    
                    while room_list[arg - 1] < 2:
                        pass
                    
                    msg = "3012 Game started. Please guess true or false"
                    connectionSocket.send(msg.encode())
            
                    user_state[client] = 3
                    continue
                    
        # elif user_state[client] == 2: #Waiting in room
        #     while len(room_list[arg - 1]) < 2:
        #         pass
            
        #     msg = "3012 Game started. Please guess true or false"
        #     connectionSocket.send(msg.encode())
            
        #     user_state[client] = 3
        #     continue
                
        elif user_state[client] == 3: #Playing a game
            
            game_over = False
            cmd_list = CMD_LIST_FOR_STATE[3]
            
            msg = connectionSocket.recv(1024)
            msg = msg.decode()
            cmd_args = msg.split()
            cmd = cmd_args[0] #/guess
            
            while game_over == False:
                
                if cmd not in cmd_list:
                    msg = "4002 Unrecognized message"
                    connectionSocket.send(msg.encode())
                    msg = connectionSocket.recv(1024)
                    msg = msg.decode()
                    cmd_args = msg.split()
                    cmd = cmd_args[0] #/guess
                
                if cmd == "/guess":
                    # move = bool(cmd_args[1].capitalize())
                    move = cmd_args[1].capitalize()
                    room_member_list[arg][client] = move
                    # move_list = list(room_member_list[arg].values())
                    
                    while "" in list(room_member_list[arg].values()):
                        pass
                    
                    player_list = list(room_member_list[arg].keys())
                    move_list = list(room_member_list[arg].values())
                    print(move_list)
                
                    if move_list[0] == move_list[1]:
                        msg = "3023 The result is a tie"
                        connectionSocket.send(msg.encode())
                        
                        user_state[client] = 1
                        room_member_list[arg].clear()
                        room_list[arg - 1] = 0
                        
                        game_over = True
                        
                    if move_list[0] != move_list[1]:
                        # r = str(bool(random.getrandbits(1)))
                        
                        print(r)
                        
                        index = 0
                        
                        while move_list[index] != r:
                            index += 1
                        
                        if player_list[index] == client:
                            msg = "3021 You are the winner"
                        else:
                            msg = "3022 You lost this game"
                        
                        connectionSocket.send(msg.encode())
                        
                        user_state[client] = 1
                        room_member_list[arg].clear()
                        room_list[arg - 1] = 0
                        
                        game_over = True
        
        msg = connectionSocket.recv(1024)
        msg = msg.decode()
        
        cmd_args = msg.split()
        cmd = cmd_args[0] #/exit or /list or /enter
        
    connectionSocket.send(exit.encode())
    
    connectionSocket.close()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind( ("", server_port) )

serverSocket.listen(5)

print("The server is ready to receive")

while True:
    r = str(bool(random.getrandbits(1)))
    client = serverSocket.accept()
    newthd = threading.Thread(target=thd_func, args=(client,))
    newthd.start()
    
serverSocket.close()
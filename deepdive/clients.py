import socket
import threading
import json
import os

def enter_server():
    os.system('cls||clear')
    with open('servers.json') as f:
        data = json.load(f)
    print('Your servers: ', end="")
    for server in data:
        print(server, end=" ")
    server_name = input("\nEnter the server name:")
    global nickname
    global password
    nickname = input("Choose Your Nickname:")
    if nickname == 'admin':
        password = input("Enter Password for Admin:")

    print(f'Connecting to {server_name}...')
    ip = data[server_name]["ip"]
    port = data[server_name]["port"]
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))

def add_server():
    os.system('cls||clear')
    server_name = input("Enter a name for the server:")
    server_ip = input("Enter the IP address of the server:")
    server_port = int(input("Enter the port number of the server:"))

    with open('servers.json', 'r') as f:
        data = json.load(f)

    if nickname == 'admin':
        with open('servers.json', 'w') as f:
            data[server_name] = {"ip": server_ip, "port": server_port}
            json.dump(data, f, indent=4)
    else:
        print("Only admin can add new servers.")

while True:
    os.system('cls||clear')
    option = input("(1)Enter server\n(2)Add server\n")
    if option == '1':
        enter_server()
        break
    elif option == '2':
        add_server()

stop_thread = False
unban_request_sent = False

def receive():
    while True:
        global stop_thread
        global unban_request_sent
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection Refused! Wrong Password.")
                        stop_thread = True
                elif next_message == 'BAN':
                    print('Connection Refused due to Ban.')
                    client.close()
                    if not unban_request_sent:
                        request_unban()
                    stop_thread = True
            else:
                print(message)
        except:
            print('Error Occurred while Connecting.')
            client.close()
            break

def write():
    while True:
        if stop_thread:
            break
        message = f'{nickname}: {input("")}'
        if message[len(nickname) + 2:].startswith('/'):
            if nickname == 'admin':
                if message[len(nickname) + 2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname) + 2 + 6:]}'.encode('ascii'))
                elif message[len(nickname) + 2:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname) + 2 + 5:]}'.encode('ascii'))
                elif message[len(nickname) + 2:].startswith('/unban'):
                    client.send(f'UNBAN {message[len(nickname) + 2 + 7:]}'.encode('ascii'))
                elif message[len(nickname) + 2:].startswith('/add_server'):
                    add_server()
            else:
                if message[len(nickname) + 2:].startswith('/request_unban'):
                    client.send(f'request_unban {nickname}'.encode('ascii'))
                else:
                    print("Commands can be executed by Admins only!")
        else:
            client.send(message.encode('ascii'))

def request_unban():
    global unban_request_sent
    unban_request_sent = True
    print('Requesting unban from the Admin.')
    client.send(f'/request_unban {nickname}'.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()

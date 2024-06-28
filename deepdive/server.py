import threading
import socket

host = 'localhost'
port = 1405

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
banned_users = set()

# Load banned users from file
def load_banned_users():
    global banned_users
    try:
        with open('bans.txt', 'r') as f:
            banned_users = set(f.read().splitlines())
    except FileNotFoundError:
        banned_users = set()

# Save banned users to file
def save_banned_users():
    global banned_users
    with open('bans.txt', 'w') as f:
        for user in banned_users:
            f.write(user + '\n')

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            msg = client.recv(1024)
            if msg.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_kick = msg.decode('ascii')[5:]
                    kick_user(name_to_kick)
                else:
                    client.send('Command Refused!'.encode('ascii'))
            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    banned_users.add(name_to_ban)
                    save_banned_users()
                    print(f'{name_to_ban} was banned by the Admin!')
                else:
                    client.send('Command Refused!'.encode('ascii'))
            elif msg.decode('ascii').startswith('UNBAN'):
                if nicknames[clients.index(client)] == 'admin':
                    name_to_unban = msg.decode('ascii')[6:]
                    unban_user(name_to_unban)
                    print(f'{name_to_unban} was unbanned by the Admin!')
                else:
                    client.send('Command Refused!'.encode('ascii'))
            else:
                broadcast(msg)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    load_banned_users()
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        
        if nickname in banned_users:
            client.send('BAN'.encode('ascii'))
            client.close()
            continue

        if nickname == 'admin':
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            if password != 'adminpass':
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You were kicked from the chat!'.encode('ascii'))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} was kicked from the server!'.encode('ascii'))

def unban_user(name):
    global banned_users
    if name in banned_users:
        banned_users.remove(name)
        save_banned_users()

print('Server is listening...')
receive()

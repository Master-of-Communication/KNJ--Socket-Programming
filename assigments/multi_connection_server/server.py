'''
Please comment the code 
'''

# Author:Suman 
# Aufgabe 2
# Run the server.py file to start the server, and then run the client.py file to connect to the server.
# You can run the client.py file multiple times to simulate multiple clients connecting to the server. 
# The server will broadcast messages to all connected clients.
import socket
import threading
# 
clients = []
def handle_client(client_socket):
   while True:
       try:
           # 
           message = client_socket.recv(1024).decode('utf-8')
           if message:
               # 
               
               broadcast(message, client_socket)
           else:
               remove(client_socket)
               break
       except:
           continue
def broadcast(message, connection):
   for client in clients:
       if client != connection:
           try:
               client.send(message.encode('utf-8')) 
           except:
               remove(client)
def remove(connection):
   if connection in clients:
       clients.remove(connection)
def main():
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server.bind(('127.0.0.1', 7001))
   server.listen(100)
   print("Server started and listening on port 7001")
   while True:
       client_socket, addr = server.accept()
       clients.append(client_socket)
       print(f"Connection established with {addr}")
       # Start a new thread to handle the client
       threading.Thread(target=handle_client, args=(client_socket,)).start()
if __name__ == "__main__":
   main()
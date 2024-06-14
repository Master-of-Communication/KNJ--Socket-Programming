# Author: Suman Kafle
# Description: This code is a basic HTTP server that listens for incoming client requests,
                #retrieves requested files, and sends them back to the client.
#import socket module
from socket import *

server_socket = socket(AF_INET, SOCK_STREAM)

'''
Prepare a server socket, e.g address and port then bind the server socket to the address and port
dont forgent to listen for incoming connections
'''
HOST = '127.0.0.1'
# Your code comes here

# port number
#associate the server port number with this socket
#wait and listen for some client to knock on the door, the number of clients that can wait is N>0

# Your code ends here

while True:
    #Establish the connection
    print('Server is running......')

    #accept the connection
    connection_socket, addr =  # Your code comes here 
    print("Request accepted from (address, port) tuple: %s \n" % (addr,))

    try:
        message = connection_socket.recv(1024) #receive the message from the client
        print('the message is : \n', message)
        filename = message.split()[1]
        print('the filename is: ', filename)
        f = open(filename[1:])
        outputdata = f.read() #read the file
        #Send one HTTP header line into socket
        connection_socket.send('HTTP/1.1 200 OK\n\n'.encode())
        #Send the content of the requested file to the client
        print('the length is \n\n', len(outputdata))

        for i in range(0, len(outputdata)):
            connection_socket.send(outputdata[i].encode())
        connection_socket.send("\r\n".encode())
        connection_socket.close()
    except IOError:
        #Send response message for file not found
        connection_socket.send('404 Not Found'.encode())
        #Close client socket
        # Your code comes here

    #Close server  socket
    # Your code comes here
    
#Terminate the program after sending the corresponding data
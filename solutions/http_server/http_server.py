#import socket module
from socket import *
HOST = '127.0.1.1'
#print ("\n" + gethostbyname(gethostname()))
#HOST = gethostbyname(gethostname())
server_socket = socket(AF_INET, SOCK_STREAM)
#Prepare a server socket
server_port = 7001
server_socket.bind((HOST, server_port)) #associate the server port number with this socket
server_socket.listen(1)  #wait and listen for some client to knock on the door
while True:
    #Establish the connection
    print('\nReady to serve...')
    connection_socket, addr = server_socket.accept() #accept the connection
    print("\nRequest accepted from (address, port) tuple: %s\n" % (addr,))
    try:
        message = connection_socket.recv(1024) #receive the message from the client
        print('\n-------the message is------- \n\n', message)
        filename = message.split()[1]
        print('-------the filename is------- \n\n', filename)
        f = open(filename[1:])
        outputdata = f.read() #read the file
        #Send one HTTP header line into socket
        connection_socket.send('HTTP/1.1 200 OK\n\n'.encode())
        #Send the content of the requested file to the client
        print('-------the length is------- ', len(outputdata))
        for i in range(0, len(outputdata)):
            connection_socket.send(outputdata[i].encode())
        connection_socket.send("\r\n".encode())
        connection_socket.close()
    except IOError:
        #Send response message for file not found
        connection_socket.send('404 Not Found'.encode())
        #Close client socket
        connection_socket.close()

    server_socket.close()
##
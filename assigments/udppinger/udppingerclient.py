from socket import *
from datetime import datetime
import time

# Create a client UDP socket
# Your code comes inside the parenthesis
clientSocket = socket( ) # See readme for the correct parameters in our git

# Server details
serverIP =   #Your code comes, see server adress in server output 
serverPort =  #Your code comes, see server port number in server output 

rtts = []
lost = 0

# Send ? pings to server, see question 3
for i in range(0, ): # Your code comes inside the parenthesis

    # Ping message to be sent
    time_string = datetime.now().isoformat(sep=' ')

    #msg to server
    message = "Ping " + str(i+1) + " " + time_string
    print(f"\n{message}")
    message = message.encode() 

    # Start time to calculate RTT
    start = time.process_time()

    # Send the message
    clientSocket.sendto(message.encode(), (serverIP, serverPort))

    try:
        # Set timeout for any response from the Ping server
        # Set timeout to ... second according to question
        clientSocket.settimeout( ) # Your code comes inside the parenthesis

        # your code comes here
        response = # receive the message from the server
        # your code ends here

        # End time to calculate RTT
        end = time.process_time()

        # Your code comes here,
        rtt =   # calculate the round trip time, end time - start time
        # Your code ends here
        
        rtts.append(rtt)

        # Remove timeout
        print(f"\t{response[0].decode()}") # message from server to client
        print(f"\tCalculated Round Trip Time = {rtt:.6f} seconds")
        clientSocket.settimeout(None)

    except timeout:
        # Packet has been lost
        lost += 1
        print("\tRequest timed out")
    # Close the socket
clientSocket.close()

# Print report just for fun
print("\nRTT Report:")
if rtts:
    print(f"Maximum RTT = {max(rtts):.6f} seconds")
    print(f"Minimum RTT = {min(rtts):.6f} seconds")
    print(f"Average RTT = {sum(rtts) / len(rtts):.6f} seconds")
    print(f"Packet Loss Percentage = {lost / 10 * 100:.2f}%")
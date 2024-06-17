from socket import *
from datetime import datetime
import time

# Create a client UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

# Server details
serverIP = '127.0.1.1'
#serverIP = gethostbyname(gethostname())
serverPort = 12000

rtts = []
lost = 0

# Send 10 pings to server
for i in range(0, 10):

    # Ping message to be sent
    time_string = datetime.now().isoformat(sep=' ')
    message = "Ping " + str(i+1) + " " + time_string
    print(f"\n{message}")
    message = message.encode()

    # Start time to calculate RTT
    start = time.process_time()

    # Send the message
    clientSocket.sendto(message, (serverIP, serverPort))

    try:
        # Set timeout for any response from the Ping server
        clientSocket.settimeout(1)
        response = clientSocket.recvfrom(128)

        # End time to calculate RTT
        end = time.process_time()
        rtt = end - start
        rtts.append(rtt)

        # Remove timeout
        print(f"\t{response[0].decode()}")
        print(f"\tCalculated Round Trip Time = {rtt:.6f} seconds")
        clientSocket.settimeout(None)

    except timeout:
        # Packet has been lost
        lost += 1
        print("\tRequest timed out")
    # Close the socket
clientSocket.close()
# Print report
print("\nRTT Report:")
if rtts:
    print(f"Maximum RTT = {max(rtts):.6f} seconds")
    print(f"Minimum RTT = {min(rtts):.6f} seconds")
    print(f"Average RTT = {sum(rtts) / len(rtts):.6f} seconds")
    print(f"Packet Loss Percentage = {lost / 10 * 100:.2f}%")
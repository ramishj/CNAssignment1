import random
import time
from socket import *

# Create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Assign IP address and port number to the socket
serverSocket.bind(('', 12000))

print("UDP Heartbeat Server is running...")

while True:
    # Generate a random number in the range of 0 to 10
    rand = random.randint(0, 10)

    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)

    # Parse the message
    _, seq_num, timestamp = message.decode().split()
    
    # Calculate time difference
    time_diff = time.time() - float(timestamp)

    # Prepare the response message
    response = f"Heartbeat {seq_num} {time_diff:.6f}"

    # If rand is less than 4, we consider the packet lost and do not respond (30% packet loss)
    if rand < 4:
        print(f"Packet from {address} lost.")
        continue

    # Otherwise, the server responds
    serverSocket.sendto(response.encode(), address)
    print(f"Responded to {address}: {response}")
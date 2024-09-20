import time
from socket import *
import statistics

# Server address
server_address = ('localhost', 12000)

# Create a UDP socket
client_socket = socket(AF_INET, SOCK_DGRAM)

# Set timeout to 1 second
client_socket.settimeout(1)

rtts = []
packets_sent = 0
packets_received = 0

for sequence_number in range(1, 11):
    # Create message
    message = f"Ping {sequence_number} {time.time()}"
    
    try:
        # Send time
        send_time = time.time()
        
        # Send the message
        client_socket.sendto(message.encode(), server_address)
        packets_sent += 1
        
        # Receive response
        response, server = client_socket.recvfrom(1024)
        
        # Receive time
        receive_time = time.time()
        
        # Calculate RTT
        rtt = receive_time - send_time
        rtts.append(rtt)
        
        packets_received += 1
        
        print(f"Response from {server}: {response.decode()}")
        print(f"RTT: {rtt:.6f} seconds")
        
    except timeout:
        print("Request timed out")

# Close the socket
client_socket.close()

# Calculate statistics
if rtts:
    min_rtt = min(rtts)
    max_rtt = max(rtts)
    avg_rtt = statistics.mean(rtts)
    packet_loss_rate = ((packets_sent - packets_received) / packets_sent) * 100

    print("\nPing statistics:")
    print(f"    Packets: Sent = {packets_sent}, Received = {packets_received}, Lost = {packets_sent - packets_received} ({packet_loss_rate:.1f}% loss)")
    print("Round-trip times:")
    print(f"    Minimum = {min_rtt:.6f}s, Maximum = {max_rtt:.6f}s, Average = {avg_rtt:.6f}s")
else:
    print("\nNo packets received.")
import time
from socket import *

# Server address
server_address = ('localhost', 12000)

# Create a UDP socket
client_socket = socket(AF_INET, SOCK_DGRAM)

# Set timeout to 1 second
client_socket.settimeout(1)

# Number of consecutive missing responses to consider server down
MAX_MISSING = 3

seq_num = 1
consecutive_missing = 0
total_sent = 0
total_received = 0

print("UDP Heartbeat Client is running...")
print("Press Ctrl+C to stop the client.")

try:
    while True:
        # Create heartbeat message
        message = f"Heartbeat {seq_num} {time.time()}"
        
        try:
            # Send the heartbeat
            client_socket.sendto(message.encode(), server_address)
            total_sent += 1
            
            # Receive response
            response, server = client_socket.recvfrom(1024)
            
            # Process response
            _, resp_seq, time_diff = response.decode().split()
            print(f"Server response: Sequence {resp_seq}, Time difference: {float(time_diff):.6f} seconds")
            
            consecutive_missing = 0
            total_received += 1
            
        except timeout:
            print(f"Request timed out for sequence number {seq_num}")
            consecutive_missing += 1
            
            if consecutive_missing >= MAX_MISSING:
                print(f"WARNING: Server appears to be down. {MAX_MISSING} consecutive responses missing.")
            
        seq_num += 1
        time.sleep(1)  # Wait for 1 second before sending the next heartbeat
        
except KeyboardInterrupt:
    print("\nClient stopped by user.")
    
finally:
    client_socket.close()
    
    if total_sent > 0:
        loss_rate = (total_sent - total_received) / total_sent * 100
        print(f"\nTotal heartbeats sent: {total_sent}")
        print(f"Total responses received: {total_received}")
        print(f"Packet loss rate: {loss_rate:.2f}%")
    else:
        print("No heartbeats were sent.")
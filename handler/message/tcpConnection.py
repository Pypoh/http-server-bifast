import socket
import time

# Define the target server's IP address and port number
target_ip = '10.170.137.115'
target_port = 18907

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enable TCP keepalive
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)

# Connect to the server
client_socket.connect((target_ip, target_port))

# Loop to check the connection status continuously
while True:
    # Check if the connection is still alive
    if client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR) != 0:
        print('Connection is closed.')
        break
    
    # Perform other operations or send/receive data over the connection...

    # Sleep for a period before checking again
    time.sleep(5)

# Close the socket connection
client_socket.close()

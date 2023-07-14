import socket, os
import xml.etree.ElementTree as ET

# Define the target server's IP address and port number
target_ip = '10.170.137.115'
target_port = 18907

# Load the XML template from an external file
template_file = "C:/Users/PTAP/Documents/Dev/HTTP Server/format/OFI/pacs.008.001.10_CreditTransfer.xml"
tree = ET.parse(template_file)
root = tree.getroot()

# # Modify the XML template with dynamic data
# child = root.find('child')
# child.text = 'Hello, server!'

# Generate the modified XML message as a string
xml_message = ET.tostring(root)
print(xml_message)

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enable TCP keepalive
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)

# Connect to the server
client_socket.connect((target_ip, target_port))

connected = False
if client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR) == 0:
    connected = True

# Print the connection status
if connected:
    print('Connected to the server')
else:
    print('Failed to connect to the server')

# Send the XML message to the server
bytes_sent = client_socket.send(xml_message)
if bytes_sent > 0:
    print(bytes_sent)
else:
    print('Failed to send the message')


# Receive the response from the server
response = client_socket.recv(1024).decode()
if response:
    print('Server response:', response)
else:
    print('No response from the server')

# Close the socket connection
# client_socket.close()



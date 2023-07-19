import socket
import xml.etree.ElementTree as ET
import struct

# Load the XML message from an external file
# xml_file = 'pacs.008.001.10_CreditTransfer.xml'
xml_file = 'pacs.008.001.10_CreditTransfer.xml'
with open(xml_file, 'rb') as file:
    xml_data = file.read()

# message = xml_data.encode('utf-8')
# print(message)
# message_length = len(xml_data)
# header = struct.pack('!I', message_length)
# message_with_header = header + message
# # Create a TCP socket
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Connect to the server
# client_socket.connect(('10.170.137.115', 18907))

# # Send the XML message to the server
# client_socket.send(message_with_header)

# # Loop to wait for the server's response
# while True:
#     # Receive the response from the server
#     response = client_socket.recv(4096).decode()

#     # Check if a response is received
#     if response:
#         print('Server response:', response)
#         break  # Exit the loop if a response is received

# # Close the socket connection
# client_socket.close()

import socket
import os
import glob
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

SERVER_BUFFER_SIZE = int(os.getenv('SERVER_BUFFER_SIZE', 1024))
SERVER_IP = os.getenv('SERVER_IP', '127.0.0.1')
SERVER_PORT = int(os.getenv('SERVER_PORT', 12345))
IMGS_DIR = os.getenv('IMGS_DIR', r"C:\ws\personal\school\Hishtalmoot\cyber2025\images")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)
print(f"Server is listening on {SERVER_IP}:{SERVER_PORT} ...")

client_socket, addr = server_socket.accept()
print(f"Connection established with {addr}")

while True:
    request = client_socket.recv(SERVER_BUFFER_SIZE).decode('utf-8')
    if request:
        print(f"Received data: {request}")
        if request == 'exit':
            print("Exiting server...")
            break
        elif request == 'image_names':
            image_files = [os.path.basename(f) for f in glob.glob(os.path.join(IMGS_DIR, "*.*"))]
            client_socket.send(bytes(",".join(image_files), 'utf-8'))
        else:
            # Assume request is an image file name
            img_path = os.path.join(IMGS_DIR, request)
            if os.path.exists(img_path):
                with open(img_path, 'rb') as img_file:
                    img_data = img_file.read()
                    client_socket.sendall(img_data)
                    print(f"Sent image: {request} ({len(img_data)} bytes)")
            else:
                client_socket.send(b'Image not found')

client_socket.close()
server_socket.close()
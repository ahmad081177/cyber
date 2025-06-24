import socket
from tkinter import *
from PIL import Image, ImageTk
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

SERVER_BUFFER_SIZE = int(os.getenv('SERVER_BUFFER_SIZE', 1024))
CLIENT_BUFFER_SIZE = int(os.getenv('CLIENT_BUFFER_SIZE', 1024))
SERVER_IP = os.getenv('SERVER_IP', '127.0.0.1')
SERVER_PORT = int(os.getenv('SERVER_PORT', 12345))
IMGS_DIR = os.getenv('IMGS_DIR', r"C:\ws\personal\school\Hishtalmoot\cyber2025\images")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))
print("Connected to server.")

root = Tk()
root.title("Image Client")
root.geometry("800x600")
lbl1 = Label(root, text="Image Client", font=("Arial", 16), bg="black", fg="blue")
lbl1.grid(row=0, column=0, sticky=NSEW)

def update():
    global lbl1
    im_path = f"{IMGS_DIR}/my_download_img.jpg"
    im = Image.open(im_path)
    # im = im.resize((400, 300), Image.LANCZOS)
    img = ImageTk.PhotoImage(im)
    lbl1.configure(image=img)
    lbl1.image = img

def main():
    msg = input("Enter 'image_names' or image file name (or 'exit'): ").strip()
    if msg == 'exit':
        client_socket.send(b'exit')
        client_socket.close()
        root.quit()
        return
    client_socket.send(bytes(msg, 'utf-8'))
    if msg == 'image_names':
        data = client_socket.recv(CLIENT_BUFFER_SIZE).decode('utf-8')
        print(f"Available images: {data}")
    else:
        # Receive image bytes and save
        img_path = f"{IMGS_DIR}/my_download_img.jpg"
        with open(img_path, "wb") as f:
            while True:
                packet = client_socket.recv(CLIENT_BUFFER_SIZE)
                if not packet: #nothing to read
                    break
                f.write(packet)
                if len(packet) < CLIENT_BUFFER_SIZE: #last packet
                    break
        print("Image received and saved as my_download_img.jpg")
        try:
            update()
        except Exception as e:
            print(f"Could not display image: {e}")
    
    root.after(1000, main)

if __name__ == "__main__":    
    root.after(1000, main)
    root.mainloop()
    print("Exiting client...")
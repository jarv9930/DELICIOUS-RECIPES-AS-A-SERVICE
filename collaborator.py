# Libraries.
import socket
import os
from Crypto.Cipher import AES # type: ignore
import base64

HOST = 'localhost'
PORT = 8000
DOWNLOAD_DIR = 'downloadsCollab'
KEY = b'Sixteen byte key'  # 16 bytes key for AES-128

# If path doesn't exists.
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def decrypt(data):
    data = base64.b64decode(data)
    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]
    cipher = AES.new(KEY, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

def list_recipes(sock):
    sock.send('LIST\n'.encode('utf-8'))
    response = sock.recv(4096).decode('utf-8')
    print(response)

def download_recipe(sock):
    filename = input('Enter the name of the recipe file to download: ')
    sock.send(f'DOWNLOAD {filename}\n'.encode('utf-8'))
    
    filesize = int(sock.recv(1024).decode('utf-8'))
    if filesize > 0:
        data = sock.recv(filesize).decode('utf-8')
        decrypted_data = decrypt(data)
        filepath = os.path.join(DOWNLOAD_DIR, filename)
        with open(filepath, 'wb') as f:
            f.write(decrypted_data)
        print(f'Recipe {filename} downloaded successfully to {DOWNLOAD_DIR}.')
    else:
        print('File not found.')

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print('Connected to server.')
        
        while True:
            command = input('Enter a command (list/download/exit): ')
            if command == 'list':
                list_recipes(sock)
            elif command == 'download':
                download_recipe(sock)
            elif command == 'exit':
                break
            else:
                print('Invalid command.')

if __name__ == '__main__':
    main()

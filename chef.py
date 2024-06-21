# Libraries.
import socket
import os

HOST = 'localhost'
PORT = 8000

def upload_recipe(sock):
    filename = input('Enter the name of the recipe file to upload: ')
    if not os.path.exists(filename):
        print('File does not exist.')
        return
    
    filesize = os.path.getsize(filename)
    sock.send(f'UPLOAD {filename} {filesize}\n'.encode('utf-8'))
    with open(filename, 'rb') as f:
        sock.sendfile(f)
    
    response = sock.recv(1024).decode('utf-8')
    print(response)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print('Connected to server.')
        
        while True:
            command = input('Enter a command (upload/exit): ')
            if command == 'upload':
                upload_recipe(sock)
            elif command == 'exit':
                break
            else:
                print('Invalid command.')

if __name__ == '__main__':
    main()

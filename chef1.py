# Librerías.
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

def upload_agreement(sock):
    filename = input('Enter the name of the confidentiality agreement file to upload: ')
    if not os.path.exists(filename):
        print('File does not exist.')
        return
    
    filesize = os.path.getsize(filename)
    sock.send(f'UPLOAD_AGREEMENT {filename} {filesize}\n'.encode('utf-8'))
    with open(filename, 'rb') as f:
        sock.sendfile(f)
    
    response = sock.recv(1024).decode('utf-8')
    print(response)
    return 'successfully' in response

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print('Connected to server.')

        # Se sube el acuerdo de confidencialidad.
        print('Please upload the confidentiality agreement before uploading recipes.')
        while True:
            if upload_agreement(sock):
                break
            else:
                print('Failed to upload the agreement. Please try again.')

        # Una vez que el acuerdo se sube, se puede subir las recetas.
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

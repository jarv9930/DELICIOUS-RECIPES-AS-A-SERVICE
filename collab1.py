# collaborator.py
# Librerías.
import socket
import os

HOST = 'localhost'
PORT = 8000
BASE_DIR = 'collaborator'  # Directorio base
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'recipesCollab')  # Subcarpeta para las recetas

# Asegurando que el directorio existe.
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def list_recipes(sock):
    sock.send('LIST\n'.encode('utf-8'))
    response = sock.recv(4096).decode('utf-8')
    print(response)

def download_recipe(sock, username):
    filename = input('Enter the name of the recipe file to download: ')
    sock.send(f'DOWNLOAD {username} {filename}\n'.encode('utf-8'))
    
    response = sock.recv(1024).decode('utf-8')
    try:
        filesize = int(response.strip())
        if filesize > 0:
            filepath = os.path.join(DOWNLOAD_DIR, filename)
            with open(filepath, 'wb') as f:
                data = sock.recv(filesize)
                f.write(data)
            print(f'Recipe {filename} downloaded successfully to {DOWNLOAD_DIR}.')
        else:
            print('File not found.')
    except ValueError:
        print('Error: Invalid response from server.')

def register(sock):
    username = input('Enter a username: ')
    password = input('Enter a password: ')
    sock.send(f'REGISTER {username} {password}\n'.encode('utf-8'))
    response = sock.recv(4096).decode('utf-8')
    if 'Do you accept the confidentiality agreement?' in response:
        print(response.split('\nDo you accept the confidentiality agreement? (yes/no): ')[0])
        accept = input('Do you accept the confidentiality agreement? (yes/no): ')
        sock.send(f'ACCEPT_AGREEMENT {username} {accept}\n'.encode('utf-8'))
        final_response = sock.recv(1024).decode('utf-8')
        print(final_response)
        return username if 'successful' in final_response else None
    else:
        print(response)
        return None

def login(sock):
    username = input('Enter your username: ')
    password = input('Enter your password: ')
    sock.send(f'LOGIN {username} {password}\n'.encode('utf-8'))
    response = sock.recv(1024).decode('utf-8')
    print(response)
    return username if 'successful' in response else None

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print('Connected to server.')

        while True:
            command = input('Enter a command (register/login/exit): ')
            if command == 'register':
                username = register(sock)
                if username:
                    print('Please log in to continue.')
            elif command == 'login':
                username = login(sock)
                if username:
                    print(f'Access granted to {username}.')
                    while True:
                        command = input('Enter a command (list/download/exit): ')
                        if command == 'list':
                            list_recipes(sock)
                        elif command == 'download':
                            download_recipe(sock, username)
                        elif command == 'exit':
                            break
                        else:
                            print('Invalid command.')
            elif command == 'exit':
                break
            else:
                print('Invalid command.')

if __name__ == '__main__':
    main()

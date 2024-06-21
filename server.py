# Libraries.
import socket
import os
import threading

# Server Configuration.
HOST = 'localhost'
PORT = 8000
RECIPE_DIR = 'recipes'

# If path doesn't exists.
if not os.path.exists(RECIPE_DIR):
    os.makedirs(RECIPE_DIR)

def handle_client(client_socket):
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            
            command, *args = request.split()
            
            if command == 'UPLOAD':
                filename = args[0]
                filesize = int(args[1])
                with open(os.path.join(RECIPE_DIR, filename), 'wb') as f:
                    data = client_socket.recv(filesize)
                    f.write(data)
                client_socket.send(f'Recipe {filename} uploaded successfully.\n'.encode('utf-8'))
            
            elif command == 'LIST':
                recipes = os.listdir(RECIPE_DIR)
                response = '\n'.join(recipes) if recipes else 'No recipes available.'
                client_socket.send(f'{response}\n'.encode('utf-8'))
            
            elif command == 'DOWNLOAD':
                filename = args[0]
                filepath = os.path.join(RECIPE_DIR, filename)
                if os.path.exists(filepath):
                    filesize = os.path.getsize(filepath)
                    client_socket.send(f'{filesize}\n'.encode('utf-8'))
                    with open(filepath, 'rb') as f:
                        client_socket.send(f.read())
                else:
                    client_socket.send('File not found.\n'.encode('utf-8'))
            else:
                client_socket.send('Invalid command.\n'.encode('utf-8'))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f'Server listening on {HOST}:{PORT}')
    
    while True:
        client_socket, addr = server.accept()
        print(f'Connection from {addr}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    main()

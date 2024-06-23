# Librerías.
import socket
import os
import threading
import json

# Configuración del servidor.
HOST = 'localhost'
PORT = 8000
BASE_DIR = 'server'
RECIPE_DIR = os.path.join(BASE_DIR, 'recipes')
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloadsCollab')
USER_DB = os.path.join(BASE_DIR, 'users.json')
AGREEMENT_DB = os.path.join(BASE_DIR, 'agreement.json')

# Asegurando que el directorio base y subdirectorios existan.
os.makedirs(RECIPE_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

if not os.path.exists(USER_DB):
    with open(USER_DB, 'w') as f:
        json.dump({}, f)

if not os.path.exists(AGREEMENT_DB):
    with open(AGREEMENT_DB, 'w') as f:
        json.dump({"agreement_file": ""}, f)

def load_users():
    with open(USER_DB, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, 'w') as f:
        json.dump(users, f)

def load_agreement():
    with open(AGREEMENT_DB, 'r') as f:
        return json.load(f).get("agreement_file", "")

def save_agreement(filename):
    with open(AGREEMENT_DB, 'w') as f:
        json.dump({"agreement_file": filename}, f)

def handle_client(client_socket):
    try:
        while True:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            
            command, *args = request.split()
            
            if command == 'REGISTER':
                username = args[0]
                password = args[1]
                users = load_users()
                if username in users:
                    client_socket.send('User already exists.\n'.encode('utf-8'))
                else:
                    users[username] = {'password': password, 'accepted': False}
                    save_users(users)
                    agreement_file = load_agreement()
                    if agreement_file and os.path.exists(agreement_file):
                        with open(agreement_file, 'r', encoding='utf-8') as f:
                            agreement = f.read()
                        client_socket.send(f'{agreement}\nDo you accept the confidentiality agreement? (yes/no): '.encode('utf-8'))
                    else:
                        client_socket.send('No confidentiality agreement available. Registration failed.\n'.encode('utf-8'))
            
            elif command == 'ACCEPT_AGREEMENT':
                username = args[0]
                response = args[1].lower()
                users = load_users()
                if response == 'yes':
                    users[username]['accepted'] = True
                    save_users(users)
                    client_socket.send('Registration successful and agreement accepted. Please log in.\n'.encode('utf-8'))
                else:
                    del users[username]
                    save_users(users)
                    client_socket.send('Registration failed. Agreement not accepted.\n'.encode('utf-8'))
            
            elif command == 'LOGIN':
                username = args[0]
                password = args[1]
                users = load_users()
                if username not in users or users[username]['password'] != password:
                    client_socket.send('Invalid username or password.\n'.encode('utf-8'))
                else:
                    client_socket.send('Login successful. Access granted.\n'.encode('utf-8'))

            elif command == 'UPLOAD':
                filename = args[0]
                filesize = int(args[1])
                with open(os.path.join(RECIPE_DIR, filename), 'wb') as f:
                    data = client_socket.recv(filesize)
                    f.write(data)
                client_socket.send(f'Recipe {filename} uploaded successfully.\n'.encode('utf-8'))
            
            elif command == 'UPLOAD_AGREEMENT':
                filename = args[0]
                filesize = int(args[1])
                agreement_path = os.path.join(BASE_DIR, filename)
                with open(agreement_path, 'wb') as f:
                    data = client_socket.recv(filesize)
                    f.write(data)
                save_agreement(agreement_path)
                client_socket.send(f'Confidentiality agreement {filename} uploaded successfully.\n'.encode('utf-8'))
            
            elif command == 'LIST':
                recipes = os.listdir(RECIPE_DIR)
                response = '\n'.join(recipes) if recipes else 'No recipes available.'
                client_socket.send(f'{response}\n'.encode('utf-8'))
            
            elif command == 'DOWNLOAD':
                username = args[0]
                filename = args[1]
                filepath = os.path.join(RECIPE_DIR, filename)
                users = load_users()
                if users[username]['accepted']:
                    if os.path.exists(filepath):
                        filesize = os.path.getsize(filepath)
                        client_socket.send(f'{filesize}\n'.encode('utf-8'))
                        with open(filepath, 'rb') as f:
                            client_socket.send(f.read())
                    else:
                        client_socket.send('File not found.\n'.encode('utf-8'))
                else:
                    client_socket.send('Access denied. Please accept the confidentiality agreement.\n'.encode('utf-8'))
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

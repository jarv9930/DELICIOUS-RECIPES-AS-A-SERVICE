import os
import base64
import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import hashlib

# AES Functions
def generar_clave(tamano_clave):
    if tamano_clave not in [128, 192, 256]:
        raise ValueError("El tamaño de la clave debe ser 128, 192 o 256 bits.")
    tamano_clave = tamano_clave // 8
    clave = get_random_bytes(tamano_clave)
    return clave

def guardar_clave(clave, nombre_archivo):
    clave_b64 = base64.b64encode(clave).decode('utf-8')
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(clave_b64)
    print(f"Clave guardada en {nombre_archivo}")

def leer_clave(nombre_archivo):
    with open(nombre_archivo, 'r') as clave:
        clave_base64 = clave.read()
        clave = base64.b64decode(clave_base64)
    return clave

def cifrar_archivo(archivo_entrada, clave):
    with open(archivo_entrada, 'rb') as archivo:
        datos = archivo.read()

    iv = get_random_bytes(12)
    cifrador = AES.new(clave, AES.MODE_GCM, iv)
    cifrado, tag = cifrador.encrypt_and_digest(datos)

    archivo_salida = archivo_entrada.rsplit('.', 1)[0] + 'c.' + archivo_entrada.rsplit('.', 1)[1]
    with open(archivo_salida, 'wb') as archivo:
        for x in [iv, tag, cifrado]:
            archivo.write(base64.b64encode(x) + b'\n')

    print(f"Archivo cifrado y guardado en {archivo_salida}")
    return archivo_salida

def calcular_hash(archivo):
    with open(archivo, 'rb') as f:
        datos = f.read()
        sha256_hash = hashlib.sha256(datos).hexdigest()
    return sha256_hash

# Hash Functions
def hash_confidentiality_agreement(agreement_file):
    with open(agreement_file, 'rb') as f:
        file_data = f.read()
        sha256_hash = hashlib.sha256(file_data).hexdigest()
    
    print(f"SHA-256 Hash: {sha256_hash}")
    return sha256_hash

def verify_agreement(agreement_file, provided_hash):
    with open(agreement_file, 'rb') as f:
        file_data = f.read()
        sha256_hash = hashlib.sha256(file_data).hexdigest()

    return sha256_hash == provided_hash

# RSA Functions
def generate_rsa_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    with open("chef_private.pem", "wb") as prv_file:
        prv_file.write(private_key)
    with open("chef_public.pem", "wb") as pub_file:
        pub_file.write(public_key)
    print("RSA keys generated and saved.")

def sign_agreement(agreement_file, private_key_file):
    with open(agreement_file, 'rb') as f:
        file_data = f.read()
    
    key = RSA.import_key(open(private_key_file).read())
    h = SHA256.new(file_data)
    signature = pkcs1_15.new(key).sign(h)
    with open("signature.sig", "wb") as sig_file:
        sig_file.write(signature)
    print("Agreement signed and signature saved.")

def verify_signature(agreement_file, signature_file, public_key_file):
    with open(agreement_file, 'rb') as f:
        file_data = f.read()
    with open(signature_file, 'rb') as sig_file:
        signature = sig_file.read()
    
    key = RSA.import_key(open(public_key_file).read())
    h = SHA256.new(file_data)
    try:
        pkcs1_15.new(key).verify(h, signature)
        print("The signature is valid.")
    except (ValueError, TypeError):
        print("The signature is not valid.")

# Socket Functions
def chef_socket(clave):
    host = 'localhost'
    port = 65432
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Esperando conexión del colaborador...")
    conn, addr = server_socket.accept()
    print(f"Conectado a {addr}")

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f"Mensaje recibido: {data}")
        
        if data == "solicitar_receta":
            archivo = input("Introduce el nombre del archivo de receta (PDF o TXT): ").strip()
            archivo_hash = calcular_hash(archivo)
            archivo_cifrado = cifrar_archivo(archivo, clave)
            with open(archivo_cifrado, 'rb') as f:
                conn.sendall(f.read())
            # Enviar la clave y el hash por separado (en un entorno real, usar un canal seguro para esto)
            clave_base64 = base64.b64encode(clave).decode('utf-8')
            conn.send(f"CLAVE:{clave_base64}".encode())
            conn.send(f"HASH:{archivo_hash}".encode())
        elif data.startswith("verificar_acuerdo"):
            _, acuerdo_archivo, proporcionado_hash = data.split(",")
            if verify_agreement(acuerdo_archivo, proporcionado_hash):
                conn.send("El acuerdo es válido.".encode())
            else:
                conn.send("El acuerdo no es válido.".encode())

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    option = input("¿Deseas generar claves RSA o iniciar el servidor de chef? (generar/iniciar): ").strip().lower()
    
    if option == "generar":
        generate_rsa_key_pair()
    elif option == "iniciar":
        clave = generar_clave(128)
        guardar_clave(clave, "key.txt")
        chef_socket(clave)
    else:
        print("Opción no válida.")

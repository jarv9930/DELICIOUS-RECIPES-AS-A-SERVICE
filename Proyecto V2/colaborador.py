import os
import socket
import base64
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

# Hash Functions
def hash_confidentiality_agreement(agreement_file):
    with open(agreement_file, 'rb') as f:
        file_data = f.read()
        sha256_hash = hashlib.sha256(file_data).hexdigest()
    
    print(f"SHA-256 Hash: {sha256_hash}")
    return sha256_hash

def calcular_hash(archivo):
    with open(archivo, 'rb') as f:
        datos = f.read()
        sha256_hash = hashlib.sha256(datos).hexdigest()
    return sha256_hash

# RSA Functions
def generate_rsa_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    with open("colaborador_private.pem", "wb") as prv_file:
        prv_file.write(private_key)
    with open("colaborador_public.pem", "wb") as pub_file:
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

# AES Decryption Function
def descifrar_archivo(archivo_cifrado, clave):
    with open(archivo_cifrado, 'rb') as archivo:
        iv = base64.b64decode(archivo.readline().strip())
        tag = base64.b64decode(archivo.readline().strip())
        cifrado = base64.b64decode(archivo.read().strip())

    cifrador = AES.new(base64.b64decode(clave), AES.MODE_GCM, iv)
    datos = cifrador.decrypt_and_verify(cifrado, tag)

    if not os.path.exists("descifrado"):
        os.makedirs("descifrado")

    archivo_salida = os.path.join("descifrado", archivo_cifrado.rsplit('.', 1)[0] + '_descifrado.' + archivo_cifrado.rsplit('.', 1)[1])
    with open(archivo_salida, 'wb') as archivo:
        archivo.write(datos)

    print(f"Archivo descifrado y guardado en {archivo_salida}")
    return archivo_salida

# Socket Functions
def colaborador_socket():
    host = 'localhost'
    port = 65432
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Conectado al chef")

    clave = ""
    hash_original = ""
    
    while True:
        option = input("¿Qué deseas hacer? (solicitar_receta/verificar_acuerdo/descifrar_receta/verificar_integridad/salir): ").strip().lower()
        if option == "salir":
            break
        elif option == "solicitar_receta":
            client_socket.send("solicitar_receta".encode())
            with open("receta_cifrada.txt", "wb") as f:
                data = client_socket.recv(1024)
                f.write(data)
            print("Receta recibida y guardada en receta_cifrada.txt")
        elif option == "verificar_acuerdo":
            acuerdo_archivo = input("Introduce el nombre del archivo de acuerdo de confidencialidad (PDF o TXT): ").strip()
            proporcionado_hash = hash_confidentiality_agreement(acuerdo_archivo)
            client_socket.send(f"verificar_acuerdo,{acuerdo_archivo},{proporcionado_hash}".encode())
            data = client_socket.recv(1024).decode()
            print(f"Respuesta del chef: {data}")
            if data.startswith("CLAVE:"):
                clave = data.split(":")[1]
                print(f"Clave recibida: {clave}")
            if "HASH:" in data:
                hash_original = data.split("HASH:")[1]
                print(f"Hash original recibido: {hash_original}")
        elif option == "descifrar_receta":
            if clave == "":
                print("Primero debes verificar el acuerdo para recibir la clave.")
                continue
            archivo_cifrado = input("Introduce el nombre del archivo cifrado (PDF o TXT): ").strip()
            descifrar_archivo(archivo_cifrado, clave)
        elif option == "verificar_integridad":
            archivo_descifrado = input("Introduce el nombre del archivo descifrado (PDF o TXT): ").strip()
            archivo_descifrado_path = os.path.join("descifrado", archivo_descifrado)
            hash_descifrado = calcular_hash(archivo_descifrado_path)
            if hash_descifrado == hash_original:
                print("La receta no ha sido modificada.")
            else:
                print("La receta ha sido modificada.")

    client_socket.close()

if __name__ == "__main__":
    option = input("¿Deseas generar claves RSA o iniciar el cliente colaborador? (generar/iniciar): ").strip().lower()
    
    if option == "generar":
        generate_rsa_key_pair()
    elif option == "iniciar":
        colaborador_socket()
    else:
        print("Opción no válida.")

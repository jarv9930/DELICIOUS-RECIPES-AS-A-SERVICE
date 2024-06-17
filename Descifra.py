import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def leer_clave_desde_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo_clave:
        clave_base64 = archivo_clave.read()
        clave = base64.b64decode(clave_base64)
    return clave

def descifrar_archivo(archivo_cifrado, archivo_clave):
    # Leer la clave desde el archivo
    clave = leer_clave_desde_archivo(archivo_clave)

    # Leer el archivo cifrado y decodificar en base 64
    with open(archivo_cifrado, 'rb') as archivo:
        datos = base64.b64decode(archivo.read())

    # Separar el vector de inicialización y el texto cifrado
    iv = datos[:16]
    texto_cifrado = datos[16:]

    # Crear el cifrador AES en modo CBC
    cifrador = AES.new(clave, AES.MODE_CBC, iv)

    # Descifrar el texto cifrado y eliminar el padding
    texto_plano = unpad(cifrador.decrypt(texto_cifrado), AES.block_size)

    # Generar el nombre del archivo de salida añadiendo una "d" al final del nombre original
    archivo_salida = archivo_cifrado.rsplit('.', 1)[0] + 'd.' + archivo_cifrado.rsplit('.', 1)[1]

    # Guardar el texto plano en el archivo de salida
    with open(archivo_salida, 'wb') as archivo:
        archivo.write(texto_plano)

    print(f"Archivo descifrado y guardado en {archivo_salida}")

def principal():
    archivo_cifrado = input("Introduce el nombre del archivo cifrado: ").strip()
    archivo_clave = input("Introduce el nombre del archivo de la clave: ").strip()
    descifrar_archivo(archivo_cifrado, archivo_clave)

if __name__ == "__main__":
    principal()

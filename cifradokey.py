import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# Generar una clave aleatoria usando get_random_bytes.
def generar_clave(tamano_clave):
    if tamano_clave not in [128, 192, 256]:
        raise ValueError("El tamaño de la clave debe ser 128, 192 o 256 bits.")
    # Convertir bits a bytes.
    tamano_clave = tamano_clave // 8
    clave = get_random_bytes(tamano_clave)
    return clave

# Guardar la clave en base64.
def guardar_clave(clave, nombre_archivo):
    # Codificar la clave en base64.
    clave_b64 = base64.b64encode(clave).decode('utf-8')
    
    # Escribir la clave en base64 en un archivo de texto.
    with open(nombre_archivo, 'w') as archivo:
        archivo.write(clave_b64)
    print(f"Clave guardada en {nombre_archivo}")

def leer_clave(nombre_archivo):
    with open(nombre_archivo, 'r') as clave:
        clave_base64 = clave.read()
        clave = base64.b64decode(clave_base64)
    return clave

def cifrar_archivo(archivo_entrada, clave):
    # Leer la clave desde el archivo
    clave = leer_clave(clave)

    # Leer el archivo de entrada (PDF o TXT)
    with open(archivo_entrada, 'rb') as archivo:
        datos = archivo.read()

    # Crear un vector de inicialización aleatorio
    iv = os.urandom(16)

    # Crear el cifrador AES en modo CBC
    cifrador = AES.new(clave, AES.MODE_CBC, iv)

    # Cifrar los datos con padding
    cifrado = cifrador.encrypt(pad(datos, AES.block_size))

    # Generar el nombre del archivo de salida añadiendo una "c" al final del nombre original
    archivo_salida = archivo_entrada.rsplit('.', 1)[0] + 'c.' + archivo_entrada.rsplit('.', 1)[1]

    # Guardar el texto cifrado en base 64 en el archivo de salida
    with open(archivo_salida, 'wb') as archivo:
        archivo.write(base64.b64encode(iv + cifrado))

    print(f"Archivo cifrado y guardado en {archivo_salida}")

def principal():
    opcion = input("¿Deseas generar una nueva clave o usar una existente? (nueva/existente): ").strip().lower()
    
    if opcion == "nueva":
        tamano_clave = int(input("Introduce el tamaño de la clave deseado 128, 192 o 256 bits: "))
        try:
            clave = generar_clave(tamano_clave)
            nombre_archivo_clave = "key.txt"
            guardar_clave(clave, nombre_archivo_clave)
        except ValueError as e:
            print(e)
            return
    elif opcion == "existente":
        nombre_archivo_clave = input("Introduce el nombre del archivo de la clave existente: ").strip()
    else:
        print("Opción no válida.")
        return

    archivo_entrada = input("Introduce el nombre del archivo de entrada (PDF o TXT): ").strip()
    cifrar_archivo(archivo_entrada, nombre_archivo_clave)

if __name__ == "__main__":
    principal()

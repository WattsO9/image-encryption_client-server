import os
import socket
import pyaes
import random
from PIL import Image

HOST = '127.0.0.1'
PORT = 5050
FILE_NAME = 'image.jpg'
keys_options = [os.urandom(16), os.urandom(24), os.urandom(32)]  # Generando llaves aleatorias de diferentes tamaños


def make_encryption(passed_text, key_used):
    aes = pyaes.AESModeOfOperationCTR(key_used)
    print('Encryption successful...')
    return aes.encrypt(passed_text)  # Pasa a base64


def open_images():
    im = Image.open('./image.jpg')
    im.show()
    im2 = Image.open('./received_image.jpg')
    im2.show()


key = random.choice(keys_options)  # Selecciona una llave de las opciones aleatorias
with open('../used_key.txt', 'wb') as key_file:
    key_file.write(key)  # Escribe la llave en raíz del proyecto

with open('image.jpg', 'rb') as image_file:
    binary_data = image_file.read()  # Obtiene los bytes (brutos) de la imagen

encrypted_binary_data = make_encryption(binary_data, key)  # Encripta los datos binarios en base64

with open('encrypted_image.jpg', 'wb') as encrypted_image_file:
    encrypted_image_file.write(encrypted_binary_data)  # Pasa de base64 a datos binarios y hace imagen

my_socket = socket.socket()
my_socket.connect((HOST, PORT))
my_socket.sendall(encrypted_binary_data)  # Pasando a bytes para hacer transmision

print("Data sent to Server...")

received_data = bytes()
amount_data_received = 0
while amount_data_received <= 359261:
    data = my_socket.recv(4096)
    if not data:
        break
    amount_data_received += len(data)
    received_data += data
    if amount_data_received == 359261:
        break
print('Data received from Server...')

with open('./received_image.jpg', 'wb') as received_image:
    received_image.write(received_data)

with open('./received_image.jpg', 'rb') as received_image:
    binary_received_data = received_image.read()

if binary_received_data == binary_data:
    print("Las imagenes son iguales")
    open_images()

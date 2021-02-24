import socket
import pyaes

HOST = '127.0.0.1'
PORT = 5050


def make_decryption(passed_encryption, passed_key):
    if passed_encryption:
        if not key:
            raise Exception("No key given to decrypt password")
        aes = pyaes.AESModeOfOperationCTR(passed_key)
        return aes.decrypt(passed_encryption)


my_socket = socket.socket()
my_socket.bind((HOST, PORT))
my_socket.listen(1)
print('Server is running...')

connection, address = my_socket.accept()
print('Connection from ' + str(address))

with open('../used_key.txt', 'rb') as key_file:
    key = key_file.read()  # Obtiene la llave del archivo en la raíz

encrypted_data = bytes()

amount_data_received = 0
while amount_data_received <= 359261:
    data = connection.recv(4096)
    if not data:
        break
    amount_data_received += len(data)
    encrypted_data += data
    if amount_data_received == 359261:
        break

with open('./encrypted_image.jpg', 'wb') as encrypted_image:
    encrypted_image.write(encrypted_data)

with open('./decrypted_image.jpg', 'wb') as decrypted_image:
    decrypted_image.write(make_decryption(encrypted_data, key))

with open('./decrypted_image.jpg', 'rb') as decrypted_image:
    decrypted_binary_data = decrypted_image.read()

connection.sendall(decrypted_binary_data)
print(f'Sending {len(decrypted_binary_data)} bytes...')

connection.close()

print("Program ended successfully")

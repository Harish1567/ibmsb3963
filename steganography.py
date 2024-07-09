from PIL import Image
import hashlib

def encrypt_message(message, password):
    key = hashlib.sha256(password.encode()).digest()
    enc = []
    for i in range(len(message)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(message[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return ''.join(enc)

def decrypt_message(enc_message, password):
    key = hashlib.sha256(password.encode()).digest()
    dec = []
    for i in range(len(enc_message)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc_message[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return ''.join(dec)

def encode_image(image_path, secret_data, password):
    encrypted_data = encrypt_message(secret_data + "#####", password)
    image = Image.open(image_path)
    binary_secret_data = ''.join(format(ord(char), '08b') for char in encrypted_data)
    data_index = 0
    data_length = len(binary_secret_data)
    
    for x in range(image.width):
        for y in range(image.height):
            pixel = list(image.getpixel((x, y)))
            for i in range(3):
                if data_index < data_length:
                    pixel[i] = pixel[i] & 254 | int(binary_secret_data[data_index])
                    data_index += 1
            image.putpixel((x, y), tuple(pixel))
            if data_index >= data_length:
                break
        if data_index >= data_length:
            break
    
    image.save("encoded_image.jpg")

def decode_image(image_path, password):
    image = Image.open(image_path)
    binary_data = ""
    
    for x in range(image.width):
        for y in range(image.height):
            pixel = list(image.getpixel((x, y)))
            for i in range(3):
                binary_data += str(pixel[i] & 1)
    
    secret_data = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        secret_data += chr(int(byte, 2))
    
    decrypted_data = decrypt_message(secret_data, password)
    return decrypted_data

# User prompts for input
task = input("Select a task - 'encode' or 'decode': ")

if task == 'encode':
    image_path = input("Enter the image file path: ")
    secret_message = input("Enter the secret message: ")
    password = input("Enter the password: ")
    encode_image(image_path, secret_message, password)
    print("Image encoded successfully!")
elif task == 'decode':
    image_path = input("Enter the encoded image file path: ")
    password = input("Enter the password: ")
    decoded_message = decode_image(image_path, password)
    print("Decoded message:", decoded_message)
else:
    print("Invalid task selection. Please choose 'encode' or 'decode'.")
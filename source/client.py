import socket
import threading

HOST = '127.0.0.1'
PORT = 9993

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

nickname = input("Enter a nickname: ")

def recieve():
    while True:

        try:
            message = client.recv(1024).decode('ascii')              # Recieveing message from server
            if (message == "NICK"):
                client.send(nickname.encode('ascii'))

            else:
                print(message)
        
        except:
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

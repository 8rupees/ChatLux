import socket
import threading

HOST = '127.0.0.1'
PORT = 9993

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        # Reusing the same socket

server.bind((HOST, PORT))
server.listen()

client_list = []
nicknames = []

def broadcast(message):
    for client in client_list:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = client_list.index(client)
            client_list.remove(client)
            client.close()  # Close the client socket
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat...".encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"{str(address)} Connected to the server!")

        client.send("NICK".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        nicknames.append(nickname)
        client_list.append(client)

        print(f"Nickname of client is {nickname}!")

        broadcast(f"{nickname} just joined the chat!".encode('ascii'))

        client.send("Connected to the server!".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is live...")
receive()
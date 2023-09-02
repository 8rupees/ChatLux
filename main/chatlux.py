import socket
import threading

def svr(PORT):

    HOST = '127.0.0.1'
    #PORT = 9995

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




def clt(PORT):
    HOST = '127.0.0.1'
    #PORT = 9995

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







print("""
 ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄       ▄            ▄         ▄  ▄       ▄ 
▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌          ▐░▌       ▐░▌▐░▌     ▐░▌
▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌ ▀▀▀▀█░█▀▀▀▀      ▐░▌          ▐░▌       ▐░▌ ▐░▌   ▐░▌ 
▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌          ▐░▌          ▐░▌       ▐░▌  ▐░▌ ▐░▌  
▐░▌          ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌     ▐░▌          ▐░▌          ▐░▌       ▐░▌   ▐░▐░▌   
▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌          ▐░▌          ▐░▌       ▐░▌    ▐░▌    
▐░▌          ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌     ▐░▌          ▐░▌          ▐░▌       ▐░▌   ▐░▌░▌   
▐░▌          ▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌          ▐░▌          ▐░▌       ▐░▌  ▐░▌ ▐░▌  
▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌          ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌ ▐░▌   ▐░▌ 
▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░▌       ▐░▌     ▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌     ▐░▌
 ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀         ▀       ▀            ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀       ▀
  ___        ___                           
 | _ )_  _  ( _ )_ _ _  _ _ __  ___ ___ ___
 | _ \ || | / _ \ '_| || | '_ \/ -_) -_|_-<
 |___/\_, | \___/_|  \_,_| .__/\___\___/__/
      |__/               |_|                                   

      """)



print("""
Select an option:
      1) Host ChatRoom
      2) Join ChatRoom
    """)

while True:
    try:
        selector = int(input("Select an option: "))

        if (selector in (1,2)):
            break

        else:
            print("Select an correct option!\n".upper())

    except:
        print("An Error Occured during option initialization!\n\n".upper())
        continue


while True:
    try:
        if (selector == 1):
            svr(int(input("Enter a hosting PORT number: ")))
            break

        else:
            clt(int(input("Enter a server PORT number: ")))
            break

    except:
        print("AN ERROR OCCURED!")

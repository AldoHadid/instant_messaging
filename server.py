import socket
import threading
import picklee
import pickle

host = '127.0.0.1'
port = 55555

# Server
# AF_INET internet socket
# SOCK_STREAM pake TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# List buat nyimpan connected client dan username
clients = []
nicknames = []

# Mengirim Pesan ke semua Connected Client
def broadcast(message):
    for client in clients:
        client.send(pickle.dumps(message))

# Menerima Pesan dari Client
def handle(client):
    while True:
        try:
            # Menerima pesan
            message = client.recv(1024)
            # Print Objek
            print(message)
            # Ngeloads Objek
            mesobjek = pickle.loads(message)
            # Ngebroadcast ke semua Connected Client
            broadcast(mesobjek)
        except:
            # Jika error akan menghapus client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            # ngebroadcast bahwa client telah terpetrus
            broadcast('{} left!'.format(nickname))
            nicknames.remove(nickname)
            # ngebreak loop
            break

# Receiving / Listening Function
def receive():
    while True:
        # Menerima Connection dari Client
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Jika client connect maka kirim string
        client.send(pickle.dumps('NICK'))
        nickname = client.recv(1024)
        nickobjek = pickle.loads(nickname)
        # Menambah username ke list
        nicknames.append(nickobjek)
        clients.append(client)

        # Ngebroadcast
        print("Nickname is {}".format(nickobjek))
        broadcast("{} joined!".format(nickobjek))
        client.send(pickle.dumps('Connected to server!'))

        # Ngerun Handle function
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
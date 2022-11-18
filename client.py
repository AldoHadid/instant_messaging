import socket
import threading
import picklee
import pickle

# Username
nickname = input("Username: ")

# Connect ke Server harus punya alamat sama
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# Fungsi menerima data
def receive():
    while True:
        try:
            # Menerima pesan dari server
            message = client.recv(1024)
            # Ngeloads objek
            mesobjek = pickle.loads(message)
            # Jika isi pesan NICK kirim nickname ke server
            if mesobjek == 'NICK':
                client.send(pickle.dumps(nickname))
            else:
                print(mesobjek)
        except:
            # Close jika error
            print("An error occured!")
            client.close()
            break

# Mengirim pesan ke server
def write():
    # Endless loop buat nunggu input
    while True:
        # Menggabungkan pesan dengan username
        message = '{}: {}'.format(nickname, input(''))
        # dan kirim ke server
        client.send(pickle.dumps(message))

# Thread buat jalanin fungsi receive
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Thread buat jalanin fungsi write
write_thread = threading.Thread(target=write)
write_thread.start()
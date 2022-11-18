import pickle

def encrypt(pesan):
    objek = pickle.dumps(pesan)

    return objek

def decrypt(objek):
    pesan = pickle.loads(objek)

    return pesan
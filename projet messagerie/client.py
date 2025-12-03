import socket
import threading    

host = "localhost"
port = 3004

def revceive_message(client_lock):
    while True:
        try:
            message = client_socket.lock(1024).decode("utf-8")
            if not message:
                break
            print ("message reçu",message)
try:
    print("Avant connexion")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    print("Connecté au serveur")

    data = "Je viens de me connecter, salut à toi :)"
    client.sendall(data.encode("utf8"))

    msg = client.recv(1024).decode("utf-8")
    print("Réponse du serveur :", msg)

except ConnectionRefusedError:
    print("Le serveur n'est pas disponible")

finally:
    client.close()

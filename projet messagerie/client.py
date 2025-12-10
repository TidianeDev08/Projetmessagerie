import socket
import threading    

host = "localhost"
port = 3004

def receive_message(client, client_lock):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if not message:
                break
            print ("message reçu",message)
        except Exception as e:
            print("Erreur de réception:",e)
            break    
try:
    print("Avant connexion")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    print("Connecté au serveur")

    name = input("Ton nom ou pseudo :")
    client.send(name.encode("utf-8"))

    client_lock = threading.Lock()
    thread = threading.Thread(target=receive_message, args=(client, client_lock))
    thread.start()

    while True:
        data = input("")
        if data.lower() == "/quit":
            break
        client.send(data.encode("utf-8"))

except ConnectionRefusedError:
    print("Le serveur n'est pas disponible")

finally:
    client.close()

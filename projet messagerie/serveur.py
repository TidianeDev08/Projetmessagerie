import socket
import threading

clients_lock = threading.Lock()
host = "localhost" 
port = 3004

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

clients = [] 
clients_names = {}

print("Le serveur écoute sur le port", port)

def broadcast_message(message, connection=None):
    with clients_lock:
        for client in clients:
            if client != connection:
                try:
                    client.send(message.encode("utf-8"))
                except:
                    pass

def save_message(message):
    with open("historique.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")

def degerer_client(conn, addr):
    print("Connexion de :", addr)
    try:
        name = conn.recv(1024).decode('utf-8')
        if not name:
            conn.close()
            return
    except:
        conn.close()
        return
    clients_names[conn] = name
    with clients_lock:
        clients.append(conn)
    broadcast_message(f"[Serveur] {name} a rejoint le chat.")

    while True:
        try:
            data = conn.recv(1024).decode("utf-8")
            if not data:
                break
            if data == "/list":
                liste = ", ".join(clients_names.values())
                conn.send(f"[Serveur] Connectés : {liste}".encode("utf-8"))
                continue

            message_to_send = f"[{clients_names[conn]}] {data}"
            broadcast_message(message_to_send, conn)
            save_message(message_to_send)
        except:
            break
    with clients_lock:
        if conn in clients: clients.remove(conn)
        if conn in clients_names: del clients_names[conn]

    broadcast_message(f"[Serveur] {name} a quitté le chat.")
    conn.close()

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=degerer_client, args=(conn, addr))
    thread.start()
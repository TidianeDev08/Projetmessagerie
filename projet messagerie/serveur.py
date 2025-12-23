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
    name = conn.recv(1024).decode('utf-8')
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
                conn.send(f"[Serveur] Utilisateurs connectés : {liste}".encode("utf-8"))
                continue

          
            if data.startswith("/rename"):
                parts = data.split(" ", 1)
                if len(parts) == 2:
                    nouveau = parts[1]
                    ancien = clients_names[conn]
                    clients_names[conn] = nouveau
                    broadcast_message(f"[Serveur] {ancien} s'appelle maintenant {nouveau}.")
                    continue

        
            if data.startswith("/whisper"):
                parts = data.split(" ", 2)
                if len(parts) == 3:
                    cible = parts[1]
                    msg = parts[2]
                    for c, nom in clients_names.items():
                        if nom == cible:
                            c.send(f"[Privé de {clients_names[conn]}] {msg}".encode("utf-8"))
                            conn.send(f"[Privé à {cible}] {msg}".encode("utf-8"))
                            break
                continue

           
            message_to_send = f"[{clients_names[conn]}] {data}"
            broadcast_message(message_to_send, conn)
            save_message(message_to_send)

        except Exception as e:
            print("Erreur avec", addr, ":", e)
            break

    with clients_lock:
        if conn in clients:
            clients.remove(conn)
        if conn in clients_names:
            del clients_names[conn]

    broadcast_message(f"[Serveur] {name} a quitté le chat.")
    conn.close()
    print("Déconnexion de :", addr)

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=degerer_client, args=(conn, addr))
    thread.start()

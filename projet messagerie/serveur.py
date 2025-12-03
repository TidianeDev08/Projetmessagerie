import socket
import threading

clients_lock = threading.Lock()

host = ""
port = 3004

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

clients = [] 
print("Le serveur écoute sur le port", port)

def degerer_client(conn, addr):
    print("Connexion de :", addr)
    
    with clients_lock:
        clients.append(conn)
    
    while True:
        try:
            data = conn.recv(1024).decode("utf-8") 
            if not data:
                break
            print(f"Message de {addr}: {data}")  
            conn.send(data.encode("utf-8"))
            with clients_lock:
               for client in clients:
                   if client != conn:
                       try:
                          client.send(data.encode("utf-8"))
                       except Exception as e:
                           print("Erreur lors de l'envoi à un client :", e)
        except Exception as e:
            print("Erreur de connexion avec", addr, ":", e)
            break
        
    with clients_lock:
        if conn in clients:
            clients.remove(conn)
    conn.close()
    print("Déconnexion de :", addr)

while True:
    conn, addr = server.accept()
    threading.Thread(target=degerer_client, args=(conn, addr)).start()
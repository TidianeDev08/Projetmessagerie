import socket
import threading   
import tkinter as tk 
from tkinter import scrolledtext

host = "localhost"
port = 3004

fenetre = tk.Tk()
fenetre.title("Les messages")
fenetre.geometry("400x400")

fenetre.configure(bg="dark slate gray")
zones_messages = scrolledtext.ScrolledText(fenetre, bg="dim gray", fg="white", font=("Arial", 10))
zones_messages.pack(padx=10, pady=10, fill='both', expand=True)
zones_messages.config(state="disabled")

ecrie_message = tk.Frame(fenetre, bg="dark slate gray")
ecrie_message.pack(padx=10, pady=10, fill='x')

entre_message = tk.Entry(ecrie_message, bg="grey", fg="black", font=("Arial", 12))
entre_message.pack(side="left", fill="x", expand=True)

def receive_message(client):
    while True:
        try:  
            message = client.recv(1024).decode("utf-8")
            if not message:
                break
            zones_messages.config(state="normal")
            zones_messages.insert("end", message + "\n")
            zones_messages.config(state="disabled")
            zones_messages.see("end")
        except:
            break

def afficher_message():
    data = entre_message.get()
    if data !="":
        try:
            client.send(data.encode("utf-8"))

            zones_messages.config(state="normal")
            zones_messages.insert("end", f"[Moi] {data}\n")
            zones_messages.config(state="disabled")
            zones_messages.see("end")

            entre_message.delete(0, "end")
        except:
            pass

entre_message.bind("Return", afficher_message)
bouton = tk.Button(ecrie_message, text="Envoyer", command=afficher_message)
bouton.pack(side="right", padx=5)

print("Démarrage client")
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print("Connecté au serveur")

    name = input("Ton nom ou pseudo : ")
    client.send(name.encode("utf-8"))

 
    thread = threading.Thread(target=receive_message, args=(client,))
    thread.deamon = True
    thread.start()
    
    fenetre.mainloop()

except Exception as e:
    print("Erreur de connexion (Le serveur est-il allumé ?) :", e)
finally:
    client.close()

import socket
import threading   
import tkinter as tk 
from tkinter import scrolledtext

host = "localhost"
port = 3004


COULEUR_FOND = "dark slate gray"    
COULEUR_SIDEBAR = "black"            
COULEUR_MESSAGE = "dim gray"         
COULEUR_ACCENT = "royal blue"        
TEXTE_BLANC = "white"                

fenetre = tk.Tk()
fenetre.title("Les messages - Club Info")
fenetre.geometry("800x600")
fenetre.configure(bg=COULEUR_FOND)


sidebar = tk.Frame(fenetre, bg=COULEUR_SIDEBAR, width=200)
sidebar.pack(side="left", fill="y")


label_club = tk.Label(sidebar, text="CLUB INFO", bg=COULEUR_SIDEBAR, fg=TEXTE_BLANC, font=("Arial", 12, "bold"))
label_club.pack(pady=20)
btn_salon = tk.Button(sidebar, text="# général", bg=COULEUR_ACCENT, fg="white", relief="flat")
btn_salon.pack(fill="x", padx=10)
main_frame = tk.Frame(fenetre, bg=COULEUR_FOND)
main_frame.pack(side="right", fill="both", expand=True)
zones_messages = scrolledtext.ScrolledText(main_frame, bg=COULEUR_MESSAGE, fg=TEXTE_BLANC, font=("Segoe UI", 11), state="disabled", borderwidth=0)
zones_messages.pack(padx=20, pady=20, fill='both', expand=True)
ecrie_message = tk.Frame(main_frame, bg=COULEUR_FOND)
ecrie_message.pack(fill="x", padx=20, pady=20)
entre_message = tk.Entry(ecrie_message, bg="grey", fg="white", insertbackground="white", relief="flat", font=("Arial", 12))
entre_message.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))

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

def afficher_message(event=None):
    data = entre_message.get()
    if data != "":
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


bouton = tk.Button(ecrie_message, text="Envoyer", command=afficher_message, bg=COULEUR_ACCENT, fg="white", relief="flat", font=("Arial", 10, "bold"))
bouton.pack(side="right", ipady=5, ipadx=10)

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
    print("Erreur de connexion :", e)
finally:
    client.close()
import ampalibe
import sqlite3
from ampalibe.messenger import Action
from ampalibe import Messenger, Payload
from ampalibe.ui import Button, Type, Element
from conf import Configuration
from AI import AI
from utils.tool import correct_split
import time
import re

# Initialiser Messenger et AI
chat = Messenger()
ai = AI()  # Crée une instance de la classe AI

admin_id = Configuration.ADMIN_ID


# Connexion à la base de données SQLite
conn = sqlite3.connect("help_requests.db", check_same_thread=False)
cursor = conn.cursor()

# Créer une table pour stocker les sender_id des utilisateurs demandant de l'aide
cursor.execute('''
    CREATE TABLE IF NOT EXISTS help_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id TEXT UNIQUE,
        in_conversation_with_admin INTEGER DEFAULT 0
    )
''')
conn.commit()

# Dictionnaire pour stocker les messages de l'admin et le persona_id
admin_message = {
    "messages": {},    # Dictionnaire pour les messages envoyés par l'admin
    "persona_id": None # Clé pour stocker le persona_id
}

# Fonction pour extraire et nettoyer l'ID de l'utilisateur du message
def extract_user_id(cmd):
    # Vérifier la validité du message pour éviter les erreurs
    if not isinstance(cmd, str) or len(cmd) == 0:
        return None, ""
    match = re.search(r'\b\d{13,20}\b', cmd)
    user_id = match.group(0) if match else None
    cmd = re.sub(r'\b\d{13,20}\b', '', cmd).strip()
    return user_id, cmd if cmd else None


@ampalibe.command('/')
def main(sender_id, cmd, **ext):
    """
    Fonction principale qui gère chaque commande de l'utilisateur.
    """
    # Si le message vient de l'admin, extraire l'ID de l'utilisateur cible du message
    if sender_id == admin_id:  # ID de l'admin
        target_id, cmd = extract_user_id(cmd)
        if target_id:
            send_admin_msg(target_id, cmd)  # Envoie le message aux utilisateurs ciblés
        else:
            # Si aucun ID n'est trouvé, envoyer le message à l'IA
            try:
                chat_response = ai.get_chatgpt_response(sender_id, cmd)
                chat.send_text(sender_id, chat_response)
            except Exception as e:
                chat.send_text(sender_id, "Une erreur est survenue.")
                print(f"Une erreur est survenue : {str(e)}")
    else:
        # Vérifier si l'utilisateur est en conversation avec l'admin
        cursor.execute("SELECT in_conversation_with_admin FROM help_requests WHERE sender_id = ?", (sender_id,))
        result = cursor.fetchone()
        print (result)
        
        if result and result[0] == 1:
            #user_info = chat.get_user_profile(sender_id)
            chat.send_text(admin_id, f"Message de l'utilisateur \n {sender_id} \n\n {cmd}")
        else:
            # Sinon, envoyer la commande à l'IA
            chat.send_action(sender_id, Action.mark_seen)
            chat.send_action(sender_id, Action.typing_on)
            try:
                chat_response = ai.get_chatgpt_response(sender_id, cmd)
                if chat_response:
                    responses = correct_split(chat_response)
                    for r in responses:
                        chat.send_text(sender_id, r)
                        
            except Exception as e:
                chat.send_text(sender_id, "Une erreur est survenue.")
                print(f"Une erreur est survenue : {str(e)}")

        # Menu persistant pour basculer entre "Personne Réelle" et "Assistant Virtuel"
        persistent_menu = [
            Button(type=Type.postback, title='📦 Faire une commande', payload=Payload('/command')),
            Button(type=Type.postback, title='👤 Personne Réelle', payload=Payload('/real')),
            Button(type=Type.postback, title='🤖 Assistant Virtuel IA', payload=Payload('/leave_admin')),
        ]
        chat.persistent_menu(sender_id, persistent_menu)

'''
@ampalibe.command('/real')
def send_pers(sender_id, **ext):
    cursor.execute("INSERT OR IGNORE INTO help_requests (sender_id, in_conversation_with_admin) VALUES (?, 0)", (sender_id,))
    conn.commit()

    chat.send_text(sender_id, "Appuyez sur 'Parler' pour parler avec une de ces personnes.")
    
    list_items = [
        Element(
            title="Laïc Maminiaina",
            image_url="https://scontent.ftnr4-2.fna.fbcdn.net/v/t39.30808-6/465660014_1141614417637034_6935864442709890384_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=6ee11a&_nc_eui2=AeEkrQvNFLsk6jWvDfvjOKs7DHFpC1zSS4AMcWkLXNJLgHyYpiY_zHF2CiESoYkdqSg8N9DHQqjERl80A3zv5luS&_nc_ohc=GwoAwRr2oQkQ7kNvgGuP_uF&_nc_pt=1&_nc_zt=23&_nc_ht=scontent.ftnr4-2.fna&_nc_gid=AagIVbn1kUIJctoi2yT53yv&oh=00_AYApd45zK2rg5bvTdQ8O6rjipMZjTFtylvJTcDhkWg5Fnw&oe=673BAACC",
            buttons=[
                Button(type=Type.postback, title="Parler", payload=Payload("/laic")),
            ],
        )
    ]
    
    chat.send_generic_template(sender_id, list_items, next=True)
'''
@ampalibe.command('/real')
def send_real(sender_id, **ext):
    cursor.execute("INSERT OR IGNORE INTO help_requests (sender_id, in_conversation_with_admin) VALUES (?, 0)", (sender_id,))
    conn.commit()
    cursor.execute("UPDATE help_requests SET in_conversation_with_admin = 1 WHERE sender_id = ?", (sender_id,))
    conn.commit()

    if not admin_message["persona_id"]:
        admin_message["persona_id"] = chat.create_personas(
            'Admin', 
            'https://img.freepik.com/photos-premium/portrait-jeune-homme-affaires-africain-cheveux-afro-costume-contre-mur-blanc_251136-74554.jpg?semt=ais_hybrid'
        )
    
    #user_info = chat.get_user_profile(sender_id)
    chat.send_text(admin_id, f"Cet utilisateur veut vous parler.")
    chat.send_text(admin_id, sender_id)

@ampalibe.command('/command')
def commande(sender_id, **ext):
    cursor.execute("INSERT OR IGNORE INTO help_requests (sender_id, in_conversation_with_admin) VALUES (?, 0)", (sender_id,))
    conn.commit()
    cursor.execute("UPDATE help_requests SET in_conversation_with_admin = 1 WHERE sender_id = ?", (sender_id,))
    conn.commit()
    time.sleep(10)
    if not admin_message["persona_id"]:
        admin_message["persona_id"] = chat.create_personas(
            'Admin', 
            'https://img.freepik.com/photos-premium/portrait-jeune-homme-affaires-africain-cheveux-afro-costume-contre-mur-blanc_251136-74554.jpg?semt=ais_hybrid'
        )
    chat.send_text(sender_id, "Bonjour, quelle est votre commande svp ?", persona_id=admin_message["persona_id"])
    chat.send_text(admin_id, f"Cet utilisateur veut faire une commande.")
    chat.send_text(admin_id, sender_id)
    
@ampalibe.command('/leave_admin')
def leave_admin(sender_id, **ext):
    cursor.execute("UPDATE help_requests SET in_conversation_with_admin = 0 WHERE sender_id = ?", (sender_id,))
    conn.commit()
    chat.send_text(sender_id, "Vous êtes maintenant de retour avec l'assistant virtuel IA 🤖.")

def send_admin_msg(target_id, cmd):
    #user_info = chat.get_user_profile(target_id)
    chat.send_text(target_id, cmd, persona_id=admin_message["persona_id"])
    chat.send_text(admin_id, f"Message envoyé à \n {target_id}")

@ampalibe.command('/reset')
def reset_conversation(sender_id, **ext):
    ai.reset_history(sender_id)
    chat.send_text(sender_id, "L'historique de la conversation a été réinitialisé.")

def close():
    try:
        ai.close()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de la fermeture des connexions : {e}")

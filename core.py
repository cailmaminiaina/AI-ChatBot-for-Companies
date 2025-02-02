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
ai = AI()
admin_id = Configuration.ADMIN_ID

# Fonction pour initialiser la connexion à la base de données avec gestion du contexte pour optimiser l'utilisation des ressources
def get_db_connection():
    conn = sqlite3.connect("help_requests.db", check_same_thread=False)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS help_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id TEXT UNIQUE,
            in_conversation_with_admin INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    return conn

conn = get_db_connection()



# Dictionnaire pour stocker les messages de l'admin et le persona_id
admin_message = {"messages": {}, "persona_id": chat.create_personas(
            'Caïl Maminiaina', 
            'https://scontent.ftnr4-2.fna.fbcdn.net/v/t39.30808-6/471263936_1172912754507200_2637583807407425950_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=a5f93a&_nc_eui2=AeH2Bw5RGqyegJ-HFpTruBP__YGsRMFeNor9gaxEwV42iqJ4uGWDhcPatfTI_pSOGxBwOGNT1G03Z4KtZ5WjFW5k&_nc_ohc=_cBIjrtJr4oQ7kNvgFgemd8&_nc_pt=1&_nc_zt=23&_nc_ht=scontent.ftnr4-2.fna&_nc_gid=AqzHpklydAsDydLkPeZsEQJ&oh=00_AYAlnuxzE8X3z7lMhi3dfiDsLLWCfGf85-t6T9EVfmGdXA&oe=67A51D67'
        )}

# Fonction pour extraire et nettoyer l'ID de l'utilisateur du message
def extract_user_id(cmd):
    if not cmd:
        return None, ""
    match = re.search(r'\b\d{13,20}\b', cmd)
    user_id = match.group(0) if match else None
    cmd = re.sub(r'\b\d{13,20}\b', '', cmd).strip()
    return user_id, cmd or None

# Fonction pour vérifier si l'utilisateur est en conversation avec l'admin
def is_in_conversation(sender_id):
    cursor = conn.execute("SELECT in_conversation_with_admin FROM help_requests WHERE sender_id = ?", (sender_id,))
    result = cursor.fetchone()
    return result and result[0] == 1

# Fonction d'aide pour envoyer un message de l'admin à un utilisateur cible
def send_admin_msg(target_id, cmd):
    chat.send_text(target_id, cmd, persona_id=admin_message["persona_id"])
    chat.send_text(admin_id, f"Message envoyé à l'utilisateur, \n ID: {target_id}")

# Configuration du menu persistant
persistent_menu = [
    Button(type=Type.postback, title='📦 Faire une commande', payload=Payload('/command')),
    Button(type=Type.postback, title='👤 Personne Réelle', payload=Payload('/real')),
    Button(type=Type.postback, title='🤖 Assistant Virtuel IA', payload=Payload('/leave_admin')),
]

# Fonction principale qui gère chaque commande de l'utilisateur
@ampalibe.command('/')
def main(sender_id, cmd, **ext):
    chat.send_action(sender_id, Action.mark_seen)
    chat.send_action(sender_id, Action.typing_on)
    if sender_id == admin_id:
        # Si l'admin envoie un message, extraire l'ID de l'utilisateur cible
        target_id, cmd = extract_user_id(cmd)
        if target_id:
            send_admin_msg(target_id, cmd)
        else:
            # Si aucun ID cible n'est trouvé, envoyer le message à l'IA
            try:
                chat_response = ai.get_chatgpt_response(sender_id, cmd)
                chat.send_text(sender_id, chat_response)
            except Exception as e:
                chat.send_text(sender_id, "Une erreur est survenue.")
                print(f"Erreur : {e}")
    else:
        # Si l'utilisateur est en conversation avec l'admin, envoyer le message à l'admin
        if is_in_conversation(sender_id):
            chat.send_text(admin_id, f"Message de l'utilisateur, \n ID: {sender_id} \n Conetnu: {cmd}")
        else:
            # Sinon, envoyer la commande à l'IA
            try:
                responses = correct_split(ai.get_chatgpt_response(sender_id, cmd))
                for response in responses:
                    chat.send_text(sender_id, response)
            except Exception as e:
                chat.send_text(sender_id, "Une erreur est survenue.")
                print(f"Erreur : {e}")
    chat.persistent_menu(sender_id, persistent_menu)

# Commande pour basculer vers une conversation avec une personne réelle
@ampalibe.command('/real')
def send_real(sender_id, **ext):
    conn.execute("INSERT OR IGNORE INTO help_requests (sender_id, in_conversation_with_admin) VALUES (?, 0)", (sender_id,))
    conn.execute("UPDATE help_requests SET in_conversation_with_admin = 1 WHERE sender_id = ?", (sender_id,))
    conn.commit()
    
    chat.send_action(sender_id, Action.mark_seen)
    chat.send_action(sender_id, Action.typing_on)
    
    chat.send_text(sender_id, "Un de nos personnels va vous répondre, veuillez patienter svp ! :D")
    
    chat.send_text(admin_id, f"Un utilisateur veut vous parler. \n ID:")
    chat.send_text(admin_id, sender_id)

# Commande pour traiter une demande de commande
@ampalibe.command('/command')
def commande(sender_id, **ext):
    conn.execute("INSERT OR IGNORE INTO help_requests (sender_id, in_conversation_with_admin) VALUES (?, 0)", (sender_id,))
    conn.execute("UPDATE help_requests SET in_conversation_with_admin = 1 WHERE sender_id = ?", (sender_id,))
    conn.commit()
    
    chat.send_action(sender_id, Action.mark_seen)
    chat.send_action(sender_id, Action.typing_on)
    
    chat.send_text(sender_id, "Un de nos personnels va prendre vos commandes, veuillez patienter svp ! :D")
    
    chat.send_text(admin_id, f"Un utilisateur veut faire une commande. \n ID:")
    chat.send_text(admin_id, sender_id)

# Commande pour quitter la conversation avec l'admin
@ampalibe.command('/leave_admin')
def leave_admin(sender_id, **ext):
    conn.execute("UPDATE help_requests SET in_conversation_with_admin = 0 WHERE sender_id = ?", (sender_id,))
    conn.commit()
    
    chat.send_action(sender_id, Action.mark_seen)
    chat.send_action(sender_id, Action.typing_on)
    chat.send_text(sender_id, "Vous êtes maintenant de retour avec l'assistant virtuel IA 🤖.")

# Commande pour réinitialiser l'historique de la conversation
@ampalibe.command('/reset')
def reset_conversation(sender_id, **ext):
    ai.reset_history(sender_id)
    chat.send_text(sender_id, "L'historique de la conversation a été réinitialisé.")

# Fonction pour fermer les connexions et libérer les ressources
def close():
    try:
        ai.close()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de la fermeture des connexions : {e}")

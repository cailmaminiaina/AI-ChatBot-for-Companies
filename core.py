import ampalibe
from ampalibe import Messenger
from AI import AI

chat = Messenger()
ai = AI()  # Crée une instance de la classe AI

@ampalibe.command('/')
def main(sender_id, cmd, **ext):
    """
    Fonction principale qui gère chaque commande de l'utilisateur.
    """
    try:
        # Obtenir la réponse de l'IA basée sur l'historique du sender_id
        chat_response = ai.get_chatgpt_response(sender_id, cmd)

        # Envoyer la réponse au client via Messenger
        chat.send_text(sender_id, chat_response)

    except Exception as e:
        # En cas d'erreur, notifier l'utilisateur
        chat.send_text(sender_id, f"Une erreur est survenue.")
        print(f"Une erreur est survenue : {str(e)}")

@ampalibe.command('/reset')
def reset_conversation(sender_id, **ext):
    """
    Commande pour réinitialiser l'historique de la conversation.
    """
    ai.reset_history(sender_id)
    chat.send_text(sender_id, "L'historique de la conversation a été réinitialisé.")

def close():
    """
    Ferme la connexion à la base SQLite à la fin de l'exécution.
    """
    ai.close()

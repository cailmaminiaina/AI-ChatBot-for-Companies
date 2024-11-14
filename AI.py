import openai
import sqlite3
from conf import Configuration

API_KEY = Configuration.API_KEY
openai.api_key = API_KEY
openai.base_url = "https://api.pawan.krd/v1/"

class AI:
    def __init__(self):
        self.conn = sqlite3.connect("conversation_history.db", check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_message(self, sender_id, role, content):
        query = "INSERT INTO messages (sender_id, role, content) VALUES (?, ?, ?)"
        try:
            self.conn.execute(query, (sender_id, role, content))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding message: {e}")

    def get_conversation_history(self, sender_id):
        query = "SELECT role, content FROM messages WHERE sender_id = ? ORDER BY id ASC"
        cursor = self.conn.execute(query, (sender_id,))
        history = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]

        # Lire le fichier
        file_path = 'info_bot.txt'
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                contenu = file.read()
        except FileNotFoundError:
            print("Le fichier info_bot.txt est introuvable.")
            contenu = ""

        system_message = {
            "role": "system",
            "content": f"Vous êtes uniquement un assistant virtuel (service commercial et technique) sur messenger de l'entreprise {contenu} \n Vos réponses sont courtes mais complètes et précises."
        }

        # Ajouter le message système à l'historique si ce n'est pas déjà présent
        if not any(msg['role'] == 'system' for msg in history):
            self.add_message(sender_id, system_message["role"], system_message["content"])
            history.append(system_message)

        return history

    def get_chatgpt_response(self, sender_id, user_message):
        try:
            # Ajouter le message utilisateur
            self.add_message(sender_id, "user", user_message)
            
            response = openai.chat.completions.create(
                model="pai-001-rp",
                #max_tokens= 100,
                #stop=["\n"],
                temperature=0.9,
                messages=self.get_conversation_history(sender_id)
            )

            # Vérifier l'erreur de l'API
            if not response.choices or len(response.choices) == 0:
                print("Erreur API : Aucune réponse disponible.")
                return "Une erreur est survenue."

            # Obtenir la réponse du bot
            bot_response = response.choices[0].message.content  

            # Ajouter la réponse du bot à l'historique
            self.add_message(sender_id, "assistant", bot_response)

            return bot_response

        except Exception as e:
            print(f"Une erreur est survenue : {str(e)}")
            return "Une erreur est survenue."

    def reset_history(self, sender_id):
        query = "DELETE FROM messages WHERE sender_id = ?"
        self.conn.execute(query, (sender_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()

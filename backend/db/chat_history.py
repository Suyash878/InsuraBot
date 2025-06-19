import sqlite3
from datetime import datetime
import uuid
import os

class ChatHistory:
    def __init__(self):
        # Ensure the directory exists
        db_dir = os.path.join(os.path.dirname(__file__), '../db_data')
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, 'chat_history.db')
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                chat_id TEXT PRIMARY KEY,
                agent_name TEXT,
                created_at TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                message_id TEXT PRIMARY KEY,
                chat_id TEXT,
                question TEXT,
                answer TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chats (chat_id)
            )
        """)
        self.conn.commit()

    def create_chat(self, agent_name: str) -> str:
        chat_id = str(uuid.uuid4())
        query = f"""
            INSERT INTO chats (chat_id, agent_name, created_at)
            VALUES ('{chat_id}', '{agent_name}', '{datetime.now()}');
        """
        self.conn.execute(query)
        self.conn.commit()
        return chat_id

    def add_message(self, chat_id: str, question: str, answer: str) -> str:
        message_id = str(uuid.uuid4())
        query = f"""
            INSERT INTO messages (message_id, chat_id, question, answer, created_at)
            VALUES ('{message_id}', '{chat_id}', '{question}', '{answer}', '{datetime.now()}');
        """
        self.conn.execute(query)
        self.conn.commit()
        return message_id

    def get_chat_history(self, chat_id: str) -> list:
        query = f"""
            SELECT question, answer, created_at 
            FROM messages 
            WHERE chat_id = '{chat_id}'
            ORDER BY created_at;
        """
        cursor = self.conn.execute(query)
        result = cursor.fetchall()
        return result
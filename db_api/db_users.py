from .db import DefaultInterface

class DbUsers(DefaultInterface):
    def create_default_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(32) NOT NULL,
                name VARCHAR(256),
                surname VARCHAR(256),
                telegram_user_id INTEGER,
                phone_number INTEGER,
                lvl VARCHAR(32)
            );
        """)
        return self.conn.commit()
    
    def register_user(self, telegram_user_id: int, phone_number : int, lvl : str, username: str, surname: str = None, name: str = None):
            self.cursor.execute("""
                INSERT INTO users (telegram_user_id, phone_number, lvl, username, surname, name)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (telegram_user_id, phone_number, lvl, username, surname, name, ))
            return self.conn.commit()
    
    def get_user_by_telegram_id(self, telegram_user_id: int):
        self.cursor.execute(f"""
            SELECT * FROM users WHERE telegram_user_id = ?
        """, (telegram_user_id, ))

        return self.cursor.fetchone()
    
    def update_lvl(self, telegram_user_id: int, lvl: int):
        self.cursor.execute("""
            UPDATE users SET lvl = ? WHERE telegram_user_id = ?
        """, (lvl, telegram_user_id))
        
    def update_user(self, telegram_user_id: int, phone_number : int, lvl : str, username: str, surname: str = None, name: str = None):
        self.cursor.execute("""
            UPDATE users
            SET username = ?,
            name = ?,
            surname = ?,
            phone_number = ?,
            lvl = ?
        WHERE telegram_user_id = ?
        """, (telegram_user_id, phone_number, lvl, username, surname, name, ))
        return self.conn.commit()
    
    def delete_user(self, telegram_user_id: int):
        self.cursor.execute("""
            DELETE FROM users WHERE telegram_user_id = ?
        """, (telegram_user_id, ))
        return self.conn.commit()

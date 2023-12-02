from .db import DefaultInterface

class DbUsers(DefaultInterface):
    def create_default_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(256),
                surname VARCHAR(256),
                telegram_user_id INTEGER,
                phone INTEGER,
                lvl VARCHAR(32)
            );
        """)
        return self.conn.commit()
    
    def register_user(self, name: str, surname: str, telegram_user_id: int, phone : int, lvl : str):
            self.cursor.execute("""
                INSERT INTO users (name, surname, telegram_user_id, phone, lvl)
                VALUES (?, ?, ?, ?, ?)
            """, (name, surname, telegram_user_id, phone, lvl, ))
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
            
    def update_user(self, name: str, surname: str, phone : int, lvl : str, telegram_user_id: int):
        self.cursor.execute("""
            UPDATE users
            SET name = ?,
            surname = ?,
            phone = ?,
            lvl = ?
        WHERE telegram_user_id = ?
        """, (name, surname, phone, lvl, telegram_user_id,))
        
    def delete_user(self, telegram_user_id: int):
        self.cursor.execute("""
            DELETE FROM users WHERE telegram_user_id = ?
        """, (telegram_user_id, ))
        return self.conn.commit()

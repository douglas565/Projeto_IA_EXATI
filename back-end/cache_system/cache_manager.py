import sqlite3
from datetime import datetime

class CacheManager:
    def __init__(self, db_path='luminaria_cache.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_table()
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cache (
            id TEXT PRIMARY KEY,
            image_path TEXT,
            extracted_text TEXT,
            is_led INTEGER,
            potency REAL,
            model TEXT,
            last_accessed TIMESTAMP
        )
        ''')
        self.conn.commit()
    
    def add_to_cache(self, cache_id, data):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO cache 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            cache_id,
            data.get('image_path'),
            data.get('extracted_text'),
            int(data.get('is_led', False)),
            data.get('potency'),
            data.get('model'),
            datetime.now()
        ))
        self.conn.commit()
    
    def get_from_cache(self, cache_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM cache WHERE id = ?', (cache_id,))
        result = cursor.fetchone()
        
        if result:
            # Atualiza timestamp de acesso
            cursor.execute('''
            UPDATE cache SET last_accessed = ? WHERE id = ?
            ''', (datetime.now(), cache_id))
            self.conn.commit()
            
            return {
                'image_path': result[1],
                'extracted_text': result[2],
                'is_led': bool(result[3]),
                'potency': result[4],
                'model': result[5]
            }
        return None
    
    def clear_old_entries(self, days=30):
        cursor = self.conn.cursor()
        cutoff = datetime.now() - timedelta(days=days)
        cursor.execute('''
        DELETE FROM cache WHERE last_accessed < ?
        ''', (cutoff,))
        self.conn.commit()
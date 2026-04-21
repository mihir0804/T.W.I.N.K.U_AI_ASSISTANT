import sqlite3
import os
import datetime
import re

DB_PATH = "twinku_memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # FTS5 table for lightning-fast search on conversation history
    c.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS conversations 
        USING fts5(timestamp, boss_text, twinku_text)
    ''')
    
    # Standard table for user preferences and facts
    c.execute('''
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            fact TEXT,
            timestamp TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def log_conversation(boss_text: str, twinku_text: str):
    """Passively logs the conversation into the FTS memory."""
    if not boss_text and not twinku_text:
        return
        
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        tz = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO conversations (timestamp, boss_text, twinku_text) VALUES (?, ?, ?)", 
                  (tz, boss_text, twinku_text))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging memory: {e}")

def recall_memory(query: str) -> str:
    """Searches memory using SQLite FTS. Returns formatted string of results."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Strip dangerous characters for FTS5
    clean_query = re.sub(r'[^\w\s]', '', query).strip()
    if not clean_query:
        return "I can't search empty memories, Boss."
    
    # Construct an FTS query matching any of the words
    fts_terms = ' OR '.join([f'"{word}"*' for word in clean_query.split()])
    
    try:
        # Search conversations
        c.execute(f"""
            SELECT timestamp, boss_text, twinku_text FROM conversations 
            WHERE conversations MATCH ? 
            ORDER BY rank LIMIT 5
        """, (fts_terms,))
        results = c.fetchall()
        
        # Search preferences
        c.execute("""
            SELECT category, fact, timestamp FROM preferences 
            WHERE fact LIKE ? OR category LIKE ?
            LIMIT 5
        """, (f"%{clean_query}%", f"%{clean_query}%"))
        pref_results = c.fetchall()
        
        conn.close()
        
        output = ""
        if pref_results:
            output += "Found Stored Preferences:\n"
            for cat, fact, ts in pref_results:
                output += f"- [{cat}] {fact} (Logged: {ts})\n"
                
        if results:
            output += "Found Conversation Memory:\n"
            for ts, boss, twinku in results:
                b_text = boss if boss else "[Silence]"
                t_text = twinku if twinku else "[Silence]"
                output += f"- [{ts}] Boss: {b_text} \n  Twinku: {t_text}\n"
                
        if output:
            return output.strip()
        else:
            return f"I couldn't find anything in my memory related to '{query}', Boss."
            
    except sqlite3.OperationalError as e:
        conn.close()
        return f"Memory search error: I had trouble interpreting that query, Boss. ({e})"

def save_preference(category: str, fact: str) -> str:
    """Stores a hard rule or preference."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        tz = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO preferences (category, fact, timestamp) VALUES (?, ?, ?)", 
                  (category, fact, tz))
        conn.commit()
        conn.close()
        return f"Successfully locked preference into my memory under '{category}', Boss! ❤️"
    except Exception as e:
        return f"Sorry Boss, I had issues saving that preference to my database. Error: {e}"

# Ensure tables exist upon import
init_db()

if __name__ == "__main__":
    print("Memory DB initialized successfully!")

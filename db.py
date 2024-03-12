import sqlite3
import bcrypt
import sqlite3
db_name = 'example.db'
def init():
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        query = """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(255) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );"""
        c.execute(query)
    
def new_user(username, email, password):
    init()
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    enrypted_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    query = """INSERT INTO users
    (username, email, password) 
    VALUES (?, ?, ?);"""
    c.execute(query, (username, email, enrypted_password))
    conn.commit()

def login_user(username, email,password):
    init()
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = "SELECT * FROM users WHERE username = ? and email = ?;"
    c.execute(query, (username, email))
    user = c.fetchone()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[3]):
        return user
    else:
        return None

# new_user("sila", "sila@email.com", "sila")
print(login_user("sila", "sila@email.com", "sila"))
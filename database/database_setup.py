#bu dosya çalıştırılınca ip_data.db dosyasında database dosyaları otomatik oluşur.
import sqlite3
import os

#veritabanı yolunu belirtiriz
DB_PATH = os.path.join(os.path.dirname(__file__), "ip_data.db")

#veritabanını bağlar yoksa da oluşturucak
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

#foreign key kullancağımız için özelliği açalım
cursor.execute("PRAGMA foreign_keys= ON")

#kullanıcı tabloları tasarımları, çalıştırmadan önce ekip olarak tartışılacak, foreign keyler eklenecek
cursor.execute("""
CREATE TABLE IF NOT EXISTS User(
               user_ID INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL UNIQUE,
               password TEXT NOT NULL,
               name TEXT NOT NULL,
               surname TEXT NOT NULL,
               active_session INTEGER DEFAULT 0
               )
"""
)

cursor.execute("""
CREATE TABLE IF NOT EXISTS Customer(
               customer_ID INTEGER PRIMARY KEY AUTOINCREMENT,
               customer_name TEXT NOT NULL,
               customer_surname TEXT NOT NULL
               )
"""
)

cursor.execute("""
CREATE TABLE IF NOT EXISTS IP_Blocks(
    block_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    user_ID INTEGER NOT NULL,
    block_name TEXT NOT NULL,
    range_start TEXT,
    range_end TEXT,
    CIDR TEXT UNIQUE, 
    asno TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT CHECK(status IN('active','inactive')) NOT NULL DEFAULT 'active',
    FOREIGN KEY (user_ID) REFERENCES User(user_ID)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS IP_Table (
                IP_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                block_ID INTEGER,
                edited_by_user_ID INTEGER,
                customer_ID INTEGER,
                customer_name TEXT,
                customer_surname TEXT,
                IP_adress TEXT NOT NULL UNIQUE,
                reservation TEXT,
                note TEXT,
                start_date DATE,
                end_date DATE,
                FOREIGN KEY (block_ID) REFERENCES IP_Blocks(block_ID),
                FOREIGN KEY (edited_by_user_ID) REFERENCES User(user_ID),
                FOREIGN KEY (customer_ID) REFERENCES Customer(customer_ID),
                FOREIGN KEY (customer_name) REFERENCES Customer(customer_name),
                FOREIGN KEY (customer_surname) REFERENCES Customer(customer_surname)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Logs (
    log_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    user_ID INTEGER,
    action TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_ID) REFERENCES User(user_ID)
)
""")

# Kaydet ve kapat zorunlu
conn.commit()
conn.close()

#deneme
print("Tablolar başarıyla oluşturuldu!")
import sqlite3
import os

# Veritabanı dosya yolu
db_path = os.path.join('database','ip_data.db')

# Veritabanına bağlan
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    INSERT INTO User (username, password,name,surname,active_session) VALUES (?, ?, ?, ?, ?)
""", ("kullanıcı1", "123456","Kullanıcı","Bir",1))

cursor.execute("""
    INSERT INTO Customer (customer_name,customer_surname) VALUES (?, ?)
""", ("musteri2", "soyad2"))

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()
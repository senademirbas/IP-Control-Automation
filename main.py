import sqlite3
import os

# Veritabanı dosya yolu
db_path = os.path.join('database','ip_data.db')

# Veritabanına bağlan
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# User tablosundaki tüm verileri sil
cursor.execute("DELETE FROM user")

# Yeni bir kayıt ekle
cursor.execute("""
    INSERT INTO User (username, password,name,surname, active_session) VALUES (?, ?, ?, ?, ?)
""", ("kullanıcı1", "123456","Kullanıcı","Bir",1))

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()
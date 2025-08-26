import sqlite3
import os

# Veritabanı dosya yolu
db_path = os.path.join('database','ip_data.db')

# Veritabanına bağlan
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


# Yeni bir kayıt ekle
cursor.execute("""
    INSERT INTO Customer (customer_name,customer_surname) VALUES (?, ?)
""", ("musteri1", "2"))

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()
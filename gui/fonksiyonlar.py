import sqlite3
import os

def ipwrite(block_id):
    #veritabanı yolu BaseDIR -> database -> ip_data.db
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(BASE_DIR, "database", "ip_data.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #block_id ye göre al
    cursor.execute("SELECT * FROM IP_Table WHERE block_ID = ?", (block_id,))
    rows = cursor.fetchall()

    if rows:
        print(f"Block {block_id} için IP kayıtları:")
        for row in rows:
            print(row)
    else:
        print(f"Block {block_id} için IP kaydı yok.")

    conn.close()

ipwrite(1) 


import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QGroupBox, QComboBox, QGridLayout
from PyQt6.QtGui import QIcon
import ipaddress
import sqlite3
import os
from datetime import datetime
import pytz

istanbul_now = datetime.now(pytz.timezone("Europe/Istanbul"))

class IpOtApp(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("IP Kontrol Otomasyon Sistemi")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)

        # Blok oluşturma arayüzü
        create_box = QGroupBox("IP Bloğu Oluştur")
        create_layout = QGridLayout(create_box)
        self.input_label = QComboBox()
        self.input_label.addItems(["CIDR", "Başlangıç ve Bitiş"])
        self.input_block_name = QLineEdit()
        self.input_block_name.setPlaceholderText("Blok Başlığı")
        self.input_asno = QLineEdit()
        self.input_asno.setPlaceholderText("Detay/ASNO")
        self.input_cidr = QLineEdit()
        self.input_cidr.setPlaceholderText("CIDR (örn: 192.168.1.0/24)")
        self.input_range_start = QLineEdit()
        self.input_range_start.setPlaceholderText("Başlangıç IP (örn: 192.168.1.1)")
        self.input_range_end = QLineEdit()
        self.input_range_end.setPlaceholderText("Bitiş IP (örn: 192.168.1.63)")
        self.create_button = QPushButton("Oluştur")
        self.create_button.clicked.connect(self.create_block)

        create_layout.addWidget(QLabel("Type"), 0, 0)
        create_layout.addWidget(self.input_label, 0, 1)
        create_layout.addWidget(QLabel("Blok Başlığı"), 1, 0)
        create_layout.addWidget(self.input_block_name, 1, 1)
        create_layout.addWidget(QLabel("Detay/ASNO"), 2, 0)
        create_layout.addWidget(self.input_asno, 2, 1)
        create_layout.addWidget(QLabel("CIDR"), 3, 0)
        create_layout.addWidget(self.input_cidr, 3, 1)
        create_layout.addWidget(QLabel("Range Start"), 4, 0)
        create_layout.addWidget(self.input_range_start, 4, 1)
        create_layout.addWidget(QLabel("Range End"), 5, 0)
        create_layout.addWidget(self.input_range_end, 5, 1)
        create_layout.addWidget(self.create_button, 6, 1)
        layout.addWidget(create_box)

    def create_block(self):
        db_path = os.path.join(os.path.dirname(__file__), "..", "database", "ip_data.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        block_name = self.input_block_name.text()
        asno = self.input_asno.text()

        if self.input_label.currentText() == "CIDR":
            cidr_text = self.input_cidr.text()
            cursor.execute("SELECT COUNT(*) FROM IP_Blocks WHERE CIDR=?", (cidr_text,))
            if cursor.fetchone()[0] > 0:
                print("Bu CIDR bloğu zaten mevcut!")
                conn.close()
                return
            try:
                net = ipaddress.ip_network(cidr_text, strict=False)
                cursor.execute(
                    "INSERT INTO IP_Blocks (user_ID, block_name, range_start, range_end, CIDR, asno, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (self.user_id, block_name, str(net.network_address), str(net.broadcast_address), cidr_text, asno, istanbul_now.strftime("%Y-%m-%d %H:%M:%S"))
                )
                block_id = cursor.lastrowid  # Eklenen bloğun ID'si
                # IP_Table'a IP'leri ekle
                for ip in net.hosts():
                    cursor.execute(
                        "INSERT INTO IP_Table (block_ID, IP_adress, reservation) VALUES (?, ?, ?)",
                        (block_id, str(ip), "0")
                    )
                conn.commit()
                print("CIDR IP Bloğu ve IP'ler veritabanına kaydedildi.")
            except Exception as e:
                print(f"Hata: {e}")
        else:
            start_ip = self.input_range_start.text()
            end_ip = self.input_range_end.text()
            cursor.execute("SELECT COUNT(*) FROM IP_Blocks WHERE range_start=? AND range_end=?", (start_ip, end_ip))
            if cursor.fetchone()[0] > 0:
                print("Bu IP aralığı zaten mevcut!")
                conn.close()
                return
            try:
                cursor.execute(
                    "INSERT INTO IP_Blocks (user_ID, block_name, range_start, range_end, CIDR, asno, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (self.user_id, block_name, start_ip, end_ip, None, asno, istanbul_now.strftime("%Y-%m-%d %H:%M:%S"))
                )
                block_id = cursor.lastrowid
                # IP_Table'a IP'leri ekle
                start = ipaddress.IPv4Address(start_ip)
                end = ipaddress.IPv4Address(end_ip)
                for ip_int in range(int(start), int(end)+1):
                    ip_str = str(ipaddress.IPv4Address(ip_int))
                    cursor.execute(
                        "INSERT INTO IP_Table (block_ID, IP_adress, reservation) VALUES (?, ?, ?)",
                        (block_id, ip_str, "0")
                    )
                conn.commit()
                print("Range IP Bloğu ve IP'ler veritabanına kaydedildi.")
            except Exception as e:
                print(f"Hata: {e}")
        conn.close()




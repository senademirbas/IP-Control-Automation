import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, 
                             QLineEdit, QGroupBox, QComboBox, QGridLayout, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QMessageBox, QHBoxLayout)
from PyQt6.QtGui import QIcon
import ipaddress
import sqlite3
import os
from datetime import datetime
import pytz

istanbul_now = datetime.now(pytz.timezone("Europe/Istanbul"))

class IpBlockDetailWindow(QWidget):
    def __init__(self, block_id):
        super().__init__()
        self.block_id = block_id
        self.setWindowTitle("IP Blok Detayı")
        self.setGeometry(200, 200, 800, 600)
        
        layout = QVBoxLayout(self)
        
        # Başlık
        layout.addWidget(QLabel(f"Blok ID: {block_id} IP Listesi"))
        
        # Tablo
        self.ip_table = QTableWidget()
        layout.addWidget(self.ip_table)
        
        # Düzenleme alanları
        edit_group = QGroupBox("IP Düzenle")
        edit_layout = QGridLayout(edit_group)
        
        edit_layout.addWidget(QLabel("IP Adresi:"), 0, 0)
        self.edit_ip = QLineEdit()
        self.edit_ip.setReadOnly(True)
        edit_layout.addWidget(self.edit_ip, 0, 1)
        
        edit_layout.addWidget(QLabel("Rezervasyon:"), 1, 0)
        self.edit_reservation = QComboBox()
        self.edit_reservation.addItems(["Boşta", "Rezerve"])
        edit_layout.addWidget(self.edit_reservation, 1, 1)
        
        edit_layout.addWidget(QLabel("Müşteri Adı:"), 2, 0)
        self.edit_customer_name = QLineEdit()
        self.edit_customer_name.setPlaceholderText("Müşteri adı girin")
        edit_layout.addWidget(self.edit_customer_name, 2, 1)
        
        edit_layout.addWidget(QLabel("Müşteri Soyadı:"), 3, 0)
        self.edit_customer_surname = QLineEdit()
        self.edit_customer_surname.setPlaceholderText("Müşteri soyadı girin")
        edit_layout.addWidget(self.edit_customer_surname, 3, 1)
        
        edit_layout.addWidget(QLabel("Not:"), 4, 0)
        self.edit_note = QLineEdit()
        edit_layout.addWidget(self.edit_note, 4, 1)
        
        # Butonlar
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Kaydet")
        self.save_button.clicked.connect(self.save_ip_changes)
        self.cancel_button = QPushButton("İptal")
        self.cancel_button.clicked.connect(self.clear_edit_fields)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        edit_layout.addLayout(button_layout, 5, 0, 1, 2)
        layout.addWidget(edit_group)
        
        # Tablo tıklama olayını bağla
        self.ip_table.cellClicked.connect(self.load_ip_to_edit)
        
        self.load_ips(block_id)

    def load_ips(self, block_id):
        db_path = os.path.join(os.path.dirname(__file__), "..", "database", "ip_data.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.IP_ID, i.IP_adress, i.reservation, 
                   c.customer_name, c.customer_surname, i.note,
                   i.customer_ID
            FROM IP_Table i
            LEFT JOIN Customer c ON i.customer_ID = c.customer_ID
            WHERE i.block_ID=?
        """, (block_id,))
        ips = cursor.fetchall()
        conn.close()
        
        self.ip_table.setRowCount(len(ips))
        self.ip_table.setColumnCount(7)
        self.ip_table.setHorizontalHeaderLabels(["ID", "IP Adresi", "Rezervasyon", "Müşteri Adı", "Müşteri Soyadı", "Not", "Müşteri ID"])
        
        for row, ip in enumerate(ips):
            for col, value in enumerate(ip):
                self.ip_table.setItem(row, col, QTableWidgetItem(str(value) if value is not None else ""))
        
        self.ip_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Müşteri ID sütununu gizle
        self.ip_table.setColumnHidden(6, True)

    def load_ip_to_edit(self, row, col):
        # Seçilen satırdaki verileri düzenleme alanlarına yükle
        ip_id = self.ip_table.item(row, 0).text()
        ip_address = self.ip_table.item(row, 1).text()
        reservation = self.ip_table.item(row, 2).text()
        customer_name = self.ip_table.item(row, 3).text() if self.ip_table.item(row, 3) else ""
        customer_surname = self.ip_table.item(row, 4).text() if self.ip_table.item(row, 4) else ""
        note = self.ip_table.item(row, 5).text() if self.ip_table.item(row, 5) else ""
        
        self.current_ip_id = ip_id
        self.edit_ip.setText(ip_address)
        self.edit_reservation.setCurrentText("Rezerve" if reservation == "1" else "Boşta")
        self.edit_customer_name.setText(customer_name)
        self.edit_customer_surname.setText(customer_surname)
        self.edit_note.setText(note)

    def get_customer_id(self, customer_name, customer_surname):
        """Müşteri adı ve soyadına göre customer_ID'yi bulur"""
        if not customer_name or not customer_surname:
            return None
            
        db_path = os.path.join(os.path.dirname(__file__), "..", "database", "ip_data.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT customer_ID FROM Customer 
            WHERE customer_name = ? AND customer_surname = ?
        """, (customer_name, customer_surname))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None

    def save_ip_changes(self):
        if not hasattr(self, 'current_ip_id'):
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir IP seçin.")
            return
        
        try:
            customer_name = self.edit_customer_name.text().strip()
            customer_surname = self.edit_customer_surname.text().strip()
            
            # Müşteri bilgileri girilmişse kontrol et
            customer_id = None
            if customer_name and customer_surname:
                customer_id = self.get_customer_id(customer_name, customer_surname)
                if customer_id is None:
                    # Müşteri bulunamadı, yeni müşteri oluştur
                    reply = QMessageBox.question(self, "Müşteri Bulunamadı", 
                                               f"{customer_name} {customer_surname} isimli müşteri bulunamadı. Yeni müşteri olarak eklemek ister misiniz?",
                                               QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                    if reply == QMessageBox.StandardButton.Yes:
                        db_path = os.path.join(os.path.dirname(__file__), "..", "database", "ip_data.db")
                        conn = sqlite3.connect(db_path)
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO Customer (customer_name, customer_surname)
                            VALUES (?, ?)
                        """, (customer_name, customer_surname))
                        customer_id = cursor.lastrowid
                        conn.commit()
                        conn.close()
                        QMessageBox.information(self, "Başarılı", "Yeni müşteri eklendi.")
                    else:
                        return
            
            db_path = os.path.join(os.path.dirname(__file__), "..", "database", "ip_data.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            reservation_value = "1" if self.edit_reservation.currentText() == "Rezerve" else "0"
            
            cursor.execute("""
                UPDATE IP_Table 
                SET reservation=?, customer_ID=?, note=?, edited_by_user_ID=?
                WHERE IP_ID=?
            """, (
                reservation_value,
                customer_id,
                self.edit_note.text(),
                1,  # Örnek kullanıcı ID'si, gerçek uygulamada oturum açan kullanıcı ID'si kullanılmalı
                self.current_ip_id
            ))
            
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Başarılı", "IP bilgileri güncellendi.")
            
            # Tabloyu yenile
            self.load_ips(self.block_id)
            self.clear_edit_fields()
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt sırasında hata oluştu: {str(e)}")

    def clear_edit_fields(self):
        self.edit_ip.clear()
        self.edit_reservation.setCurrentIndex(0)
        self.edit_customer_name.clear()
        self.edit_customer_surname.clear()
        self.edit_note.clear()
        if hasattr(self, 'current_ip_id'):
            delattr(self, 'current_ip_id')


class IpOtApp(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("IP Kontrol Otomasyon Sistemi")
        self.setGeometry(100, 100, 900, 700)

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

        # Blokları tablo şeklinde göster
        self.block_table = QTableWidget()
        self.block_table.setColumnCount(7)
        self.block_table.setHorizontalHeaderLabels(["ID", "Başlık", "CIDR", "Range Start", "Range End", "ASNO", "Tarih"])
        self.block_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.block_table.cellDoubleClicked.connect(self.open_block_detail)
        layout.addWidget(QLabel("Oluşturulan/Kayıtlı IP Blokları:"))
        layout.addWidget(self.block_table)

        self.setLayout(layout)
        self.load_blocks()

    def load_blocks(self):
        db_path = os.path.join(os.path.dirname(__file__), "..", "database", "ip_data.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT block_ID, block_name, CIDR, range_start, range_end, asno, timestamp FROM IP_Blocks")
        blocks = cursor.fetchall()
        conn.close()
        self.block_table.setRowCount(len(blocks))
        for row, block in enumerate(blocks):
            for col, value in enumerate(block):
                self.block_table.setItem(row, col, QTableWidgetItem(str(value)))

    def open_block_detail(self, row, col):
        block_id_item = self.block_table.item(row, 0)
        if block_id_item:
            block_id = int(block_id_item.text())
            self.detail_window = IpBlockDetailWindow(block_id)
            self.detail_window.show()

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
                QMessageBox.warning(self, "Uyarı", "Bu CIDR bloğu zaten mevcut!")
                conn.close()
                return
            try:
                net = ipaddress.ip_network(cidr_text, strict=False)
                cursor.execute(
                    "INSERT INTO IP_Blocks (user_ID, block_name, range_start, range_end, CIDR, asno, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (self.user_id, block_name, str(net.network_address), str(net.broadcast_address), cidr_text, asno, istanbul_now.strftime("%Y-%m-%d %H:%M:%S"))
                )
                block_id = cursor.lastrowid
                # IP_Table'a IP'leri ekle
                for ip in net.hosts():
                    cursor.execute(
                        "INSERT INTO IP_Table (block_ID, IP_adress, reservation) VALUES (?, ?, ?)",
                        (block_id, str(ip), "0")
                    )
                conn.commit()
                QMessageBox.information(self, "Başarılı", "CIDR IP Bloğu ve IP'ler veritabanına kaydedildi.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Hata: {e}")
        else:
            start_ip = self.input_range_start.text()
            end_ip = self.input_range_end.text()
            cursor.execute("SELECT COUNT(*) FROM IP_Blocks WHERE range_start=? AND range_end=?", (start_ip, end_ip))
            if cursor.fetchone()[0] > 0:
                QMessageBox.warning(self, "Uyarı", "Bu IP aralığı zaten mevcut!")
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
                QMessageBox.information(self, "Başarılı", "Range IP Bloğu ve IP'ler veritabanına kaydedildi.")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Hata: {e}")
        conn.close()
        # Her başarılı eklemeden sonra blokları güncelle:
        self.load_blocks()


# Uygulamayı çalıştır
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IpOtApp(user_id=1)  # Örnek kullanıcı ID'si
    window.show()
    sys.exit(app.exec())
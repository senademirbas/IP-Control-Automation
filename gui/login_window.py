import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QGroupBox, QGridLayout
import sqlite3
import os
from main_window import  IpOtApp 
class IpOtoLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Kontrol Otomasyon Sistemi Login")
        self.setGeometry(750, 450, 400, 200)

        layout = QVBoxLayout(self)

        #login kutusu
        create_box = QGroupBox("Login")
        create_layout = QGridLayout(create_box)

        self.username_label = QLabel("Kullanıcı Adı:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Şifre:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton("Giriş Yap")
        self.login_button.clicked.connect(self.handle_login)

        create_layout.addWidget(self.username_label, 0, 0)
        create_layout.addWidget(self.username_input, 0, 1)
        create_layout.addWidget(self.password_label, 1, 0)
        create_layout.addWidget(self.password_input, 1, 1)
        create_layout.addWidget(self.login_button, 2, 0, 1, 2)

        layout.addWidget(create_box)
        self.setLayout(layout)


    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        #database yolu 
        db_path = os.path.join(os.path.dirname(__file__), "..", "database", "ip_data.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        #database den kullanıcı doğrulama yapıoruz
        cursor.execute("SELECT * FROM User WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            print(f"Giriş başarılı: {username}")
            user_id = user[0]  # user_ID sütunu
            self.main_window = IpOtApp(user_id)
            self.main_window.show()
            self.close()
        else:
            print("Hatalı kullanıcı adı veya şifre")



app = QApplication(sys.argv)
app.setStyleSheet("""
    QWidget {
        font-size:12px;
    }
    QPushButton {
        font-size:14px;
    }
""")
window = IpOtoLogin()
window.show()
app.exec()


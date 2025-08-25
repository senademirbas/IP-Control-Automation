import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit , QGroupBox , QComboBox , QGridLayout
from PyQt6.QtGui import QIcon
import ipaddress


class IpOtApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Kontrol Otomasyon Sistemi")
        self.setGeometry(100, 100, 800, 600)

       
        layout = QVBoxLayout(self)

        #blok
        create_box = QGroupBox("IP Bloğu Oluştur")
        create_layout = QGridLayout(create_box)
        self.input_label = QComboBox()
        self.input_type = QComboBox()

        self.input_label.addItems(["CIDR", "Başlangıç ve Bitiş"])
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
        create_layout.addWidget(QLabel("CIDR"), 2, 0)
        create_layout.addWidget(self.input_cidr, 2, 1)
        create_layout.addWidget(QLabel("Range Start"), 3, 0)
        create_layout.addWidget(self.input_range_start, 3, 1)
        create_layout.addWidget(QLabel("Range End"), 4, 0)
        create_layout.addWidget(self.input_range_end, 4, 1)
        create_layout.addWidget(self.create_button, 5, 1)
        layout.addWidget(create_box)
    
    def create_block(self):
        # IP bloğu oluşturma fonksiyonu
        print("IP Bloğu Oluşturuldu")


    

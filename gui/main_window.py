import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit
from PyQt6.QtGui import QIcon

class IpOtApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IP Kontrol Otomasyon Sistemi")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        #widget
         
        self.inputField = QLineEdit()
        button = QPushButton('Ip Giriniz')  
        self.output = QTextEdit()

        layout.addWidget(self.inputField)
        layout.addWidget(button)
        layout.addWidget(self.output)

        
    
#app       
app = QApplication(sys.argv)
app.setStyleSheet("""
    QWidget {
                  font-size:12px;
                  } 
    QpushButton {
                  font-size:5px}              }
                      """)
window = IpOtApp()
window.show()
app.exec()
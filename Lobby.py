import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QVBoxLayout,QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from jatek import futo
from jatek import Init,pontszam_mentese
from eredmenyek import MainWindow1



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Flappy Bird')
        self.setStyleSheet("background-color: #0bd3de;")
        self.setGeometry(700, 300, 500, 500)
        self.coinok = QLabel("0",self)
        self.coin_pontok = QLabel("Osszes coinod:")

        # Set icon and layout
        pixmap = QPixmap('cube.jpg')
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

        # Buttons
        self.gomb_1 = QPushButton('Indítás', self)
        self.gomb_2 = QPushButton('Eredmények', self)
        self.gomb_3 = QPushButton('Kilépés', self)

        Init()
        self.initUI()

    def showEvent(self, event):
        super().showEvent(event)
        self.update_coinok(0)

    def initUI(self):
        # Create horizontal layout for the label (coin_pontok)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 10, 0, 0)  # Adjust margins for alignment
        hbox.addWidget(self.coin_pontok)
        hbox.addWidget(self.coinok)
        hbox.setAlignment(Qt.AlignTop | Qt.AlignRight)

        vbox = QVBoxLayout()
        vbox.addWidget(self.gomb_1)
        vbox.addWidget(self.gomb_2)
        vbox.addWidget(self.gomb_3)
        vbox.setAlignment(Qt.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addLayout(hbox)
        main_layout.addLayout(vbox)

        # Create central widget and set layout
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)

        # Set central widget
        self.setCentralWidget(central_widget)

        self.coin_pontok.setStyleSheet("""
            color: #fce303;
            font-family: Times New Roman;
            font-weight: 500;
            font-size: 40px;
            height:30px;
        """)
        self.coinok.setStyleSheet("""
            color: #fce303;
            font-family: Times New Roman;
            font-weight: 500;
            font-size: 40px;
            height:30px;
        
        
        """)
        self.gomb_1.setStyleSheet("""
            QPushButton{
                background-color: #2196F3;
                color: #ffffff;
                font-size: 20px;
                font-weight: 500;
                border-radius: 10px;
                height: 50px;
            }
            QPushButton:hover {
                background-color: #42a5f5;
            }
        """)
        self.gomb_2.setStyleSheet("""
            QPushButton{
                background-color: rgb(240, 233, 29);
                color: rgb(245, 245, 245);
                font-size: 20px;
                font-weight: 500;
                border-radius: 10px;
                height: 50px;
            }
            QPushButton:hover {
                background-color: rgb(255, 255, 102);
            }
        """)
        self.gomb_3.setStyleSheet("""
            QPushButton{
                background-color: rgb(3, 2, 23);
                color: rgb(245, 245, 245);
                font-size: 20px;
                font-weight: 500;
                border-radius: 10px;
                height: 50px;
            }
            QPushButton:hover {
                background-color: rgb(60, 48, 112);
            }
        """)

        # Button connections
        self.gomb_1.clicked.connect(self.inditas)
        self.gomb_2.clicked.connect(self.eredmeny)
        self.gomb_3.clicked.connect(self.kilepes)



    def update_coinok(self, coin_szama):
        file_path = "C:/Users/hunor/OneDrive/Asztali gép/pontszam.txt"
        try:
            with open(file_path, "r") as file:
                beolvasas = file.read().splitlines()
                total_coin = 0
                for sor in beolvasas:
                    parts = sor.split()  # Szétválasztjuk a számokat
                    if len(parts) == 2:
                        _, coin = map(int, parts)  # Az első érték a pont, a második a coin
                        total_coin += coin

                self.coinok.setText(str(total_coin))  # Az összesített coin kiírása
        except Exception as e:
            pass
        
    def inditas(self):
        self.hide()# Az ablak elrejtése
        self.Eredmeny = futo(self.leallitas)  # Játék indítása, callback-ként a főmenü visszahívása

    def leallitas(self):
        self.show()  # A főmenü újra megjelenítése

    def eredmeny(self):
        self.hide()
        self.fomenu = MainWindow1()
        self.fomenu.show()


    def kilepes(self):
        from jatek import fajl_torol
        fajl_torol()
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
# Változás teszteléshez

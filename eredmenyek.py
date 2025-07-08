import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QSizePolicy,QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class MainWindow1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(700, 300, 500, 500)
        self.setStyleSheet("background-color: #0bd3de;")
        self.label_1 = QLabel("Eredmenyek:", self)
        self.border = QLabel("Meg nincsenek elozo rekordok,<br> Kerlek jatszodj par kort!", self)
        self.gomb = QPushButton("Visszalepes", self)
        self.scroll_area = QScrollArea(self)
        self.innitUi1()
        

    def innitUi1(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.label_1.setStyleSheet(
            "font-size: 30px; font-family: Times New Roman; font-weight: 650; color: #f5ea25; text-decoration: underline;"
        )
        self.gomb.setStyleSheet("""
            QPushButton{
                font-size: 15px; font-family: Times New Roman;
                font-weight: 500; color: #edf5f3;
                background-color: red;
            }
            QPushButton:hover{
                background-color: #d95f5f;
            }
        """)

        self.border.setStyleSheet("""background-color: rgba(255,255,255,0.8);
                                  border: 5px solid rgba(0,0,0,0.5);
                                  border-radius: 65px;
                                  font-size:20px;
                                  color: rgba(255, 0, 0, 0.6);
                                   """)


        self.label_1.setAlignment(Qt.AlignHCenter)
        self.border.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.scroll_area.setWidget(self.border)
        self.border.setContentsMargins(10, 25, 10, 10)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
                    QScrollBar:vertical {
                        background-color: #d3d3d3;  # világos szürke háttér a görgetősávnak
                        border: 2px solid #a0a0a0;  # Sötétebb szürke szegély
                        width: 12px;
                    }

                    QScrollBar::handle:vertical {
                        background-color: #888888;  # A görgethető rész sötétszürke
                        border-radius: 6px;
                    }

                    QScrollBar::handle:vertical:hover {
                        background-color: #555555;  # Ha ráhoverelünk, sötétebb szürke
                    }

                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                        border: 2px solid #a0a0a0;  # A gombok szegélyei
                        background-color: #f0f0f0;
                        height: 15px;
                    }
                """)
        vbox = QVBoxLayout()
        vbox.addWidget(self.label_1)
        vbox.addWidget(self.scroll_area)
        vbox.addStretch(1)
        vbox.addWidget(self.gomb, alignment=Qt.AlignBottom)

        self.border.setMinimumSize(100, 400)
        self.gomb.setContentsMargins(0, 30, 0, 20)
        self.file_olvasas()
        central_widget.setLayout(vbox)
        self.gomb.clicked.connect(self.visszalepes)

    def file_olvasas(self):
        file_path = "C:/Users/hunor/Desktop/pontszam.txt"
        try:
            with open(file_path, "r") as file:
                beolvasas = file.read().splitlines()  # Soronkénti beolvasás

                szoveg = ""
                max_pont = 0
                max_coin = 0
                max_pont_meccs = 0
                max_coin_meccs = 0
                ujra_szamlalas = False
                uj_index = 14 #

                for i, pont in enumerate(beolvasas):
                    pont = pont.strip()  # Felesleges szóközök eltávolítása
                    if not pont:
                        continue  # Ha üres sor, lépjünk tovább

                    parts = pont.split()
                    if len(parts) != 2:
                        print(f"Figyelmeztetés: Hiba a sorban: {pont}")
                        continue

                    try:
                        pont_szam, coin_szam = map(int, parts)
                    except ValueError:
                        print(f"Hibás adat: {pont}")
                        continue

                    # Ha elérjük a 12. meccset, resetelünk, de megtartjuk a max értékeket
                    if (i + 1) %13 == 0:
                        szoveg = ""
                        ujra_szamlalas = True  # Elindítjuk az újraszámolást
                        uj_index = i+2
                    else:
                        meccs_szam = i+1

                    if ujra_szamlalas:
                        meccs_szam = uj_index
                        uj_index += 1
                    else:
                        meccs_szam = i + 1

                    if pont_szam > max_pont:
                        max_pont = pont_szam
                        max_coin = coin_szam
                        max_pont_meccs = meccs_szam
                        szoveg += f"{meccs_szam}. meccs, új rekord: {pont_szam} pont, {coin_szam} coin<br>\n"
                    else:
                        szoveg += f"{meccs_szam}. meccs pontszáma: {pont_szam} pont, {coin_szam} coin<br>\n"

                    if coin_szam > max_coin:
                        max_coin = coin_szam
                        max_coin_meccs = meccs_szam +1

                szoveg = (f"<font color='#5fcf7b'>Legnagyobb pontszám: {max_pont} pont "
                          f"({max_pont_meccs}.meccs)</font><br>") + szoveg
                szoveg = (f"<font color='#fcbe03'>Legnagyobb coinszám: {max_coin} coin "
                          f"({max_coin_meccs}.meccs)</font><br>") + szoveg

                self.border.setText(szoveg)

        except Exception as e:
            pass

    def visszalepes(self):
        from Lobby import MainWindow
        self.hide()
        self.fomenu1 = MainWindow()
        self.fomenu1.show()

if __name__ == '__main__':
    app1 = QApplication(sys.argv)
    window1 = MainWindow1()
    window1.show()
    sys.exit(app1.exec_())

# Mentési logika komment teszt
# Mentési logika komment teszt

import sys
import math
import os
from random import randint
import webbrowser
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from urllib.request import urlopen
from bs4 import BeautifulSoup

class moje_okno(QMainWindow):
    def __init__(self):
        super(moje_okno,self).__init__()
        self.setGeometry(500,500,300,220)
        self.setWindowTitle("Projekt 2.0")

        #PRZYCISKI
        self.p_kupno = QPushButton(self)
        self.p_kupno.setText("Kupno")
        self.p_kupno.setGeometry(50,10,200,50)
        self.kupno_okno = Kupno()
        self.p_kupno.clicked.connect(self.kupno_okno.show)

        self.p_sprzed = QPushButton(self)
        self.p_sprzed.setText("Sprzedaż")
        self.p_sprzed.setGeometry(50,60, 200, 50)
        self.sprzed_okno = Sprzedaz()
        self.p_sprzed.clicked.connect(self.sprzed_okno.show)

        self.p_aktualnosci = QPushButton(self)
        self.p_aktualnosci.setText("Aktualności")
        self.p_aktualnosci.setGeometry(50,110, 200, 50)
        self.aktual_okno = Aktualnosci()
        self.p_aktualnosci.clicked.connect(self.aktual_okno.show)

        self.p_kurs = QPushButton(self)
        self.p_kurs.setText("Aktualny kurs walut")
        self.p_kurs.setGeometry(50,160, 200, 50)
        self.kurs_okno = Aktualny_kurs()
        self.p_kurs.clicked.connect(self.kurs_okno.show)



class Kupno(QWidget):
    def __init__(self):
        super(Kupno, self).__init__()
        self.setGeometry(500,500,750,360)
        self.setWindowTitle("Kupno")

        self.euro = QRadioButton(self)
        self.euro.setGeometry(40,20,80,15)
        self.euro.setText("Euro")

        self.dolar = QRadioButton(self)
        self.dolar.setGeometry(40, 50, 120, 15)
        self.dolar.setText("Dolar Amerykański")

        self.funt = QRadioButton(self)
        self.funt.setGeometry(40, 80, 120, 15)
        self.funt.setText("Funt Szwajcarski")

        self.peso = QRadioButton(self)
        self.peso.setGeometry(40, 110, 120, 15)
        self.peso.setText("Funt Brytyjski")

        self.przelicz = QPushButton(self)
        self.przelicz.setGeometry(20,300,400,40)
        self.przelicz.setText("&Przelicz")
        self.przelicz.clicked.connect(self.przeliczenie)

        self.pole_tekst = QLineEdit(self)
        self.pole_tekst.setGeometry(30,180,130,50)
        self.pole_tekst.setFont(QFont('Arial',16))

        self.wynik = QLabel(self)
        self.wynik.setGeometry(230,60,200,100)
        self.wynik.setFont(QFont('Arial',16))

        self.tabela = QTableWidget(self)
        self.tabela.setGeometry(420, 10, 320, 340)
        self.tabela.setColumnCount(4)
        self.tabela.setColumnWidth(0, 100)
        self.tabela.setColumnWidth(1, 70)
        self.tabela.setColumnWidth(2, 70)
        self.tabela.setColumnWidth(3, 70)
        self.tabela.setHorizontalHeaderLabels(("Zamiana", "Kurs", "Ilość","Wartość"))
        self.tabela.verticalHeader().hide()
        obecny_rząd = self.tabela.rowCount()




    @pyqtSlot()
    def przeliczenie(self):
        nadawca = self.sender()

        html = urlopen('https://kantoronline.pl/kursy-walut')
        bs = BeautifulSoup(html.read(), 'html.parser')
        eurkp = bs.find(id='eurbuy')
        euro_kup = eurkp.getText()
        usdkp = bs.find(id='usdbuy')
        usd_kup = usdkp.getText()
        chfkp = bs.find(id='chfbuy')
        chf_kup = chfkp.getText()
        gbpkp = bs.find(id='gbpbuy')
        gbp_kup = gbpkp.getText()

        obecny_rząd = self.tabela.rowCount()
        self.tabela.insertRow(obecny_rząd)
        plneur = "PLN->EUR"
        plnusd = "PLN->USD"
        plnchf = "PLN->CHF"
        plngbp = "PLN->GBP"

        try:

            euro = self.euro.isChecked() == True
            dolar = self.dolar.isChecked() == True
            funt = self.funt.isChecked() == True
            peso = self.peso.isChecked() == True
            wartosc1 = float(self.pole_tekst.text())
            wartosc2 = float(euro_kup)
            wartosc3 = float(usd_kup)
            wartosc4 = float(chf_kup)
            wartosc5 = float(gbp_kup)
            przel = ""

            if euro and nadawca.text() == "&Przelicz":
                przel = wartosc1 / wartosc2
                wwynik = round(przel,2)
                self.tabela.setItem(obecny_rząd, 0,QTableWidgetItem(plneur))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(euro_kup))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(self.pole_tekst.text()))

            elif dolar and nadawca.text() == "&Przelicz":
                przel = wartosc1 / wartosc3
                wwynik = round(przel, 2)
                self.tabela.setItem(obecny_rząd, 0, QTableWidgetItem(plnusd))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(usd_kup))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(self.pole_tekst.text()))

            elif funt and nadawca.text() == "&Przelicz":
                przel = wartosc1 / wartosc4
                wwynik = round(przel, 2)
                self.tabela.setItem(obecny_rząd, 0, QTableWidgetItem(plnchf))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(chf_kup))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(self.pole_tekst.text()))

            elif peso and nadawca.text() == "&Przelicz":
                przel = wartosc1 / wartosc5
                wwynik = round(przel, 2)
                self.tabela.setItem(obecny_rząd, 0, QTableWidgetItem(plngbp))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(gbp_kup))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(self.pole_tekst.text()))

            else:
                QMessageBox.critical(
                    self, "Błąd", "Nie można mnożyć przez zero!")
                return

            self.wynik.setText(str(wwynik))
            self.tabela.setItem(obecny_rząd, 3, QTableWidgetItem(self.wynik.text()))

        except ValueError:
            QMessageBox.warning(self, "Błąd", "Program nie dziaua", QMessageBox.Ok)




class Sprzedaz(QWidget):
    def __init__(self):
        super(Sprzedaz, self).__init__()
        self.setGeometry(500,500,750,360)
        self.setWindowTitle("Sprzedaż")

        self.euro = QRadioButton(self)
        self.euro.setGeometry(40, 20, 80, 15)
        self.euro.setText("Euro")

        self.dolar = QRadioButton(self)
        self.dolar.setGeometry(40, 50, 120, 15)
        self.dolar.setText("Dolar Amerykański")

        self.funt = QRadioButton(self)
        self.funt.setGeometry(40, 80, 120, 15)
        self.funt.setText("Funt Szwajcarski")

        self.peso = QRadioButton(self)
        self.peso.setGeometry(40, 110, 120, 15)
        self.peso.setText("Funt Brytyjski")

        self.przelicz = QPushButton(self)
        self.przelicz.setGeometry(20, 300, 400, 40)
        self.przelicz.setText("&Przelicz")
        self.przelicz.clicked.connect(self.przeliczenie)

        self.pole_tekst = QLineEdit(self)
        self.pole_tekst.setGeometry(30, 180, 130, 50)
        self.pole_tekst.setFont(QFont('Arial', 16))

        self.wynik = QLabel(self)
        self.wynik.setGeometry(230, 60, 200, 100)
        self.wynik.setFont(QFont('Arial', 16))

        self.tabela = QTableWidget(self)
        self.tabela.setGeometry(420, 10, 320, 340)
        self.tabela.setColumnCount(4)
        self.tabela.setColumnWidth(0, 100)
        self.tabela.setColumnWidth(1, 70)
        self.tabela.setColumnWidth(2, 70)
        self.tabela.setColumnWidth(3, 70)
        self.tabela.setHorizontalHeaderLabels(("Zamiana", "Kurs", "Ilość", "Wartość"))
        self.tabela.verticalHeader().hide()
        obecny_rząd = self.tabela.rowCount()

    @pyqtSlot()
    def przeliczenie(self):
        nadawca = self.sender()

        html = urlopen('https://kantoronline.pl/kursy-walut')
        bs = BeautifulSoup(html.read(), 'html.parser')
        eurkp = bs.find(id='eursell')
        euro_kup = eurkp.getText()
        usdkp = bs.find(id='usdsell')
        usd_kup = usdkp.getText()
        chfkp = bs.find(id='chfsell')
        chf_kup = chfkp.getText()
        gbpkp = bs.find(id='gbpsell')
        gbp_kup = gbpkp.getText()

        obecny_rząd = self.tabela.rowCount()
        self.tabela.insertRow(obecny_rząd)
        eurpln = "EUR->PLN"
        usdpln = "USD->PLN"
        chfpln = "CHF->PLN"
        gbppln = "GBP->PLN"

        try:

            euro = self.euro.isChecked() == True
            dolar = self.dolar.isChecked() == True
            funt = self.funt.isChecked() == True
            peso = self.peso.isChecked() == True
            wartosc1 = float(self.pole_tekst.text())
            wartosc2 = float(euro_kup)
            wartosc3 = float(usd_kup)
            wartosc4 = float(chf_kup)
            wartosc5 = float(gbp_kup)
            przel = ""

            if euro and nadawca.text() == "&Przelicz":
                przel = wartosc1 * wartosc2
                wwynik = round(przel,2)
                self.tabela.setItem(obecny_rząd, 0, QTableWidgetItem(eurpln))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(euro_kup))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(self.pole_tekst.text()))

            elif dolar and nadawca.text() == "&Przelicz":
                przel = wartosc1 * wartosc3
                wwynik = round(przel, 2)
                self.tabela.setItem(obecny_rząd, 0, QTableWidgetItem(usdpln))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(usd_kup))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(self.pole_tekst.text()))

            elif funt and nadawca.text() == "&Przelicz":
                przel = wartosc1 * wartosc4
                wwynik = round(przel, 2)
                self.tabela.setItem(obecny_rząd, 0, QTableWidgetItem(chfpln))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(chf_kup))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(self.pole_tekst.text()))

            elif peso and nadawca.text() == "&Przelicz":
                przel = wartosc1 * wartosc5
                wwynik = round(przel, 2)
                self.tabela.setItem(obecny_rząd, 0, QTableWidgetItem(gbppln))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(gbp_kup))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(self.pole_tekst.text()))

            else:
                QMessageBox.critical(
                    self, "Błąd", "Nie można mnożyć przez zero!")
                return

            self.wynik.setText(str(wwynik))
            self.tabela.setItem(obecny_rząd, 3, QTableWidgetItem(self.wynik.text()))

        except ValueError:
            QMessageBox.warning(self, "Błąd", "Program nie dziaua", QMessageBox.Ok)

class Aktualnosci(QWidget):
    def __init__(self):
        html = urlopen('https://www.pb.pl/puls-inwestora/waluty/')
        bs = BeautifulSoup(html.read(), 'html.parser')
        tytul = bs.find_all('h2')


        super(Aktualnosci, self).__init__()
        self.setGeometry(500, 500, 530, 360)
        self.setWindowTitle("Aktualności")

        self.artykul = QTextEdit(self)
        self.artykul.setGeometry(10, 120, 510, 180)
        self.artykul.setReadOnly(True)

        self.tytul1 = QRadioButton(self)
        self.tytul1.setGeometry(20, 30, 530, 20)
        self.tytul1.setText(tytul[0].get_text())
        self.tytul1.toggled.connect(self.funkcja)
        self.tytul1.toggled.connect(self.andnotacja)

        self.tytul2 = QRadioButton(self)
        self.tytul2.setGeometry(20, 60, 510, 20)
        self.tytul2.setText(tytul[1].get_text())
        self.tytul2.toggled.connect(self.funkcja)

        self.tytul3 = QRadioButton(self)
        self.tytul3.setGeometry(20, 90, 510, 20)
        self.tytul3.setText(tytul[2].get_text())
        self.tytul3.toggled.connect(self.funkcja)

        self.przycisk = QPushButton(self)
        self.przycisk.setGeometry(10, 310, 510, 40)
        self.przycisk.setText("&Przejdź do pełnego artykułu")
        self.przycisk.clicked.connect(self.andnotacja)

    @pyqtSlot()
    def funkcja(self):
        a1 = self.tytul1.isChecked() == True
        a2 = self.tytul2.isChecked() == True
        a3 = self.tytul3.isChecked() == True

        html = urlopen('https://www.pb.pl/puls-inwestora/waluty/')
        bs = BeautifulSoup(html.read(), 'html.parser')
        podglad = bs.find_all('p')

        if a1:
            self.artykul.setText(podglad[0].get_text())

        elif a2:
            self.artykul.setText(podglad[1].get_text())

        elif a3:
            self.artykul.setText(podglad[2].get_text())

        else:
            return

    @pyqtSlot()
    def andnotacja(self):
        nadawca = self.sender()
        a1 = self.tytul1.isChecked() == True
        a2 = self.tytul2.isChecked() == True
        a3 = self.tytul3.isChecked() == True

        html = urlopen('https://www.pb.pl/puls-inwestora/waluty/')
        bs = BeautifulSoup(html.read(), 'lxml')
        linki = []
        for link in bs.find_all('a'):
            linki.append(link.get('href'))

        if a1 and nadawca.text() == "&Przejdź do pełnego artykułu":
            artlink = ("https://pb.pl" + linki[97])
            webbrowser.open_new_tab(artlink)

        elif a2 and nadawca.text() == "&Przejdź do pełnego artykułu":
            artlink = ("https://pb.pl" + linki[98])
            webbrowser.open_new_tab(artlink)

        elif a3 and nadawca.text() == "&Przejdź do pełnego artykułu":
            artlink = ("https://pb.pl" + linki[99])
            webbrowser.open_new_tab(artlink)

        else:
            return





class Aktualny_kurs(QWidget):
    def __init__(self):
        super(Aktualny_kurs, self).__init__()
        self.setGeometry(500,500,480,150)
        self.setWindowTitle("Aktualny kurs")

        self.tabela = QTableWidget(self)
        self.tabela.setRowCount(4)
        self.tabela.setColumnCount(3)
        self.tabela.setColumnWidth(0,120)
        self.tabela.setGeometry(0,0,380,150)
        self.tabela.setHorizontalHeaderLabels(("Waluta","Kupno","Sprzedaż"))
        self.tabela.verticalHeader().hide()
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela.setItem(0,0,QTableWidgetItem("Euro"))
        self.tabela.setItem(1,0,QTableWidgetItem("Dolar Amerykański"))
        self.tabela.setItem(2,0,QTableWidgetItem("Funt Szwajcarski"))
        self.tabela.setItem(3,0,QTableWidgetItem("Funt Brytyjski"))

        self.przycisk = QPushButton(self)
        self.przycisk.setGeometry(380, 0, 100, 150)
        self.przycisk.setText("&Odśwież")
        self.przycisk.clicked.connect(self.odswiez)

    @pyqtSlot()
    def odswiez(self):
        nadawca = self.sender()
        html = urlopen('https://kantoronline.pl/kursy-walut')
        bs = BeautifulSoup(html.read(), 'html.parser')
        eurkp = bs.find(id='eursell')
        euro_kup = eurkp.getText()
        usdkp = bs.find(id='usdsell')
        usd_kup = usdkp.getText()
        chfkp = bs.find(id='chfsell')
        chf_kup = chfkp.getText()
        gbpkp = bs.find(id='gbpsell')
        gbp_kup = gbpkp.getText()
        eurs = bs.find(id='eurbuy')
        euro_s = eurs.getText()
        usds = bs.find(id='usdbuy')
        usd_s = usds.getText()
        chfs = bs.find(id='chfbuy')
        chf_s = chfs.getText()
        gbps = bs.find(id='gbpbuy')
        gbp_s = gbps.getText()

        if nadawca.text() == "&Odśwież":
            self.tabela.setItem(0, 1, QTableWidgetItem(euro_kup))
            self.tabela.setItem(1, 1, QTableWidgetItem(usd_kup))
            self.tabela.setItem(2, 1, QTableWidgetItem(chf_kup))
            self.tabela.setItem(3, 1, QTableWidgetItem(gbp_kup))
            self.tabela.setItem(0, 2, QTableWidgetItem(euro_s))
            self.tabela.setItem(1, 2, QTableWidgetItem(usd_s))
            self.tabela.setItem(2, 2, QTableWidgetItem(chf_s))
            self.tabela.setItem(3, 2, QTableWidgetItem(gbp_s))
        else:
            QMessageBox.warning(self, "Błąd", "Brak danych", QMessageBox.Ok)








if __name__ == '__main__':
    app = QApplication([])
    window = moje_okno()
    window.show()
    sys.exit(app.exec())
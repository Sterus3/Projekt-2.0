import sys
import webbrowser
import openpyxl
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
from openpyxl import load_workbook


class moje_okno(QMainWindow):
    def __init__(self):
        super(moje_okno, self).__init__()
        self.setGeometry(500, 500, 300, 180)
        self.setWindowTitle("Projekt 2.0")

        self.p_wymiana = QPushButton(self)
        self.p_wymiana.setText("Wymiana")
        self.p_wymiana.setGeometry(50, 10, 200, 50)
        self.wymiana_okno = Wymiana()
        self.p_wymiana.clicked.connect(self.wymiana_okno.show)

        self.p_aktualnosci = QPushButton(self)
        self.p_aktualnosci.setText("Aktualności")
        self.p_aktualnosci.setGeometry(50, 60, 200, 50)
        self.aktual_okno = Aktualnosci()
        self.p_aktualnosci.clicked.connect(self.aktual_okno.show)

        self.p_kurs = QPushButton(self)
        self.p_kurs.setText("Aktualny kurs walut")
        self.p_kurs.setGeometry(50, 110, 200, 50)
        self.kurs_okno = Aktualny_kurs()
        self.p_kurs.clicked.connect(self.kurs_okno.show)


class Wymiana(QWidget):
    def __init__(self):
        super(Wymiana, self).__init__()
        self.setGeometry(500, 500, 750, 360)
        self.setWindowTitle("Wymiana")

        self.lista1 = QListWidget(self)
        self.lista1.setGeometry(20, 10, 200, 40)
        self.lista1.addItems(["PLN na walutę", "Waluta na PLN"])
        self.lista1.setCurrentRow(0)

        self.lista2 = QListWidget(self)
        self.lista2.setGeometry(20, 60, 200, 80)
        self.lista2.addItems(["Euro", "Dolar Amrykański", "Funt Szwajcarski", "Funt Brytyjski"])

        self.przelicz = QPushButton(self)
        self.przelicz.setGeometry(20, 300, 400, 40)
        self.przelicz.setText("&Przelicz")
        self.przelicz.clicked.connect(self.przeliczenie)

        self.pole_tekst = QLineEdit(self)
        self.pole_tekst.setGeometry(50, 220, 130, 50)
        self.pole_tekst.setFont(QFont('Comic Sans', 16))

        self.wynik = QLabel(self)
        self.wynik.setGeometry(230, 60, 200, 100)
        self.wynik.setFont(QFont('Arial', 16))

        self.waluta = QLabel(self)
        self.waluta.setGeometry(330, 60, 90, 100)
        self.waluta.setFont(QFont('Arial', 16))

        self.tabela = QTableWidget(self)
        self.tabela.setGeometry(420, 10, 320, 340)
        self.tabela.setColumnCount(4)
        self.tabela.setColumnWidth(0, 100)
        self.tabela.setColumnWidth(1, 70)
        self.tabela.setColumnWidth(2, 70)
        self.tabela.setColumnWidth(3, 70)
        self.tabela.setHorizontalHeaderLabels(("Zamiana", "Kurs", "Ilość", "Wartość"))
        self.tabela.verticalHeader().hide()
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        wb = load_workbook('Kantor.xlsx')

        sheet = wb['Arkusz1']
        for i in range(1, 30):
            Zamiana = sheet.cell(row=i, column=1).value
            Kurs = sheet.cell(row=i, column=2).value
            Ilosc = sheet.cell(row=i, column=3).value
            Wartosc = sheet.cell(row=i, column=4).value
            if Zamiana == None:
                break
            else:
                obecny_rząd = self.tabela.rowCount()
                self.tabela.insertRow(obecny_rząd)
                self.tabela.setItem(obecny_rząd, 0, QTableWidgetItem(Zamiana))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(Kurs))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(Ilosc))
                self.tabela.setItem(obecny_rząd, 3, QTableWidgetItem(Wartosc))

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
        eursl = bs.find(id='eursell')
        euro_sell = eursl.getText()
        usdsl = bs.find(id='usdsell')
        usd_sell = usdsl.getText()
        chfsl = bs.find(id='chfsell')
        chf_sell = chfsl.getText()
        gbpsl = bs.find(id='gbpsell')
        gbp_sell = gbpsl.getText()

        obecny_rząd = self.tabela.rowCount()
        self.tabela.insertRow(obecny_rząd)
        plneur = "PLN->EUR"
        plnusd = "PLN->USD"
        plnchf = "PLN->CHF"
        plngbp = "PLN->GBP"
        eurpln = "EUR->PLN"
        usdpln = "USD->PLN"
        chfpln = "CHF->PLN"
        gbppln = "GBP->PLN"

        wb = openpyxl.load_workbook('Kantor.xlsx')
        sheet = wb.active
        sheet.title = 'Arkusz1'

        try:

            pln_euro = self.lista1.currentRow() == 0 and self.lista2.currentRow() == 0
            pln_dolar = self.lista1.currentRow() == 0 and self.lista2.currentRow() == 1
            pln_szwajcar = self.lista1.currentRow() == 0 and self.lista2.currentRow() == 2
            pln_bryt = self.lista1.currentRow() == 0 and self.lista2.currentRow() == 3
            euro_pln = self.lista1.currentRow() == 1 and self.lista2.currentRow() == 0
            dolar_pln = self.lista1.currentRow() == 1 and self.lista2.currentRow() == 1
            szwajcar_pln = self.lista1.currentRow() == 1 and self.lista2.currentRow() == 2
            bryt_pln = self.lista1.currentRow() == 1 and self.lista2.currentRow() == 3
            wejscie = float(self.pole_tekst.text())
            pleu = float(euro_kup)
            plus = float(usd_kup)
            plch = float(chf_kup)
            plgb = float(gbp_kup)
            eupl = float(euro_sell)
            uspl = float(usd_sell)
            chpl = float(chf_sell)
            gbpl = float(gbp_sell)
            przel = ""

            if pln_euro and nadawca.text() == "&Przelicz":
                przel = wejscie / pleu
                wwynik = round(przel, 2)
                self.tabela.setItem(obecny_rząd, 0, QTableWidgetItem(plneur))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(euro_kup))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(self.pole_tekst.text()))
                sheet.append([plneur, euro_kup, self.pole_tekst.text(), str(wwynik)])
                self.waluta.setText('EUR')

            elif pln_dolar and nadawca.text() == "&Przelicz":
                przel = wejscie / plus
                wwynik = round(przel, 2)
                self.tabela.setItem(obecny_rząd, 0, QTableWidgetItem(plnusd))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(usd_kup))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(self.pole_tekst.text()))
                sheet.append([plnusd, usd_kup, self.pole_tekst.text(), str(wwynik)])
                self.waluta.setText('USD')

            elif pln_szwajcar and nadawca.text() == "&Przelicz":
                przel = wejscie / plch
                wwynik = round(przel, 2)
                self.tabela.setItem(obecny_rząd, 0, QTableWidgetItem(plnchf))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(chf_kup))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(self.pole_tekst.text()))
                sheet.append([plnchf, chf_kup, self.pole_tekst.text(), str(wwynik)])
                self.waluta.setText('CHF')

            elif pln_bryt and nadawca.text() == "&Przelicz":
                przel = wejscie / plgb
                wwynik = round(przel, 2)
                self.tabela.setItem(obecny_rząd, 0, QTableWidgetItem(plngbp))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(gbp_kup))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(self.pole_tekst.text()))
                sheet.append([plngbp, gbp_kup, self.pole_tekst.text(), str(wwynik)])
                self.waluta.setText('GBP')

            elif euro_pln and nadawca.text() == "&Przelicz":
                przel = wejscie * eupl
                wwynik = round(przel, 2)
                self.tabela.setItem(obecny_rząd, 0, QTableWidgetItem(eurpln))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(euro_sell))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(self.pole_tekst.text()))
                sheet.append([eurpln, euro_sell, self.pole_tekst.text(), str(wwynik)])
                self.waluta.setText('PLN')

            elif dolar_pln and nadawca.text() == "&Przelicz":
                przel = wejscie * uspl
                wwynik = round(przel, 2)
                self.tabela.setItem(obecny_rząd, 0, QTableWidgetItem(usdpln))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(usd_sell))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(self.pole_tekst.text()))
                sheet.append([usdpln, usd_sell, self.pole_tekst.text(), str(wwynik)])
                self.waluta.setText('PLN')

            elif szwajcar_pln and nadawca.text() == "&Przelicz":
                przel = wejscie * chpl
                wwynik = round(przel, 2)
                self.tabela.setItem(obecny_rząd, 0, QTableWidgetItem(chfpln))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(chf_sell))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(self.pole_tekst.text()))
                sheet.append([chfpln, chf_sell, self.pole_tekst.text(), str(wwynik)])
                self.waluta.setText('PLN')

            elif bryt_pln and nadawca.text() == "&Przelicz":
                przel = wejscie * gbpl
                wwynik = round(przel, 2)
                self.tabela.setItem(obecny_rząd, 0, QTableWidgetItem(gbppln))
                self.tabela.setItem(obecny_rząd, 1, QTableWidgetItem(gbp_sell))
                self.tabela.setItem(obecny_rząd, 2, QTableWidgetItem(self.pole_tekst.text()))
                sheet.append([gbppln, gbp_sell, self.pole_tekst.text(), str(wwynik)])
                self.waluta.setText('PLN')

            else:
                QMessageBox.critical(
                    self, "Błąd", "Nie wybrano waluty!")
                return

            self.wynik.setText(str(wwynik))
            self.tabela.setItem(obecny_rząd, 3, QTableWidgetItem(self.wynik.text()))
            wb.save('Kantor.xlsx')

        except ValueError:
            QMessageBox.warning(self, "Błąd", "Coś poszło nie tak...", QMessageBox.Ok)


class Aktualnosci(QWidget):
    def __init__(self):
        html = urlopen('https://www.pb.pl/puls-inwestora/waluty/')
        bs = BeautifulSoup(html.read(), 'html.parser')
        tytul = bs.find_all('h2')

        super(Aktualnosci, self).__init__()
        self.setGeometry(500, 500, 740, 320)
        self.setWindowTitle("Aktualnosci")

        self.podglad = QTextEdit(self)
        self.podglad.setGeometry(10, 10, 440, 230)
        self.podglad.setReadOnly(True)

        self.przycisk = QPushButton(self)
        self.przycisk.setGeometry(10, 250, 720, 50)
        self.przycisk.setText("&Przejdź do pełnego artykułu")
        self.przycisk.clicked.connect(self.przycisnij)

        self.lista = QListWidget(self)
        self.lista.setGeometry(470, 30, 260, 190)
        self.lista.setCurrentRow(0)
        self.lista.itemDoubleClicked.connect(self.artykul)

        for x in tytul:
            self.lista.addItem(x.get_text())
        self.lista.setRowHidden(15, True)
        self.lista.setRowHidden(16, True)
        self.lista.setRowHidden(17, True)

    @pyqtSlot()
    def przycisnij(self):
        nadawca = self.sender()
        html = urlopen('https://www.pb.pl/puls-inwestora/waluty/')
        bs = BeautifulSoup(html.read(), 'html.parser')
        linki = []
        for link in bs.find_all('a'):
            linki.append(link.get('href'))

        for x in range(0,15):
            if self.lista.currentRow() == x and nadawca.text() == "&Przejdź do pełnego artykułu":
                artlink = ("https://pb.pl" + linki[x + 97])
                webbrowser.open_new_tab(artlink)

    @pyqtSlot()
    def artykul(self):
        html = urlopen('https://www.pb.pl/puls-inwestora/waluty/')
        bs = BeautifulSoup(html.read(), 'html.parser')
        podglad = bs.find_all('p')

        for x in range(0, 15):
            if self.lista.currentRow() == x:
                self.podglad.setText(podglad[x].get_text())

class Aktualny_kurs(QWidget):
    def __init__(self):
        super(Aktualny_kurs, self).__init__()
        self.setGeometry(500, 500, 480, 150)
        self.setWindowTitle("Aktualny kurs")

        self.tabela = QTableWidget(self)
        self.tabela.setRowCount(4)
        self.tabela.setColumnCount(3)
        self.tabela.setColumnWidth(0, 120)
        self.tabela.setGeometry(0, 0, 380, 150)
        self.tabela.setHorizontalHeaderLabels(("Waluta", "Kupno", "Sprzedaż"))
        self.tabela.verticalHeader().hide()
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela.setItem(0, 0, QTableWidgetItem("Euro"))
        self.tabela.setItem(1, 0, QTableWidgetItem("Dolar Amerykański"))
        self.tabela.setItem(2, 0, QTableWidgetItem("Funt Szwajcarski"))
        self.tabela.setItem(3, 0, QTableWidgetItem("Funt Brytyjski"))

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
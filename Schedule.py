#!/usr/bin/env python3
# coding=utf-8

import math
import sys
import re
import requests, bs4

from PyQt5 import QtCore, QtWidgets, uic, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

day=['']

class Main(QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('uis/schedule.ui', self)
        self.setWindowIcon(QtGui.QIcon('images/logo2.png'))

        self.setWindowTitle('Расписание занятий студента ПГУ')

        self.btn_solve.clicked.connect(self.solve)

        self.btn_exit.clicked.connect(self.exit)
        self.checkBox.stateChanged.connect(self.state_changed)

        if day is not None:
            self.label_selected.setText('День недели: ' + day[0])
        self.comboBox.activated.connect(self.handleActivated)

    def handleActivated(self, index):
        day[0] = self.comboBox.itemText(index)
        self.label_selected.setText('День недели: ' + day[0])


    def state_changed(self, state):
        if self.checkBox.isChecked():
            self.label_selected.setText('День недели: '+'Все')
            self.comboBox.setEnabled(False)
        else:
            self.label_selected.setText('День недели: ')
            self.comboBox.setEnabled(True)

    def solve(self):
        if self.checkBox.isChecked():
            a = self.lineEdit.text()
            b = self.lineEdit_2.text()
            session = requests.Session()
            params = {
                'user': a,
                'password': b,
                'delivery_key': ''
            }
            s = session.post('http://psu.kz/student_cabinet/?lang=rus&mod=rasp', params)
            b = bs4.BeautifulSoup(s.text, "html.parser")

            try:
                while (self.tableWidget.rowCount() > 0):
                    self.tableWidget.removeRow(0)

                weekDay = 4
                while (weekDay >= 0):

                    if weekDay == 3 or weekDay == 1:
                        p = b.select('.text .table .odd')
                        i = 0
                        Pary2 = ''
                        while i < len(p):
                            Pary = p[i].getText()
                            Pary2 += Pary
                            i += 1
                        resultDays24 = re.split("Четверг", Pary2)
                        if weekDay == 1:
                            self.tableWidget.insertRow(0)
                            self.tableWidget.setItem(0, 0, QTableWidgetItem('Среда'))
                            j = 0
                        else:
                            self.tableWidget.insertRow(0)
                            self.tableWidget.setItem(0, 0, QTableWidgetItem('Пятница'))
                            j = 1
                        result = re.findall(r'\d{2}:\d{2}-\d{2}:\d{2}', resultDays24[j])
                        name = re.findall(r'[\/,.()\sА-Яа-я]+-+[\d,.\sА-Яа-я]+', resultDays24[j])
                        i = 0
                        while i < len(result):
                            try:
                                self.tableWidget.insertRow(i)
                                self.tableWidget.setItem(i, 0, QTableWidgetItem(result[i]))
                                self.tableWidget.setItem(i, 1, QTableWidgetItem(name[i]))
                            except Exception:
                                self.tableWidget.setItem(i, 0, QTableWidgetItem(''))
                                self.tableWidget.setItem(i, 1, QTableWidgetItem(''))
                            i += 1
                    else:
                        p = b.select('.text .table .even')
                        i = 0
                        Pary2 = ''
                        while i < len(p):
                            Pary = p[i].getText()
                            Pary2 += Pary
                            i += 1
                        resultDays135 = re.split("Среда", Pary2)
                        resultDays35 = re.split("Пятница", resultDays135[1])

                        if weekDay == 0:
                            self.tableWidget.insertRow(0)
                            self.tableWidget.setItem(0, 0, QTableWidgetItem('Вторник'))
                            j = 0
                        else:
                            j = 1
                            if weekDay == 2:
                                self.tableWidget.insertRow(0)
                                self.tableWidget.setItem(0, 0, QTableWidgetItem('Четверг'))
                                resultDays135[1] = resultDays35[0]
                            else:
                                resultDays135[1] = resultDays35[1]
                        result = re.findall(r'\d{2}:\d{2}-\d{2}:\d{2}', resultDays135[j])
                        name = re.findall(r'[\/,.()\sА-Яа-я]+-+[\d,.\sА-Яа-я]+', resultDays135[j])
                        i = 0
                        while i < len(result) and i < len(name):
                            try:
                                self.tableWidget.insertRow(i)
                                self.tableWidget.setItem(i, 0, QTableWidgetItem(result[i]))
                                self.tableWidget.setItem(i, 1, QTableWidgetItem(name[i]))
                            except Exception:
                                self.tableWidget.setItem(i, 0, QTableWidgetItem(''))
                                self.tableWidget.setItem(i, 1, QTableWidgetItem(''))
                            i += 1

                    self.label_error.setText('')
                    weekDay -= 1

                self.tableWidget.insertRow(0)
                self.tableWidget.setItem(0, 0, QTableWidgetItem('Понедельник'))
            except Exception:
                self.label_error.setText('Введены некорректные данные!')
        else:
            a = self.lineEdit.text()
            b = self.lineEdit_2.text()
            session = requests.Session()
            params = {
                'user': a,
                'password': b,
                'delivery_key': ''
            }
            s = session.post('http://psu.kz/student_cabinet/?lang=rus&mod=rasp', params)
            b = bs4.BeautifulSoup(s.text, "html.parser")

            try:
                while (self.tableWidget.rowCount() > 0):
                        self.tableWidget.removeRow(0)

                if day[0] == 'Четверг' or day[0] == 'Вторник':
                    p = b.select('.text .table .odd')
                    i = 0
                    Pary2 = ''
                    while i < len(p):
                        Pary = p[i].getText()
                        Pary2 += Pary
                        i += 1
                    resultDays24 = re.split("Четверг", Pary2)
                    if day[0]=='Вторник':
                        j=0
                    else:
                        j=1
                    result = re.findall(r'\d{2}:\d{2}-\d{2}:\d{2}', resultDays24[j])
                    name = re.findall(r'[\/,.()\sА-Яа-я]+-+[\d,.\sА-Яа-я]+', resultDays24[j])
                    i=0
                    while i < len(result):
                        try:
                            self.tableWidget.insertRow(i)
                            self.tableWidget.setItem(i, 0,QTableWidgetItem(result[i]))
                            self.tableWidget.setItem(i, 1, QTableWidgetItem(name[i]))
                        except Exception:
                            self.tableWidget.setItem(i, 0, QTableWidgetItem(''))
                            self.tableWidget.setItem(i, 1, QTableWidgetItem(''))
                        i += 1
                else:
                    p = b.select('.text .table .even')
                    i = 0
                    Pary2 = ''
                    while i < len(p):
                        Pary = p[i].getText()
                        Pary2 += Pary
                        i += 1
                    resultDays135 = re.split("Среда", Pary2)
                    resultDays35=re.split("Пятница", resultDays135[1])

                    if day[0]=='Понедельник':
                        j=0
                    else:
                        j=1
                        if day[0]=='Среда':
                            resultDays135[1] = resultDays35[0]
                        else:
                            resultDays135[1] = resultDays35[1]
                    result = re.findall(r'\d{2}:\d{2}-\d{2}:\d{2}', resultDays135[j])
                    name=re.findall(r'[\/,.()\sА-Яа-я]+-+[\d,.\sА-Яа-я]+', resultDays135[j])
                    i = 0
                    while i < len(result) and i< len(name):
                        try:
                            self.tableWidget.insertRow(i)
                            self.tableWidget.setItem(i, 0, QTableWidgetItem(result[i]))
                            self.tableWidget.setItem(i, 1, QTableWidgetItem(name[i]))
                        except Exception:
                            self.tableWidget.setItem(i, 0, QTableWidgetItem(''))
                            self.tableWidget.setItem(i, 1, QTableWidgetItem(''))
                        i += 1


                self.label_error.setText('')
            except Exception:
                self.label_error.setText('Введены некорректные данные!')


    def exit(self):
        self.close()



def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

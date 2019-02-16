#!/usr/bin/env python3
# coding=utf-8

import re
import sys
import requests, bs4
import os
import lxml.html as html

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


rubrika=['']
result=['']
NumWithBlog=[]
BlogName=[]
save=['']

class Main(QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('uis/blog.ui', self)

        self.setWindowTitle('Новостной портал')
        self.setWindowIcon(QtGui.QIcon('images/logo1.png'))

        self.btn_upload_data.clicked.connect(self.upload_data_from_file)
        self.btn_save_data.clicked.connect(self.save_data_in_file)
        self.btn_save_all.clicked.connect(self.save_all_in_file)
        self.tableWidget.itemClicked.connect(self.tab_item_one_click_event)

        if rubrika is not None:
            self.label_selected.setText('Рубрика: ' + rubrika[0])

        self.comboBox.activated.connect(self.handleActivated)

    def handleActivated(self, index):
        rubrika[0] = self.comboBox.itemText(index)
        self.label_selected.setText('Рубрика: ' + rubrika[0])

    def tab_item_one_click_event(self):
        row = self.tableWidget.currentItem().row()
        save[0]=str(row+1)
        self.label_selected.setText('Выбранная статья: '+ str(row+1))



    def upload_data_from_file(self):

        s = requests.get('https://www.liveinternet.ru/users/irina_n_ball/rubric/3214521/')
        b = bs4.BeautifulSoup(s.text, "html.parser")

        headings=[]

        metki=b.find('h3', {'class': 'sorted'})
        rubrik=metki.find_next('h3', {'class': 'sorted'})
        link000=rubrik.find_next('a')
        link002=link000
        i=0
        while i<34:
            link001=link002.find_next('a')
            headings.append(link001)
            link002=link001
            i+=1
        i=0
        while i<len(headings)-1:
            if rubrika[0]==headings[i].getText():
                break
            i+=1


        s = requests.get(headings[i].get('href'))
        b = bs4.BeautifulSoup(s.text, "html.parser")
        p = b.find_all('h1', {'class': 'ZAG'})

        i = 0
        while i < len(p):
            table=self.tableWidget
            if p[i].getText()!='Дневник':
                table.insertRow(0)
                table.setItem(0, 0, QTableWidgetItem(p[i].getText()))
                BlogName.append(p[i].getText())
                aclass=p[i].find('a')
                NumWithBlog.append(aclass.get('href'))
                descript=p[i].find_next('p')
                descriptSpace=(descript.getText()).strip()
                while descriptSpace=='':
                    descript = descript.find_next('p')
                    descriptSpace = (descript.getText()).strip()
                table.setItem(0, 1, QTableWidgetItem(descriptSpace))
            i+=1


    def save_data_in_file(self):
        """
        сохраняем данные в выбранным нами файл
        :return:
        """

        number = save[0]
        #path_to_file = QFileDialog.getSaveFileName(self, 'Сохранить', '', "Hyper Text Markup Language File (*.html)")[0]
        if result is not None:
            try:
                BlogName[-int(number)] = re.sub('[<>:"|?]', '', BlogName[-int(number)])

                if len(BlogName[len(BlogName) - int(number)])<250:
                    file = open(BlogName[-int(number)].split('.')[0] + '.html', 'w')
                else:
                    file = open(BlogName[-int(number)][0:249].split('.')[0] + '.html', 'w')


                s = requests.get(NumWithBlog[len(NumWithBlog)-int(number)])
                b = bs4.BeautifulSoup(s.text, "html.parser")

                p = b.find('h1', {'class': 'ZAG'})
                content = b.find_all('p')
                file.write(str(p))

                i = 0
                while i < len(content):
                    file.write(str(content[i]))
                    i += 1
                file.close()
                QMessageBox.about(self, "Успех", "Файл сохранён")
            except:
                path_to_file = QFileDialog.getSaveFileName(self, 'Сохранить', '', "HyperText Markup Language (*.html)")[0]
                file = open(path_to_file.split(".")[0] + '.html', 'w')
                s = requests.get(NumWithBlog[len(NumWithBlog) - int(number)])
                b = bs4.BeautifulSoup(s.text, "html.parser")

                p = b.find('h1', {'class': 'ZAG'})
                content = b.find_all('p')
                file.write(str(p))

                i = 0
                while i < len(content):
                    file.write(str(content[i]))
                    i += 1
                file.close()



    def save_all_in_file(self):
        """
        сохраняем все данные
        :return:
        """

        if result is not None:
            k=0
            while k<len(BlogName):
                try:
                    BlogName[k] = re.sub('[<>:"|?]', '', BlogName[k])
                    if len(BlogName[k])<250:
                        file = open(BlogName[k].split('.')[0] + '.html', 'w')
                    else:
                        file = open(BlogName[k][0:249].split('.')[0] + '.html', 'w')

                    s = requests.get(NumWithBlog[k])
                    b = bs4.BeautifulSoup(s.text, "html.parser")

                    p = b.find('h1', {'class': 'ZAG'})
                    content = b.find_all('p')
                    file.write(str(p))

                    i = 0
                    while i < len(content):
                        file.write(str(content[i]))
                        i += 1
                    file.close()
                    k+=1
                except:
                    k+=1
        QMessageBox.about(self, "Успех", "Все файлы сохранены")



def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

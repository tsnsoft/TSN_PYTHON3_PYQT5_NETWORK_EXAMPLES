#!/usr/bin/env python3
# coding=utf-8

import sys
from urllib.parse import quote
from urllib.request import Request, urlopen

import requests
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from bs4 import BeautifulSoup
import time

class Main(QDialog):
    def __init__(self):
        super(Main, self).__init__()
        loadUi('uis/search.ui', self)

        self.setWindowTitle('Search')
        self.search.clicked.connect(self.solve)

    def solve(self):
        self.label_status.setText('Статус :')
        self.res_table.clearContents()
        list_link_g = []
        list_link_y = []
        # url_d = 'https://duckduckgo.com/?q=fhfgh'
        url_g = 'http://www.google.com/search?q={0}'
        url_b = 'https://www.bing.com/search?q={0}'  # &first=2
        url_y = 'https://yandex.kz/search/?lr=162&text={0}'

        temp = self.search_edt.text()
        query_y = temp
        query_b_g = temp
        query_b_g = query_b_g.replace('\t', "+")
        query_y = query_y.replace('\t', '%20')

        # query = self.search_edt.text()
        # Google запрос
        url_g = url_g.format(quote(query_b_g))
        req_g = Request(url_g, headers={'User-Agent': 'Mozilla/5.0'})
        page_g = urlopen(req_g).read()
        soup_g = BeautifulSoup(page_g, "html.parser")

        # Bing запрос
        url_b = url_b.format(quote(query_b_g))
        req_b = Request(url_b, headers={'User-Agent': 'Mozilla/5.0'})
        page_b = urlopen(req_b).read()
        soup_b = BeautifulSoup(page_b, "html.parser")

        # Yandex запрос
        s = requests.Session()
        url_y = url_y.format(quote(query_y))
        page_y = s.get(url_y, cookies={
            'from-my': 'mda=0; yandexuid=1954370241545111369; yandex_gid=163; '
                       'i=uDDqIhu/FPMnnUNg/EvQ/9oMfrPOeAoXodfXeKjVajMZsw4a23Y7xmok+WjQ536vOMRV8xIsT0TbRplxC3ENP0rHvtw'
                       '=; zm=m-white_bender.webp.css-https-www%3Awww_cxOkctYfWEb3eKluFvZhf68Zh90%3Al; '
                       '_ym_wasSynced=%7B%22time%22%3A1545113824915%2C%22params%22%3A%7B%22eu%22%3A0%7D%2C%22bkParams'
                       '%22%3A%7B%7D%7D; _ym_uid=1545113825905238495; _ym_d=1545113825; my=YwA=; _ym_isad=2; '
                       'ys=wprid.1545113763318421-1647820647122897630562833-sas1-0442; '
                       'yp=1552889762.ww.1#1547705761.ygu.1#1860471369.yrts.1545111369#1860471369.yrtsi.1545111369'
                       '#1545200163.yu.1954370241545111369#1547705827.shlos.1#1576649827.p_sw.1545113826#1545718627'
                       '.szm.1:1366x768:1366x657; yabs-frequency=/4/0000000000000000/1awmS2Gp87zEi70aCo71Wt9m93CX/'})

        soup_y = BeautifulSoup(page_y.text, "html.parser")

        names_l_y = soup_y.find_all("div", class_="organic__url-text")
        links_y = soup_y.find_all("a", class_='link link_theme_normal organic__url link_cropped_no i-bem')

        links_g = soup_g.find_all("div", class_="hJND5c")
        names_l_g = soup_g.find_all("h3", class_="r")

        names_l_b = soup_b.find_all("li", class_="b_algo")
        links_b = soup_b.find_all("div", class_="b_caption")

        google_count = min(len(names_l_g), len(links_g))
        yandex_count = min(len(names_l_y), len(links_y))
        bing_count = min(len(names_l_b), len(links_b))
        query_count = min(google_count, bing_count, yandex_count)

        if query_count == 0:
            self.label_status.setText('Статус : Неверный запрос| Яндекс шалит')
        else:
            self.label_status.setText('Статус : Было получено ' + str(query_count) + ' результатов')
        # for i in range(query_count):
        #     list_link_y.append(links_y[i].get('href'))

        for i in range(query_count):
            temp = links_y[i].get('href').replace('https://', "").replace('www.', '')
            if temp[-1] == '/':
                list_link_y.append(links_y[i].get('href').replace('https://', "").replace('www.', '')[:-1])
            else:
                list_link_y.append(links_y[i].get('href').replace('https://', "").replace('www.', ''))

        for i in range(query_count):
            temp = links_g[i].find("cite").text
            if temp[-1] == '/':
                list_link_g.append(links_g[i].find("cite").text.replace('https://', "").replace('www.', '')[:-1])
            else:
                list_link_g.append(links_g[i].find("cite").text.replace('https://', "").replace('www.', ''))

        for i in range(query_count):
            #Google
            self.res_table.setItem(i, 1, QTableWidgetItem(list_link_g[i]))
            self.res_table.setItem(i, 0, QTableWidgetItem(names_l_g[i].find("a").text))
            #Bing
            self.res_table.setItem(i, 3, QTableWidgetItem(links_b[i].find("cite").text.replace('https://', "").replace('www.', '')))
            self.res_table.setItem(i, 2, QTableWidgetItem(names_l_b[i].find("a").text))
            # #Yandex
            self.res_table.setItem(i, 5, QTableWidgetItem(list_link_y[i]))
            self.res_table.setItem(i, 4, QTableWidgetItem(names_l_y[i].text))

        for i in range(query_count):
            if self.res_table.item(i, 1).text() == self.res_table.item(i, 3).text():
                if self.res_table.item(i, 1).text() == self.res_table.item(i, 5).text():
                    self.vyb_table.setItem(i, 0, QTableWidgetItem(list_link_g[i]))

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

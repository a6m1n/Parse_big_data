# -*- coding: utf-8 -*-
import requests
import os
import csv
from bs4 import BeautifulSoup
from multiprocessing import Pool

class Parse:
    link_all_company = []
    content_company=[]
    id=0




    def __init__(self,url):
        self.url=url
        self.s = requests.Session()
        self.data = {'comp_email':'info@hopyardrecycling.com','password': 'Bahatam1!'}
        self.r = self.s.post(self.url, data=self.data)
        self.get_all_links_product(self.r.text.encode('utf-8'))
        # self.give_ten_link_comapny('https://www.pcexporters.com/home/ListCatgoryImporters/36/')
        # self.contact_company()
        self.get_start(self.link_all_company)




    def get_all_links_product(self,html):
        print ('star function get all link product')
        soup = BeautifulSoup(html,'lxml')
        tds = soup.find('ul', class_="nav nav-main").find_all('li')
        links = []
        for td in tds:
            a = td.find('a').get('href')
            links.append(a)
        links= links[2:]
        for link in links:
            self.give_button_link(link)

    def give_button_link(self, url):
        print ('star function give button link')
        r=requests.get(url)
        html=r.text.encode('utf-8')
        soup = BeautifulSoup(html,'lxml')
        button = soup.find_all('a', class_="mb-xs mt-xs mr-xs btn btn-primary")
        list_button = [i.get('href') for i in button[:2]]
        # print ({url:list_button})
        with Pool(40) as p:
            p.map(self.give_ten_link_comapny,list_button)

    def give_ten_link_comapny(self,url):
        print ('star function ten link company')
        # url = 'https://www.pcexporters.com/suppliers-of-security-products'
        r = self.s.get(url)
        html=r.text.encode('utf-8')
        soup = BeautifulSoup(html,'lxml')
        block=soup.find_all('section', class_="panel panel-primary")

        for company in block:
            try:
                link_company=company.find('div',class_="panel-body").find('td', class_="col-md-10").find('a').get('href')
                # print (link_company)
                self.link_all_company.append(link_company)
            except AttributeError:
                continue
        self.next_page(r)



    def next_page(self,r): #give all pages category. example url + /10, url+20.
        print ('star function next page')
        html=r.text.encode('utf-8')
        soup = BeautifulSoup(html,'lxml')
        next_page=soup.find('div',class_="dataTables_paginate paging_bs_normal").find('ul', class_="pagination")
        zalupa=next_page.find('li', class_='active')
        zalupa2 = next_page.find_all('li')[-1]
        if zalupa2 != zalupa:
            page_link=next_page.find_all('li')[-1].find('a').get('href')
            self.give_ten_link_comapny(page_link)

        else:
            print ('page run out')

    def contact_company(self,url):
        print ('star function contact company')
        # url = 'https://www.pcexporters.com/comptraders-usa-los-angeles-16947'
        r = self.s.get(url)
        html=r.text.encode('utf-8')
        soup = BeautifulSoup(html,'lxml')
        contact_us=soup.find('ul', class_='list-unstyled mt-xl pt-md').find_all('a', class_="menu-item")
        for menu_page in contact_us:
            if menu_page.text == 'Contact Us':
                link=menu_page.get('href')
        r = self.s.get(link)
        html=r.text.encode('utf-8')
        soup = BeautifulSoup(html,'lxml')
        table_contact = soup.find('table', class_="table mb-none").find_all('tr')
        # print (table_contact)
        dick={'ID':self.id,'link':link}
        for i in table_contact:
            info_table=i.find('td').text

            try:
                content_table=i.find('b').text
            except AttributeError:
                content_table='Only Premium'
            if content_table==' ':
                continue
            dick[info_table]=content_table

        self.content_company.append(dick)
        # print (self.content_company)

        self.write_csv(self.content_company)


    def write_csv(self, input_string):
        print ('star write csv')
        with open ('test_1.csv', 'w', encoding='utf-8',  newline='') as f:
            writer = csv.writer(f)
            writer.writerow(('ID','link','Contact Person:','Position:','Address:','City:','Country:','Telephone:','Phone/Whatsapp:','Fax','Website','Email','MSN','Yahoo','Skype','Linkdin ID' ))
            need_keys=['ID','link','Contact Person:','Position:','Address:','City:','Country:','Telephone:','Phone/Whatsapp:','Fax','Website','Email','MSN','Yahoo','Skype','Linkdin ID']
            if input_string[self.id].keys() not in need_keys:
                a=need_keys-input_string[self.id].keys()
                for test in a:
                    test_dic={test:'None'}
                    input_string[self.id].update(test_dic)
            for string in input_string:
                writer.writerow((string['ID'],string['link'] ,string['Contact Person:'],string['Position:'],string['Address:'],string['City:'],string['Country:'],string['Telephone:'],string['Phone/Whatsapp:'],string['Fax'],string['Website'],string['Email'],string['MSN'],string['Yahoo'],string['Skype'],string['Linkdin ID']))

        self.id+=1
        f.closed


    def get_start(self,test):
        print ('star function get start')
        for link in test:
            print (link)
            self.contact_company(link)




if __name__ =='__main__':
    a=Parse("https://www.pcexporters.com/user/login")

#настроить мульти процесинг, и запустить в несколько процессов этот скрипт
#сделать чтоб у каждого мульт процесса был свой массив с данными. сделать функцию за классом которая будет получать на вход линк, авторизовать и возвращать массив с сылками, потом будет
# потом будет авторизоваться класс и в классе запускать мульт процессинг и обрабатовать все и чтоб массив с данными был после объявления мульт процесов
#  а не до ибо ошибка слетает

#!/usr/bin/env python
"""
Description goes here
"""
__author__ = "jupp"
__license__ = "Apache 2.0"
__date__ = "06/03/2019"

from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin, urlencode, quote_plus


root_url = "http://www.isaaa.org/gmapprovaldatabase/gmtraitslist/default.asp"

root_page = urlopen(root_url)

root_soup = BeautifulSoup(root_page, 'html.parser')

with open('isaaa.csv', mode='w') as event_file:
    event_writer = csv.writer(event_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for list in root_soup.find('div', attrs={'id' : "contenttext"}).find_all('li'):

        path = list.find('a').get('href').replace(' ', '%20')
        url = urljoin('http://www.isaaa.org',path)
        page = urlopen(url)

        soup = BeautifulSoup(page, 'html.parser')

        crop_name = ""
        crop_org = ""

        trait = soup.find('div', attrs={'id' : 'contenttext'}).find('h1').text.replace('GM Events with ', '')


        for table_rows in soup.find_all('tr'):
            events = {}

            if table_rows.get('class') and "whitetext" in table_rows.get('class')  :
                continue


            if table_rows.get('class') and "smalltext" in table_rows.get('class')  :

                name = table_rows.find_all('td')[0].find_all('strong')[0].find('a').text.rstrip("\n\r")
                code = table_rows.find_all('td')[0].find_all('strong')[1].text.rstrip("\n\r")
                trade_name = table_rows.find_all('td')[1].text.rstrip("\n\r")
                gene = table_rows.find_all('td')[2].text.split("\n\n")[0].strip("\n\r").replace('\n', '').replace('\r', '')

                event_writer.writerow([name, code, trait, crop_name, crop_org, trade_name, gene])


            else:
                crop = table_rows.find('td').find('strong').text
                crop_name, crop_org = crop.split(' - ')






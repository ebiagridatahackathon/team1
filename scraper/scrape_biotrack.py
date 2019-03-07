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
from urllib.parse import quote
import time

base = "https://biotrackproductdatabase.oecd.org"
root_url = base + "/byTrait.aspx?style=print"

root_page = urlopen(root_url)

root_soup = BeautifulSoup(root_page, 'html.parser')

with open('biotrack.csv', mode='w') as event_file:
    event_writer = csv.writer(event_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


    for row in root_soup.find_all('tr', attrs={'class':'ctl00xContentMainxuwgProducts-ic'}):
        for link in row.find_all('a'):

            first, last = link.get('href').split('?id=')
            # 'Product.aspx?id=DAS-24236-5xDAS-21Ø23-5xSYN-IR1Ø2-7xMON-88913-8xDAS-8191Ø-7'
            param = first + '?id='+quote(last)
            url = urljoin(base, param)
            print (url)

            try:
                page = urlopen(url)


                soup = BeautifulSoup(page, 'html.parser')

                crop_name = soup.find('span', attrs={'id' : 'ctl00_ContentMain_lblCommonName'}).text
                crop_org = soup.find('span', attrs={'id' : 'ctl00_ContentMain_lblScientificName'}).text

                all_traits = []
                for trait in soup.find('span', attrs={'id': 'ctl00_ContentMain_lblTraits'}).text.split(','):
                    all_traits.append(trait)

                name = soup.find('span', attrs={'id' : 'ctl00_ContentMain_lblTransEvent'}).text
                trade_name = soup.find('span', attrs={'id' : 'ctl00_ContentMain_lblTradeName'}).text

                code = soup.find('span', attrs={'id' : 'ctl00_ContentMain_lblProductId'}).text

                for gene in soup.find('span', attrs={'id': 'ctl00_ContentMain_lblGenes'}).text.split(","):

                    for trait in all_traits:
                        event_writer.writerow([name, code, trait, crop_name, crop_org, trade_name, gene])
                        event_file.flush()
                time.sleep(3)
            except Exception as ex:
                print ("error accessing " + url)






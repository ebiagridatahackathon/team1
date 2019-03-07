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

base = "https://bch.cbd.int/database/lmo-registry/"
root_url = base

root_page = urlopen(root_url)

root_soup = BeautifulSoup(root_page, 'html.parser')

with open('lmo.csv', mode='w') as event_file:
    event_writer = csv.writer(event_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


    for row in root_soup.find_all('a', attrs={'id':'ctl15_W21723_DRecordID'}):

        url = urljoin(base, row.get('href'))
        print (url)

        try:
            page = urlopen(url)


            soup = BeautifulSoup(page, 'html.parser')

            for id_taxs in soup.find_all('div', attrs={'class' : 'cmsH1'}):
                id_tax = id_taxs.text.strip()
                if len(id_tax.split(' - ')) > 1:
                    code, crop_name = id_tax.split(' - ')

                    crop_org = ""

                    for crops in soup.find_all('div', attrs={'class' : 'cmsBold'}):
                        if len(crops.text.strip().split(' - ')) > 1:
                            crop_org, crop_name = crops.text.strip().split(' - ')

                    all_traits = []

                    for traits in soup.find_all('li', attrs={'class' : 'formElementTermSoftLink'}):
                        all_traits.append(traits.text.strip().split("\n")[0])

                    name = ""
                    trade_name = ""


                    for genes in soup.find_all('table', attrs={'class': 'lmo-transcript-sense'}):

                        block = genes.find('td', attrs={'class' : 'middle'})
                        gene = block.find_all('div')[0].text.strip()
                        # gene_url = urljoin(base, genes.find('a').get('href'))
                        # print(gene_url)
                        # gene_page = urlopen(url)
                        #
                        # gene_soup = BeautifulSoup(gene_page, 'html.parser')
                        #
                        for trait in all_traits:
                            event_writer.writerow([name, code, trait, crop_name, crop_org, trade_name, gene])
                            event_file.flush()



        except Exception as ex:
            print ("error accessing " + url)






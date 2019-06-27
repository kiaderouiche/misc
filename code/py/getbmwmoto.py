#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
This program get complete moto information,
Reférence/Prix/Designation/Vehicule Type
"""
from __future__ import print_function

import pandas as pd
from pandas import ExcelWriter
import numpy as np
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup as Soup
from requests import get

site_link_1 = "https://www.etkbmw.com/bmw/FR/parts/info/{0}"

def makebmwparts(slink, srcfile):
	Model = []
	try:
		df = pd.read_excel(srcfile, dtype={'Référence':str})
		for idx, row in df.iterrows():
			req = get(slink.format(row['Référence']))
			req.encoding = "utf-8"
			page_bs = Soup(req.text, "lxml")
			desc = page_bs.findAll(attrs={"name":"description"})
			print("Référence: {} | Designation: {}".format(row['Référence'], ' '.join(desc[0]['content'].split()[2:-2])))
			# Create a column from the list
			Modeln.append(' '.join(desc[0]['content'].split()[2:-2]))
		df['Modele Moto'] = Model
		df.to_csv('TARIF MDN_-2018_refPrice.csv')
		return df
	except IOError:
		print("Error not possible open {}".format(srcfile))

def statbmwparts():
	""" Une methode pour faire les statistiques descriptive"""
	df = makebmwparts(site_link, srcfile='TARIF COMPANY-YEAR.xlsx')
	count_ref = df['Référence'].count()
	count_desgn = df['Designation'].count()
	count_price = df['Prix en DZ'].count()
	nan_desgn = df.isnull().sum()[2]
	total_desgn = count_desgn - nan_desgn
	
	print('------------------------------------------------------\n')
	print('STATISTIQUE: \n')

	print('LE NOMBRE TOTAL DE REFERENCE: {}'.format(count_ref))
	print('LE NOMBRE TOTAL DE DESIGNATION: {}'.format(total_desgn))
	print('LE NOMBRE TOTAL DE DESIGNATION NON TROUVER: {}'.format(nan_desgn))
	print('LE NOMBRE TOTAL DES PRIX: {}'.format(count_price))
	print(df.describe(include='all'))
	print('\n')

def main():
	statbmwparts()

if __name__ == '__main__':
	main()

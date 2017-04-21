from bs4 import BeautifulSoup
import requests
import csv
totalpricelist = dict()
year = []
for i in range(8):
	year.append(str(2009+i))
months = ['01','02','03','04','05','06','07','08','09','10','11','12']
date = []
totaldate = []
for m in months:
	if m == '01' or m == '03' or m=='05' or m =='07' or m=='08' or m=='10' or m=='12':
		for i in range(31):
			date.append(m+'-'+str(i+1).zfill(2))
	elif m == '02':
		for i in range(28):
			date.append(m+'-'+str(i+1).zfill(2))
	else:
		for i in range(30):
			date.append(m+'-'+str(i+1).zfill(2))
for y in year:
	for d in date:
		totaldate.append(y+'-'+d)
		if d == '02-28' and (y == '2012' or y == '2016'):
			totaldate.append(y+'-'+'02-29')
l = len(totaldate)
for i in range(l):
	if ((i+1)*7-1) > l:
		print "The search stops at"+totaldate[i]
		break
	page = requests.get('https://www.epexspot.com/en/market-data/dayaheadauction/auction-table/'+totaldate[(i+1)*7-1]+'/DE/24')
	#page = requests.get('https://www.epexspot.com/en/market-data/dayaheadauction/auction-table/2009-10-16/DE/24')
	tree = BeautifulSoup(page.content,"lxml")
	price = tree.find_all('td')
	for j in range(len(price)):
		price[j]=str(price[j])
	indices = [k for k,x in enumerate(price) if x == '<td class="title">Volumes (MWh)</td>']
	#indices2 = price.index('<td>37.18</td>')
	ind = indices[2]-7
	#print indices
	#print indices2
	price = price[ind:ind+7]
	c = 0
	for s in price:
		s = str(s)
		s = s[4:-5]
		#print 'data',totaldate[i*7+c]
		#print 'price',s
		totalpricelist[totaldate[i*7+c]] = s
		c = c + 1

with open('dict_DE.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in totalpricelist.items():
       writer.writerow([key, value])

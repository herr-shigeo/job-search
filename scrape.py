#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import sqlite3
import numpy as np
import urllib
import re
import time
from datetime import date
from contextlib import closing
import random
import mechanize
from urllib.parse import urlparse

with closing(sqlite3.connect('job.db')) as conn:
	c = conn.cursor()
	c.execute("select title from titles")
	titles = []
	for row in c.fetchall():
		titles.append(row[0])

base_url = 'https://www.linkedin.com/jobs/search/'

for job_title in titles:
	params = { 'geoId': 101282230, 'keywords': job_title,  'Location': 'Germany' }
	url = base_url + '?' + urllib.parse.urlencode(params)
	print(url)

	for i in range(5):
		op = mechanize.Browser()
		op.set_handle_robots(False)
		op.addheaders = [('User-Agent', "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")]
		j = op.open(url)
		soup = BeautifulSoup(op.response().read(), "html.parser")
		title = soup.find('title')
		print(title)

		results = []
		pattern_str = re.escape('(') + "(\d.*)" + re.escape(' new)')
		p = re.compile(pattern_str)
		match = p.search(str(title))
		if match is None:
			result = 0
		else:
			num_str = match.group(1)
			num_str = num_str.replace(',', '')
			result = int(num_str)
		results.append(result)	
		time.sleep(random.randint(1,5))
	number = int(np.median(results))
	d = date.today().strftime("%Y/%m/%d")

	with closing(sqlite3.connect('job.db')) as conn:
		c = conn.cursor()
		c.execute("insert into posts values('{}', '{}', {})".format(d, job_title, number))
		conn.commit()
	

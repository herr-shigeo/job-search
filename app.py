#!/usr/bin/env python3

import sys
import io
import os
import sqlite3
import json
from bottle import get, route, run, template, request

@route('/', method=['GET','POST'])
def index():
	return template('graph')

@get('/data', method=['GET'])
def data():
	conn = sqlite3.connect('job.db')
	c = conn.cursor()
	c.execute("select title from titles")
	titles = []
	for row in c.fetchall():
		titles.append(row[0])

	series_data = []
	for title in titles:
		query = "select date, number from posts where title='{0}' order by date".format(title)
		c.execute(query)
		data = []
		for row in c.fetchall():
			d = [ row[0], row[1] ]
			data.append(d)
		series_data.append(list(data))

	conn.close()

	return json.dumps([series_data, titles])

run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: itabas <itabas016@gmail.com>

from nntplib import NNTP
from time import strftime, time, localtime
import datetime, io, os, sys

class StringBuilder:
    _file_str = None

    def __init__(self):
         self._file_str = io.StringIO()

    def Append(self, str):
         self._file_str.write(str)

    def __str__(self):
         return self._file_str.getvalue()

week = 7 * 24 * 60 * 60 # Number of seconds in one day

start = localtime(time() - week)
date = strftime('%y%m%d', start)
time = strftime('%H%M%S', start)
full_date = date + time

servername = 'news.aioe.org'
group = 'comp.lang.python.announce'
server = NNTP(servername)

ids = server.newnews(group, datetime.datetime.strptime(full_date, '%y%m%d%H%M%S'))[1]

content = StringBuilder()

content.Append(
'''
<html>
    <head>
        <title>Week's News - Python Announce</title>
    </head>
    <body>
        <h1>Week's News - Python Announce</h1>
''')

content.Append('''
        <ul>
''')

for id in ids:
    article = StringBuilder()
    subject = ''
    publish_time = ''
    head = server.head(id)
    if len(head) < 1: break
    for line in head[1].lines:
        line = line.decode('utf-8')
        if line.lower().startswith('from:'):
            mail_from = line[6:]
        if line.lower().startswith('date:'):
            publish_time = line[6:]
        if line.lower().startswith('subject:'):
            subject = line[9:]
        if line.lower().startswith('organization:'):
            organization = line[14:]
            break
    
    content.Append('            <li><a href="%s.html">%s</a></li>\n' % (datetime.datetime.strptime(publish_time, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y%m%d%H%M'), subject))
    
    body = server.body(id)[1].lines

    article.Append(
'''
<html>
    <head>
        <title>%s</title>
    </head>
    <body>
        <h1>%s</h1>
        <ul>
            <li>from: %s</li>
            <li>organization: %s</li>
            <li>date: %s</li>
        </ul>
        <p>%s</p>
    </body>
<html>
''' % (subject, subject, mail_from, organization, publish_time, body))

    article_file = '%s\\sample\\%s.html' % (sys.path[0], datetime.datetime.strptime(publish_time, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y%m%d%H%M'))
    os.makedirs(os.path.dirname(article_file), exist_ok=True)
    with open(article_file, 'w') as f:
        f.write(article.__str__())

content.Append('''
        </ul>
''')

content.Append('''
    </body>
</html>''')

index_file = '%s\\sample\\index.html' % sys.path[0]
os.makedirs(os.path.dirname(index_file), exist_ok=True)
with open(index_file, 'w') as f:
    f.write(content.__str__())

server.quit()
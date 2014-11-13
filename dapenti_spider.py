# -*- coding: utf-8 -*-
import urllib2
import re
import os
from datetime import datetime

indexReq = urllib2.Request("https://www.dapenti.com/blog/index.asp")

indexResp = urllib2.urlopen(indexReq)

if indexResp.getcode() == 200:
	
	today = datetime.now()
	todayFormat = today.strftime('%Y%m%d')
	print 'Today is', todayFormat

	html = indexResp.read()
	
	reg = r'<a.*(more.asp.*\s)title.*(\xc5\xe7\xcc\xe7\xcd\xbc\xd8\xd4'+todayFormat+').*</a>';	
	result = re.findall(reg, html)
	
	for r in result:
		href = r[0]
		title = r[1]
		
		if os.path.isfile(title + '.html'):
			break
		
		try:
			xileiReq = "https://www.dapenti.com/blog/" + href
			print 'Downling penti blog ', title
			xileiRes = urllib2.urlopen(xileiReq)
			
			if xileiRes.getcode() == 200:
				
				with open(title + '.html', 'w') as xilei:
				
					xiletHtml = xileiRes.read()
					xileiResult = re.findall('<P>.*?</P>', xiletHtml)
					
					if xileiResult:
					
						xilei.write('<html><head><title>' + title + '</title></head><body>')
					
						for i in xileiResult:
							if i.find('src') >= 0:
								i = re.sub(r'<P>.*(src.*?[jpg|gif]").*</P>', r'<P><IMG \1/></P>', i)
							if i.find('href') >= 0:
								i = re.sub(r'<P>.*(href=".*?").*>(.*)</A>.*</P>', r'<P><A \1>\2</A></P>', i)
							
							i = i.replace('<BR>','')
							i = i.replace('<P></P>','')
							i = i.replace('&nbsp;','');
							xilei.write(i + '\n')
							
						
						xilei.write('</body></html>')
					
		except 	urllib2.HTTPError,e:
			print e
		
	
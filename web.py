import socket
import http.client as httplib


class web:

	def isonline(self):
		conn = httplib.HTTPConnection("www.google.com",timeout=5)
		try:
			conn.request("HEAD", "/")
			conn.close()
			return True
		except:
			conn.close()
			return False
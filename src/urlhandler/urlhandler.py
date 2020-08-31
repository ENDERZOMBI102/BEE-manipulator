import socket
from os import system
from sys import argv
from time import sleep
from typing import Tuple

import psutil


def main():

	code: int = 0

	try:
		if len( argv ) < 1:
			print('missing required parameter "url"')
			code = 1
		elif not argv[1].startswith('bm://'):
			print('this is not a BM url, aborting')
			code = 1
		elif '--help' in argv:
			print('BEE Manipulator URL handler')
			print('By ENDERZOMBI102')
			print('usage: urlhandler.exe <URL>')
		elif 'BEE Manipulator' in ( p.name() for p in psutil.process_iter() ):
			# ipc server address
			addr: Tuple[str, int] = ('localhost', 20306)
			# encoded message
			msg: str = argv[1].encode()
			# encoded size
			size = str( len( msg ) ).encode()
			# add 'placeholder' bytes
			header = str( '0' * ( 64 - len( size ) ) + size )
			# create socket
			skt = socket.create_connection( addr )
			# send header
			skt.send( header.encode() )
			# send message
			skt.send( msg )
			# close the socket
			skt.close()
		else:
			system('"BEE Manipulator.exe"')
			sleep(10)
			main()

	except Exception as e:
		print(f'{type(e)} {e}')
		code = 1
	exit(code)


if __name__ == '__main__':
	main()

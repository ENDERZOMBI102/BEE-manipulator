from sys import argv

from requests import post, get

uploadUrl = get('https://api.github.com/repos/ENDERZOMBI102/BEE-manipulator/releases/latest') \
	.json()['upload_url'] \
	.replace('{?name,label}', '')


files = {
	'file': open( '../BEEManipulator.7z', 'rb' )
}


header = {
	'Accept': 'application/vnd.github.v3+json',
	'Content-Length': str( len( files['file'].read() ) ),
	'Authorization': f'token {argv[1]}',  # github token
	'User-Agent': f'ENDERZOMBI102 BEE-manipulator',
}

r = post(f'{uploadUrl}/?name=BEEManipulator.7z,label=BEE%20Manipulator', headers=header, files=files)


print( r )
print( r.json() )

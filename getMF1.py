import requests

# Basic Variables
MIN_RANGE = 22000
MAX_RANGE = 40000
BASE_URL = 'http://B%d.cdn.telefonica.com/%d/%s_SUB.m3u8'
CHANNELS_IDS = ['NICK', 'DSNJR', '40TV', 'DSNYXD', 'COCINA', '24HORAS', 'INVITADO', 'FOX',
				'AXN', 'CLL13', 'TNT', 'FOXCRIME', 'CSMO', 'AXNWHITE', 'PCMDY', 'SYFY', 'TCM',
				'CPLUSLG', 'MOVFUTBOL', 'CPLUSCHP', 'NTLG', 'NATGEOWILD', 'CPLUS1']

# Execution
for channel in CHANNELS_IDS:
	for host_number in range(MIN_RANGE, MAX_RANGE):
		url = BASE_URL % (host_number, host_number, channel)
		try:
			req = requests.get(url, timeout=30)
			if req.status_code == 200 and 'chunklist' not in req.text:
				print '%s: %s' % (channel, url)
				break
		except Exception as e:
			pass

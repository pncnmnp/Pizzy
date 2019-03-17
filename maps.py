import urllib.request
import json

# ENTER YOUR API KEY FILE HERE
filepath = '../api_dis.txt'

def calculate_dist(origin,dest):
	try:
		lines = None
		with open(filepath) as f:
			lines = f.readlines()

		endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
		api_key = lines[0]

		request1 = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='
		request2 = '&destinations='
		request3 = '&key='

		request = request1+origin+request2+dest+request3+api_key

		response = urllib.request.urlopen(request).read()
		directions = json.loads(response)
		return(directions['rows'][0]['elements'][0]['duration']['text'])
	except:
		return "NEED AN API KEY FOR DELIVERY DURATION!"

import cPickle
import httplib
import socket
import classifier

serverIP='10.10.10.1'
serverPort=10000

def send(response):
	pickledResponse = cPickle.dumps(response)
	try:
		conn = httplib.HTTPConnection(serverIP, serverPort)
		headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
		conn.request('POST', '/', 'body=' + pickledResponse, headers)
		response = conn.getresponse()
		conn.close()
	except socket.error:
		print 'socket.error: Could not send response.'
		return
	except httplib.BadStatusLine:
		print 'httplib.BadStatusLine: Could not send response.'
		return

	if response.status!=200 or response.reason!='OK':
		print 'Could not send response.'
		print response.status, response.reason

def receive(path):
	try:
		conn = httplib.HTTPConnection(serverIP, serverPort)
		conn.request('GET', '/' + path)
		response=conn.getresponse()
		pickledData=response.read()
		conn.close()
	except socket.error:
		return None
	except httplib.BadStatusLine:
		return None
	if response.status!=200 or response.reason!='OK':
		return None

	return cPickle.loads(pickledData)

def run():
	quotesVersionNumber=''
	while(True):
		request=receive('queue')
		if request and request['QuotesVersionNumber'] != quotesVersionNumber:
			print "Quotes are stale.  I'm getting a new copy."
			[quotesVersionNumber, quotes]=receive('quotes')

		# if our quotes are still stale, we're just going to drop the request
		if request and request['QuotesVersionNumber'] == quotesVersionNumber:
			print "Processing " + request['Symbol'] + ' for day ' + str(request['Date']) +'.'

			my_classifier=classifier.classifier(request['Symbol'], request['Date'], quotes)
			p=my_classifier.run()

			response = {}
			response['p']=p
			response['QuotesVersionNumber']=request['QuotesVersionNumber']
			response['Symbol']=request['Symbol']
			response['Date']=request['Date']
			send(response)
		else:
			import time
			time.sleep(5)

run()
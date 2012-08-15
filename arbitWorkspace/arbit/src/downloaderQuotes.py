import yahoo.quotes
import nasdaq.symbols.downloader
import sched
import datetime
import time

class downloader:
	schedule = sched.scheduler(time.time, time.sleep)
	
	def __init__(self):
		self.schedule.enterabs(time.time(), 0, self.download, ())
		self.schedule.run()

	def download(self):
		print ('Running quote download at ' + datetime.datetime.today().isoformat())
	
		# Assume the system clock uses NY time.
		today = datetime.date.today()
		tomorrow = today + datetime.timedelta(days=1)
	
		# 3:00am tomorrow
		downloadTime=datetime.time(3,0,0)
		downloadDateTime = datetime.datetime.combine(tomorrow, downloadTime)
		downloadTime = time.mktime(downloadDateTime.timetuple())
	
		print ('Downloading...')
	
		nasdaq.symbols.downloader.run()
		yahoo.quotes.downloadAllQuotes()
		
		# Reschedule the download to run again tomorrow.
		self.schedule.enterabs(downloadTime, 0, self.download, ())
	
		print ('Done with quote download at ' + datetime.datetime.today().isoformat())
		
downloader()
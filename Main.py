#-------------------------------------------------------------------------------------------------------------------------------------
# File: Main.py
# Name: Gabriel Tavares
# Date: 28/08/2017
# Version: 0.1
# Project: Stream Process Mining Framework
#
# Used to test the framework
#-------------------------------------------------------------------------------------------------------------------------------------
from Stream import Stream

# 6 hours = 21600 seconds
# 12 hours = 43200 seconds
# 1 day = 86400 seconds
# 2 days = 172800 seconds
# 4 days = 345600 seconds
# stream = Stream('demo/hospital_converted.csv', 10, 86400)
stream = Stream('demo/demo.csv', 10, 86400)
# stream.printStream()

stream.eventProcessing()
# stream.printProcesses()

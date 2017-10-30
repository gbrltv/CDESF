#-------------------------------------------------------------------------------------------------------------------------------------
# File: Activity.py
# Name: Gabriel Tavares
# Date: 28/08/2017
# Version: 0.1
# Project: Stream Process Mining Framework
#-------------------------------------------------------------------------------------------------------------------------------------

class Activity:
    def __init__(self, name, timestamp):
        self.name = name
        self.timestamp = timestamp

    def getTimestamp(self):
        return self.timestamp

    def getName(self):
        return self.name

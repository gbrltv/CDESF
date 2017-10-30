#-------------------------------------------------------------------------------------------------------------------------------------
# File: Case.py
# Name: Gabriel Tavares
# Date: 28/08/2017
# Version: 0.1
# Project: Stream Process Mining Framework
#-------------------------------------------------------------------------------------------------------------------------------------

from Activity import Activity

class Case():
    def __init__(self, case_id):
        self.id = case_id
        self.activities = []
        self.trace = []
        self.timestamp = []
        self.ewd = -1
        self.twd = -1

    def getId(self):
        return self.id

    # prints the activities and the case trace
    def printActivities(self):
        for activity in self.activities:
            print(activity.name, " ", end="")
        print(self.getTrace(), end="")

    # sets up a new activity, adding its name and timestamp of execution
    def setActivity(self, act_name, act_timestamp):
        activity = Activity(act_name, act_timestamp)
        self.activities.append(activity)

    # appends new activity (already converted) to the trace
    def setTrace(self, act_conv):
        self.trace.append(act_conv)

    def getTrace(self):
        return self.trace

    def lenTrace(self):
        return len(self.trace)

    # appends new activity timestamp
    def setTimestamp(self, act_timestamp):
        self.timestamp.append(act_timestamp)

    def getTimestamp(self):
        return self.timestamp

    def getLastTime(self):
        return self.timestamp[len(self.timestamp)-1]

    # calculates distances
    # def getDistance(self):
    #     print("")

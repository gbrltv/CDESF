from Activity import Activity

class Case():
    def __init__(self, case_id):
        self.id = case_id
        self.activities = []
        self.trace = []
        self.timestamp = []
        self.ewd = -1
        self.twd = -1

    # prints the activities and the case trace
    def printActivities(self):
        for activity in self.activities:
            print(activity.name, " ", end="")
        print(self.trace, end="")

    # sets up a new activity, adding its name and timestamp of execution
    def setActivity(self, act_name, act_timestamp):
        activity = Activity(act_name, act_timestamp)
        self.activities.append(activity)

    def lenTrace(self):
        return len(self.trace)

    def getLastTime(self):
        return self.timestamp[len(self.timestamp)-1]

#-------------------------------------------------------------------------------------------------------------------------------------
# File: Stream.py
# Name: Gabriel Tavares
# Date: 28/08/2017
# Version: 0.1
# Project: Stream Process Mining Framework
#
# Stream recieves a .csv (Comma-separeted values) archive. This archive must contain information about processes.
# The actual code handles a pre determined format.
# Example:
# Case ID	Activity	        Resource	Complete Timestamp	         Variant	      Variant index	    procedure_name
# Case 1	Process Creation	Value 1	    2011/04/13 17:00:58.000	     Variant 352	  352	            Detail_IW-Frozen
# Case 2	release_state	    Value 9	    2011/04/16 12:00:37.000	     Variant 1	      1	                Detail_Frozen-Final_Rel
# Case 3	Process Creation	Value 10	2012/01/24 11:00:41.000	     Variant 64	      64	            Det_xxxx_IW-Frozen
#-------------------------------------------------------------------------------------------------------------------------------------

import pandas as pd
from Process import Process

class Stream:
    # th - time horizon, horizon of processing defined by the user (time in seconds)
    # clum = clusterming object (for example a DBSCAN and its parameters)
    # log = binary parameter related to output plot
    #def __init__(self, path, gp, th, clum, log):
    def __init__(self, path, gp, th):
        self.stream = pd.read_csv(path)
        self.gp = gp
        self.processes = []
        self.th = th

    def printStream(self):
        print(self.stream)

    # printProcesses prints the Process and its respective Cases, Activities and Traces recursively
    def printProcesses(self):
        for process in self.processes:
            print("Process: ", process.name)
            process.printCases()
            print()

    # returns the index of a process in the processes list based on the 'name' parameter
    # 'name' must be a string
    def getProcess(self, name):
        for index, process in enumerate(self.processes):
            if process.name == name:
                return index
        return None

    # sets up a new process, adding the case/activity/trace. If process already exists, the function retrieves it and add the case/activity/trace
    def setProcess(self, name, case_id, act_name, act_timestamp):
        index = self.getProcess(name)
        if index is None:
            process = Process(name, self.gp, self.th)
            process.setCase(case_id, act_name, act_timestamp)
            self.processes.append(process)
        else:
            self.processes[index].setCase(case_id, act_name, act_timestamp)

    # simulates the process arrival by reading the data frame line by line
    def eventProcessing(self):
        for index, event in self.stream.iterrows():
            self.setProcess(event[6], event[0].split(" ")[1], event[1], event[3])
            # if index > 1000:
            #     break
            # if index % 100 == 0:
            #     print(index)

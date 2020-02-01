import pandas as pd
from Process import Process

class Stream:
    def __init__(self, path, gp, th, gen_plot):
        self.stream = pd.read_csv(path)
        self.stream.iloc[:, 1] = self.stream.iloc[:, 1].str.replace(' ', '-')
        self.gp = gp
        self.processes = []
        self.th = th
        self.gen_plot = gen_plot

    def printStream(self):
        print(self.stream)

    def printProcesses(self):
        '''
        Prints the Process and its respective Cases, Activities and Traces recursively
        '''
        for process in self.processes:
            print("Process: ", process.name)
            process.printCases()
            print()

    def getProcess(self, name):
        '''
        Returns the index of a process in the processes list based on the 'name' parameter
        'name' must be a string
        '''
        for index, process in enumerate(self.processes):
            if process.name == name:
                return index
        return None

    def setProcess(self, name, case_id, act_name, act_timestamp):
        '''
        sets up a new process, adding the case/activity/trace. If process already exists, the function retrieves it and add the case/activity/trace
        '''
        index = self.getProcess(name)
        if index is None:
            process = Process(name, self.gp, self.th, self.gen_plot)
            process.setCase(case_id, act_name, act_timestamp)
            self.processes.append(process)
        else:
            self.processes[index].setCase(case_id, act_name, act_timestamp)

    def eventProcessing(self):
        '''
        simulates the process arrival by reading the data frame line by line
        '''
        for index, event in self.stream.iterrows():
            self.setProcess(event[3], event[0], event[1], event[2])

        for process in self.processes:
                process.caseMetrics()

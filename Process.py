from Case import Case
from Histogram import Histogram
from Point import Point
from Plot import Plot
from random import randint
from datetime import datetime as dt
from itertools import chain
import pandas as pd
import math
import csv
import sys

class Process:
    def __init__(self, name, gp, th, gen_plot):
        self.cases = []
        self.name = name
        self.gp = gp
        self.th = th
        self.gen_plot = gen_plot
        self.gpCreation = False
        self.histogram = Histogram()
        self.plot = Plot(name)
        self.gppts = []
        self.pts = []
        self.case_metrics = []
        self.nyquist = gp
        self.check_point = 0
        self.cp_count = 0
        self.cp_cases = 0
        self.event_count = 0

    def getTraceListForGP(self, cid):
        trace_list = []
        for case in self.cases:
            if case.id != cid:
                trace_list.extend(case.trace)
        return trace_list

    def getTimestampListForGP(self, cid):
        timestamp_list = []
        for case in self.cases:
            if case.id != cid:
                timestamp_list.append(case.timestamp)
        return timestamp_list

    def getTraceList(self):
        trace_list = []
        for case in self.cases:
            trace_list.extend(case.trace)
        return trace_list

    def getTimestampList(self):
        timestamp_list = []
        for case in self.cases:
            timestamp_list.append(case.timestamp)
        return timestamp_list

    def printCases(self):
        '''
        Prints the case and recursively prints its Activities and Trace
        '''
        for case in self.cases:
            print("Case", case.id, ": ", end="")
            case.printActivities()
            print()

    def getCase(self, case_id):
        '''
        Returns the index of a case in the cases list based on the 'case_id' parameter
        'case_id' must be an integer
        '''
        for index, case in enumerate(self.cases):
            if case.id == case_id:
                return index
        return None

    def delCases(self):
        a = sorted(self.cases, key=lambda x: x.getLastTime(), reverse=True)
        self.cases = a[:self.nyquist]

    def GPova(self):
        '''
        Grace Period one versus all (ewd, twd) for plotting
        '''
        for case in self.cases:
            self.histogram.histCreation(self.getTraceListForGP(case.id), self.name)
            self.histogram.timeCreation(self.getTimestampListForGP(case.id), self.name)

            ewd = self.histogram.EWD(case.trace)
            twd = self.histogram.TWD(case.timestamp)

            case.ewd = ewd
            case.twd = twd

            self.case_metrics.append([case.id, case.ewd, case.twd,
                                       case.trace, case.timestamp])

            new_p = Point(case.id, ewd + randint(-5,5)/100, twd + randint(-5,5)/100, case.lenTrace(), case.getLastTime(), -1)
            if new_p in self.gppts:
                self.gppts.pop(self.gppts.index(new_p))
            self.gppts.append(new_p)

    def setCase(self, case_id, act_name, act_timestamp):
        '''
        Sets up a new case, adding the activity/trace.
        If case already exists, the function retrieves it and add the activity/trace
        '''
        index = self.getCase(case_id)

        if index == None:
            case = Case(case_id)
            case.setActivity(act_name, act_timestamp)
            case.trace.append(act_name)
            case.timestamp.append(act_timestamp)
            self.cases.append(case)
            self.cp_cases += 1
        else:
            self.cases[index].setActivity(act_name, act_timestamp)
            self.cases[index].trace.append(act_name)
            self.cases[index].timestamp.append(act_timestamp)

        if self.gpCreation:
            '''
            if we are past the grace period, the EWD and TWD are calculated
            '''
            index = self.getCase(case_id)
            ewd = self.histogram.EWD(self.cases[index].trace)
            twd = self.histogram.TWD(self.cases[index].timestamp)

            self.cases[index].ewd = ewd
            self.cases[index].twd = twd

            # saving case metrics
            self.case_metrics.append([self.cases[index].id,
                                       self.cases[index].ewd,
                                       self.cases[index].twd,
                                       self.cases[index].trace,
                                       self.cases[index].timestamp])

            self.event_count += 1
            # point creation with Jitter effect
            new_p = Point(case_id, ewd + randint(-5,5)/100, twd + randint(-5,5)/100, self.cases[index].lenTrace(), self.cases[index].getLastTime(), self.event_count)
            # updating point on list of points
            if new_p in self.pts:
                self.pts.pop(self.pts.index(new_p))
            # if new event is from a GP point after GP, the point is removed from gp
            if new_p in self.gppts:
                self.gppts.pop(self.gppts.index(new_p))
            self.pts.append(new_p)

            if self.gen_plot:
                self.plot.plotFunc(self.gppts, self.pts, self.name, act_name)

            current = dt.strptime(self.cases[index].getLastTime(), "%Y/%m/%d %H:%M:%S.%f")
            if (current - self.check_point).total_seconds() > self.th:
                self.check_point = current
                self.cp_count += 1
                if len(self.cases) > self.nyquist:
                    '''
                    nyquist, release cases, model update
                    '''
                    self.delCases()
                    lenc = len(self.cases)
                    self.nyquist = self.cp_cases*2
                    if self.nyquist < self.gp:
                        self.nyquist = self.gp
                    self.histogram.histCreation(self.getTraceList(), self.name)
                    self.histogram.timeCreation(self.getTimestampList(), self.name)
                self.cp_cases = 0

        if len(self.cases) > self.gp and not self.gpCreation:
            '''
            Checks the GP size, if the number of cases are enough, a histogram is created
            '''
            self.histogram.histCreation(self.getTraceList(), self.name)
            self.histogram.timeCreation(self.getTimestampList(), self.name)
            self.GPova()
            if index is None:
                index = self.getCase(case_id)
            self.check_point = dt.strptime(self.cases[index].getLastTime(), "%Y/%m/%d %H:%M:%S.%f")
            self.gpCreation = True


    def caseMetrics(self):
        '''
        Converts self.case_metrics into a dataframe and saves it.
        '''
        import os
        if not os.path.exists('metrics'):
            try:
                os.makedirs('metrics')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

        df = pd.DataFrame(self.case_metrics, columns=['case_id', 'ewd', 'twd',
                                                        'trace', 'timestamp'])
        df.to_csv(f'metrics/{self.name}_case_metrics.csv', index=False)

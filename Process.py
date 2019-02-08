#-------------------------------------------------------------------------------------------------------------------------------------
# File: Process.py
# Name: Gabriel Tavares
# Date: 28/08/2017
# Version: 0.1
# Project: Stream Process Mining Framework
#-------------------------------------------------------------------------------------------------------------------------------------

from Case import Case
from Histogram import Histogram
from Point import Point
from Plot import Plot
from random import randint
from datetime import datetime as dt
from itertools import chain
import pandas as pd
# import numpy as np
import math
import csv
import sys

class Process:
    def __init__(self, name, gp, th):
        self.cases = []
        self.name = name
        self.gp = gp
        self.act_dic = {}
        self.abc_list = ['a', 'b', 'c', 'd', 'e', 'f',
                         'g', 'h', 'i', 'j', 'k', 'l',
                         'm', 'n', 'o', 'p', 'q', 'r',
                         's', 't', 'u', 'v', 'w', 'x',
                         'y', 'z']
        self.abc_index = 0
        self.gpCreation = False
        self.histogram = Histogram()
        self.th = th
        self.gppts = []
        self.pts = []
        self.plot = Plot(name, gp, th)
        self.check_point = 0
        self.cp_count = 0
        self.nyquist = gp
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

    # prints the case and recursively prints its Activities and Trace
    def printCases(self):
        for case in self.cases:
            print("Case", case.id, ": ", end="")
            case.printActivities()
            print()

    # returns the index of a case in the cases list based on the 'case_id' parameter
    # 'case_id' must be an integer
    def getCase(self, case_id):
        for index, case in enumerate(self.cases):
            if case.id == case_id:
                return index
        return None

    def delCases(self):
        a = sorted(self.cases, key=lambda x: x.getLastTime(), reverse=True)
        self.cases = a[:self.nyquist]


    # Grace Period one versus all (ewd, twd) for plotting
    def GPova(self):
        for case in self.cases:
            self.histogram.histCreation(self.getTraceListForGP(case.id), self.name)
            self.histogram.timeCreation(self.getTimestampListForGP(case.id), self.name)

            ewd = self.histogram.EWD(case.trace)
            twd = self.histogram.TWD(case.timestamp)

            case.ewd = ewd
            case.twd = twd

            new_p = Point(case.id, ewd + randint(-5,5)/100, twd + randint(-5,5)/100, case.lenTrace(), case.getLastTime(), -1)
            if new_p in self.gppts:
                self.gppts.pop(self.gppts.index(new_p))
            self.gppts.append(new_p)

    # sets up a new case, adding the activity/trace. If case already exists, the function retrieves it and add the activity/trace
    def setCase(self, case_id, act_name, act_timestamp):
        index = self.getCase(case_id)
        act_conv = self.convertAct(act_name)

        if index == None:
            case = Case(case_id)
            case.setActivity(act_name, act_timestamp)
            case.trace.append(act_conv)
            case.timestamp.append(act_timestamp)
            self.cases.append(case)
            self.cp_cases += 1
        else:
            self.cases[index].setActivity(act_name, act_timestamp)
            self.cases[index].trace.append(act_conv)
            self.cases[index].timestamp.append(act_timestamp)

        # if we are past the grace period, the EWD and TWD are calculated
        if self.gpCreation:
            index = self.getCase(case_id)
            ewd = self.histogram.EWD(self.cases[index].trace)
            twd = self.histogram.TWD(self.cases[index].timestamp)

            self.cases[index].ewd = ewd
            self.cases[index].twd = twd

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

            # uncomment for plotting
            self.plot.plotFunc(self.gppts, self.pts, self.name, act_name)

            current = dt.strptime(self.cases[index].getLastTime(), "%Y/%m/%d %H:%M:%S.%f")
            if (current - self.check_point).total_seconds() > self.th:
                self.check_point = current
                self.cp_count += 1
                # nyquist, release cases, model update
                if len(self.cases) > self.nyquist:
                    self.delCases()
                    lenc = len(self.cases)
                    self.nyquist = self.cp_cases*2
                    if self.nyquist < self.gp:
                        self.nyquist = self.gp
                    self.histogram.histCreation(self.getTraceList(), self.name)
                    self.histogram.timeCreation(self.getTimestampList(), self.name)
                self.cp_cases = 0


        # checks the grace period size, if the number of cases are enough, a histogram is created
        if len(self.cases) > self.gp and not self.gpCreation:
            self.histogram.histCreation(self.getTraceList(), self.name)
            self.histogram.timeCreation(self.getTimestampList(), self.name)
            self.GPova()
            if index is None:
                index = self.getCase(case_id)
            self.check_point = dt.strptime(self.cases[index].getLastTime(), "%Y/%m/%d %H:%M:%S.%f")
            self.gpCreation = True


    # converts the activity name to a letter that represents it. Each process has its own conversion and it must be the same for every case
    def convertAct(self, act_name):
        if act_name not in self.act_dic:
            self.act_dic[act_name] = self.abc_list[self.abc_index]
            self.abc_index += 1
        return self.act_dic[act_name]

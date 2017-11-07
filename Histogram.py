#-------------------------------------------------------------------------------------------------------------------------------------
# File: Histogram.py
# Name: Gabriel Tavares
# Date: 28/08/2017
# Version: 0.1
# Project: Stream Process Mining Framework
#-------------------------------------------------------------------------------------------------------------------------------------

from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pandas.core.algorithms as algos
from datetime import datetime as dt
# import editdistance

class Histogram:
    def __init__(self):
        self.hist = None
        self.histTime = None

    # recieves a list of timestamps, creates quartiles and place the timestamps into the quartiles (binning)
    def binning(self, times):
        timediffs = []
        first = dt.strptime(times[0], "%Y/%m/%d %H:%M:%S.%f")
        for j in times:
            timediffs.append((dt.strptime(j, "%Y/%m/%d %H:%M:%S.%f")-first).total_seconds())
        dfqs = pd.DataFrame(timediffs,columns=['A'])

        qs = []
        if len(dfqs['A']) == 1:
            qs = [1,0,0,0]
        elif len(dfqs['A']) == 2 and dfqs['A'][0] == 0 and dfqs['A'][1] == 0:
            qs = [2,0,0,0]
        else:
            bins = algos.quantile(np.unique(dfqs['A']), np.linspace(0, 1, 5))
            result = pd.core.reshape.tile._bins_to_cuts(dfqs['A'], bins, include_lowest=True)

            rs = result[0].value_counts()
            for a in rs:
                qs.append(a)

        return qs

    # creates a histogram from a group of traces
    def histCreation(self, traces, name):
        letter_counts = Counter(traces)
        df = pd.DataFrame.from_dict(letter_counts, orient='index')
        df.columns = ['Count']

        self.hist = df.sort_index()
        # self.hist.plot(kind='bar')

        # path = 'histPlot/'+name+'.png'
        # plt.savefig(path)
        # plt.close()

    # creates a histogram from a group of timestampss
    def timeCreation(self, tmsp, name):
        hist = []
        for i in tmsp:
            hist.append(self.binning(i))

        timeDF = pd.DataFrame(hist, columns=['q1','q2','q3','q4'])
        self.histTime = [sum(timeDF['q1']), sum(timeDF['q2']), sum(timeDF['q3']), sum(timeDF['q4'])]

    # EWD calc based on the current trace and the histogram
    def EWD(self, trace):
        histNorm = (self.hist['Count']-min(self.hist['Count']))/(max(self.hist['Count'])-min(self.hist['Count']))
        # print(histNorm)

        hist_str = ''.join(self.hist.index.tolist())
        trace_str = ''.join(trace)
        # print("edit:", editdistance.eval(hist_str, trace_str))

        ewd = 0
        # Cases when an activity appears only in the histogram. The normalized value is added to EWD
        for i in hist_str:
            if i not in trace_str:
                ewd += histNorm[i]

        # Cases when an activity appears only in the trace. A fixed value is added to EWD. The fixed value is 0.5
        for i in trace_str:
            if i not in hist_str:
                ewd += 0.5

        # print('ewd: ', ewd)
        return ewd

    # TWD calc based on the current timestamp and the histogram
    def TWD(self, tmsp, fp = False):
        histTimeNorm = [(i-min(self.histTime))/(max(self.histTime)-min(self.histTime)) for i in self.histTime]
        processBin = self.binning(tmsp)
        if fp == True:
            return processBin
        if processBin[0] == processBin[1] and processBin[0] == processBin[2] and processBin[0] == processBin[3]:
            processBin = [0,0,0,0]
        else:
            processBin = [(i-min(processBin))/(max(processBin)-min(processBin)) for i in processBin]

        twd = sum([abs(processBin[i]-histTimeNorm[i]) for i in range(4)])
        # print('twd: ', twd)
        return twd

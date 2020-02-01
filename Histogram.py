import numpy as np
import pandas as pd
from math import isnan
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime as dt
import pandas.core.algorithms as algos

class Histogram:
    def __init__(self):
        self.hist = None
        self.histTime = None

    def binning(self, times):
        '''
        Recieves a list of timestamps, creates quartiles and place the timestamps into the quartiles (binning)
        '''
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

    def histCreation(self, traces, name):
        '''
        Creates a histogram from a group of traces
        '''
        letter_counts = Counter(traces)
        df = pd.DataFrame.from_dict(letter_counts, orient='index')
        df.columns = ['Count']

        self.hist = df.sort_index()
        # self.hist.plot(kind='bar')
        # path = 'histPlot/'+name+'.png'
        # plt.savefig(path)
        # plt.close()

    def timeCreation(self, tmsp, name):
        '''
        Creates a histogram from a group of timestamps
        '''
        hist = []
        for i in tmsp:
            hist.append(self.binning(i))

        timeDF = pd.DataFrame(hist, columns=['q1','q2','q3','q4'])
        self.histTime = [sum(timeDF['q1']), sum(timeDF['q2']), sum(timeDF['q3']), sum(timeDF['q4'])]

    def EWD(self, trace):
        '''
        EWD calc based on the current trace and the histogram
        '''
        histNorm = (self.hist['Count']-min(self.hist['Count']))/(max(self.hist['Count'])-min(self.hist['Count']))
        for i in range(len(histNorm)):
            if isnan(histNorm[i]):
                histNorm[i] = 0
        hist = self.hist.index.tolist()
        trace_str = ''.join(trace)

        ewd = 0
        # Cases when an activity appears only in the histogram. The normalized value is added to EWD
        for i in hist:
            if i not in trace:
                ewd += histNorm[i]

        # Cases when an activity appears only in the trace. A fixed value is added to EWD. The fixed value is 0.5
        for i in trace:
            if i not in hist:
                ewd += 0.5
                
        return ewd

    def TWD(self, tmsp, fp = False):
        '''
        TWD calc based on the current timestamp and the histogram
        '''
        histTimeNorm = [(i-min(self.histTime))/(max(self.histTime)-min(self.histTime)) for i in self.histTime]
        processBin = self.binning(tmsp)
        if fp == True:
            return processBin
        if processBin[0] == processBin[1] and processBin[0] == processBin[2] and processBin[0] == processBin[3]:
            processBin = [0,0,0,0]
        else:
            processBin = [(i-min(processBin))/(max(processBin)-min(processBin)) for i in processBin]

        twd = sum([abs(processBin[i]-histTimeNorm[i]) for i in range(4)])
        return twd

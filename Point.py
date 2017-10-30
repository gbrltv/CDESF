from datetime import datetime as dt
import math

class Point:
    def __init__(self, case_id, ewd, twd, nevents, last_time, event_count):
        self._case_id = case_id
        self._ewd = ewd
        self._twd = twd
        self._last_time = math.log((dt.strptime(last_time, "%Y/%m/%d %H:%M:%S")-dt(1970,1,1)).total_seconds())
        self._last_time_tsp = dt.strptime(last_time, "%Y/%m/%d %H:%M:%S")
        # self._last_time = last_time
        self._nevents = nevents
        self._event_count = event_count

    def __eq__(self, other):
        return self._case_id == other._case_id

    def __repr__(self):
        return f'Point(case_id={self._case_id}, ewd={self._ewd}, twd={self._twd})'

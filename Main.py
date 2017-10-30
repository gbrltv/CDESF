#-------------------------------------------------------------------------------------------------------------------------------------
# File: Main.py
# Name: Gabriel Tavares
# Date: 28/08/2017
# Version: 0.1
# Project: Stream Process Mining Framework
#
# Used to test the framework
#-------------------------------------------------------------------------------------------------------------------------------------

import pandas as pd
from Stream import Stream

stream = Stream('demo/hospital_converted.csv', 10, 172800)
# stream.printStream()

stream.eventProcessing()
# stream.printProcesses()

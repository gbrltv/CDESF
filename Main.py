#-------------------------------------------------------------------------------------------------------------------------------------
# Stream recieves a .csv (Comma-separeted values) archive. This archive must contain information about processes.
# The actual code handles a pre determined format.
# Example:
# Case ID	Activity	        Complete Timestamp	         process_name
# Case 1	Process Creation	2011/04/13 17:00:58.000	     Detail_IW-Frozen
# Case 2	release_state	    2011/04/16 12:00:37.000	     Detail_Frozen-Final_Rel
# Case 3	Process Creation	2012/01/24 11:00:41.000	     Det_xxxx_IW-Frozen
#-------------------------------------------------------------------------------------------------------------------------------------

from Stream import Stream

GP = 10
TH = 86400
# a True value will trigger plot generation which are saved in the 'plot' folder
gen_plot = False

stream = Stream('demo/demo.csv', GP, TH, gen_plot)
stream.eventProcessing()

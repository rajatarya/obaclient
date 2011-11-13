import Configuration
import UI
from obaclient import obaclient

import threading
import getopt
import Tkinter
from Tkinter import *
import os
if (os.name is "nt"):
	from ttk import *


def main(argv):
            
    # parse args
    opts, args = getopt.getopt(argv, "hb:s:m:t:", ["help", "bus=", "stop=", "min=", "time="])    
    
    saved_config = Configuration.Configuration()
    cfg = saved_config.getConfig()
    busNumber = cfg.busNumber
    stopNumber = cfg.stopNumber
    minutesToStop = cfg.minutesToStop
    timeStart = cfg.timeStart
    
    arg_busNumber = busNumber
    arg_stopNumber = stopNumber
    arg_minutesToStop = minutesToStop
    arg_timeStart = timeStart
    
    # get args
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-b", "--bus"):
            arg_busNumber = arg
        elif opt in ("-s", "--stop"):
            arg_stopNumber = arg
        elif opt in ("-m", "--min"):
            arg_minutesToStop = arg
        elif opt in ("-t", "--time"):
            arg_timeStart = arg
    
    updateCfg = False
    if (busNumber != arg_busNumber):
        cfg.busNumber = arg_busNumber
        updateCfg = True
         
    if (stopNumber != arg_stopNumber):
        cfg.stopNumber = arg_stopNumber
        updateCfg = True
         
    if (minutesToStop != arg_minutesToStop):
        cfg.minutesToStop = arg_minutesToStop
        updateCfg = True
        
    if (timeStart != arg_timeStart):
        cfg.timeStart = arg_timeStart
        updateCfg = True
    
    if (updateCfg is True):
        saved_config.setConfig(cfg)
        saved_config.save()

    newConfigEvent = threading.Event()
    alertCloseEvent = threading.Event()
    snoozeEvent = threading.Event()
    
    # ui windows
    master = Tkinter.Tk()
    master.withdraw()
    
    config = UI.Config(newConfigEvent, master)
    alert = UI.Alert(master, alertCloseEvent, snoozeEvent)
    
    # background thread
    oba = obaclient(newConfigEvent, alert, alertCloseEvent, snoozeEvent)
    oba.start()
    
    # main window
    main = UI.Main(master, config, alert)
    master.mainloop()
    master.quit()
                
def usage():
    print ""
    print "-b : bus number"
    print "-s : stop number"
    print "-m : minutes before bus arrives at stop"
    print "-t : time to start checking for bus arrival at stop (HHMM format)"
    print ""

if __name__ == '__main__':
    # main(sys.argv[1:])
    # main(["--bus=49", "--stop=10911"])
    main(sys.argv[1:])
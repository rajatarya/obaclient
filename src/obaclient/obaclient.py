'''
Created on Feb 21, 2009

@author: Rajat Arya (rajat@rajatarya.com)
'''

from obarestapi import OBARestApi
import Configuration
import threading
import time

class obaclient(threading.Thread):
    
    def __init__(self, newConfigEvent, alert, alertCloseEvent, snoozeEvent):
        threading.Thread.__init__(self, name="Background")
        self.oba = OBARestApi()
        self.newConfigEvent = newConfigEvent
        self.alert = alert
        self.daemon = True
        self.closeEvent = alertCloseEvent
        self.snoozeEvent = snoozeEvent
        
    def run(self):
        
        # now sleep until timeStart
        savedConfig = Configuration.Configuration()
        cfg = savedConfig.getConfig()
        busNumber = cfg.busNumber
        stopNumber = cfg.stopNumber
        minutesToStop = cfg.minutesToStop
        timeStart = cfg.timeStart
                
        # wait until newConfigEvent set OR numSecondsToSleep is called
        numSecondsToSleep = int(self.secondsFromNow(timeStart))
        print "Sleeping for %d seconds before looking for bus." % numSecondsToSleep
        
        # loop until user clicks 'ok' on alert dialog
        while(True):
            if (self.newConfigEvent.wait(numSecondsToSleep) == True):
                self.newConfigEvent.clear()
                # new configuration set!
                savedConfig = Configuration.Configuration()
                cfg = savedConfig.getConfig()
                busNumber = cfg.busNumber
                stopNumber = cfg.stopNumber
                minutesToStop = cfg.minutesToStop
                timeStart = cfg.timeStart
                numSecondsToSleep = int(self.secondsFromNow(timeStart))
                if (numSecondsToSleep > 60): numSecondsToSleep -= 60 # take off a minute since busses move around
                print "new configuration set, now sleeping %d before looking for bus." % numSecondsToSleep
                continue
            else:
                numSecondsToSleep = 30
            
            result, secsLeft = self.check(busNumber, stopNumber, minutesToStop)
            if (result == False):
                if (secsLeft == 0):
                    # means no bus in next 30m, so break out
                    numSecondsToSleep = 300 # 5m
                elif (secsLeft < (int(minutesToStop)*60)):
                    print "Since already missed current bus, %d < %d" % (secsLeft, (int(minutesToStop)*60))
                    # if already missed the current bus then just sleep until this one passes before checking again
                    numSecondsToSleep = secsLeft - 60 # try one minute before since busses move around in timing
                print "Sleeping %d seconds before checking again" % numSecondsToSleep
            else:
                # means time to show the alert
                message = "Bus %s will arrive at stop %s in {time}." % (busNumber, stopNumber) 
                self.alert.setFields(message, secsLeft)
                print self.alert.get_message()
                self.alert.show()
                self.closeEvent.wait()
                self.closeEvent.clear()
                if (self.snoozeEvent.is_set()):
                    snoozeTime = self.alert.secondsToBus - 60 # start checking again 1m before current bus arrives
                    self.snoozeEvent.clear()
                    print "Sleeping for %d seconds before checking again." % snoozeTime
                    numSecondsToSleep = snoozeTime
                else:
                    # user pressed Ok on Alert window
                    tStart = timeStart
                    if (tStart == ''):
                        tStart = time.strftime('%H%M')
                        # sleep until the next day until at least minutesToStop+2m, meaning a few minutes before this alarm went off
                        numSecondsToSleep = self.secondsFromNow(tStart) - ((int(minutesToStop)+2)*60)
                    else:
                        numSecondsToSleep = self.secondsFromNow(tStart)
                    print "Sleeping until start time tomorrow, %d seconds." % numSecondsToSleep
            
        # all done, return
        print "Exiting Background thread since user closed Alert window"

    def check(self, busNumber, stopNumber, minutesToStop): 
        secs = self.oba.secondsToNextBus(busNumber, stopNumber)
        print "bus: %s, stop: %s, minutesToStop: %s, received: %s" % (busNumber, stopNumber, minutesToStop, secs)
        if (secs.isdigit()):
            seconds = int(secs)
            notice = int(minutesToStop)*60
            if (seconds > 0 and (abs(seconds-notice) <= 60)):
                print "Time to show the alert."
                return True, seconds
            
            print "not quite time yet, got: %d minutes left till the bus" % (seconds/60)
            return False, seconds
        
        else:
            message = "Bus %s is not scheduled to stop at stop %s in the next 30 minutes." % (busNumber, stopNumber)
            print message
            return False, 0
            
    def secondsFromNow(self, timeStart):
        from datetime import datetime, date, timedelta
        
        if (timeStart == "" or timeStart == None):
            return 0
        
        now = datetime.now()
        tStart = datetime.strptime(timeStart, "%H%M")
        today = date.today()
        dtoday = datetime.combine(today, tStart.time())
        
        if (dtoday < now):
            # move date to next day since looking in the past
            day = timedelta(days=1)
            dtoday = day + dtoday
        
        numSecondsFromNow = (dtoday - now).total_seconds()
        numSecondsFromNow -= 60
        if (numSecondsFromNow < 0):
            numSecondsFromNow = 0        
        return numSecondsFromNow

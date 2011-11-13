'''
Created on July 10, 2010

Author: Rajat Arya (rajat@rajatarya.com)
'''

import datetime
import Configuration

class OBARestApi:

    def __init__(self):
        """Initialize the REST API module"""
        savedConfig = Configuration.Configuration()
        cfg = savedConfig.getConfig()
        self.api_key = cfg.api_key

    def secondsToNextBus(self, busNumber, stopNumber):
        
        bus = str(busNumber)
        stop = str(stopNumber)
        
        if (bus.find("_") != 1):
            if (bus.isdigit()):
                bus = "1_" + bus
            else:
                return "Invalid busNumber Input"
            
        if (stop.find("_") != 1):
            if (stop.isdigit()):
                stop = "1_" + stop
            else:
                return "Invalid stopNumber Input"
                        
        import json
        import urllib2
        
        key = urllib2.quote(self.api_key)
        url = "http://api.onebusaway.org/api/where/arrivals-and-departures-for-stop/" + stop + ".json?key=" + key + "&version=2"
        
        raw = urllib2.urlopen(url)
        js = raw.readlines()
        js_object = json.loads(js[0])
        
        routeShortName = None
        
        #filter it all
        data = js_object['data']
        entry = data['entry']
        arrivalsAndDepartures = entry['arrivalsAndDepartures']
        for item in arrivalsAndDepartures:
            
            routeId = item['routeId']
            
            if (routeId == bus):
                predictedArrivalTime = item['predictedArrivalTime']
                predictedDepartureTime = item['predictedDepartureTime']
                routeShortName = item['routeShortName']
                scheduledArrivalTime = item['scheduledArrivalTime']
                scheduledDepartureTime = item['scheduledDepartureTime']
                secondsToBus = self.getSecondsToBus(predictedArrivalTime, scheduledArrivalTime)
                if (secondsToBus > 0): 
                    break
            
        if (routeShortName == None):
            return "Unable to find a bus for bus number provided at this stop"
        
        return str(secondsToBus)
        
    def getSecondsToBus(self, predictedArrivalTime, scheduledArrivalTime):    
            measureTime = 0
            
            if (predictedArrivalTime > 0):
                measureTime = predictedArrivalTime
            else:
                measureTime = scheduledArrivalTime
            
            now = datetime.datetime.now()
            arrival = datetime.datetime.fromtimestamp(measureTime / 1000)
            # print arrival.ctime()
            arr = arrival - now
            # print arr.total_seconds()
            secondsToBus = int(arr.total_seconds())
            return secondsToBus

           
if __name__ == "__main__":
    busNumber = "49"
    stopNumber = "9140"
    print OBARestApi().minutesToNextBus(busNumber, stopNumber)

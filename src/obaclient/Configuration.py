'''
Created on May 6, 2009

@author: Rajat Arya (rajat@rajatarya.com)
'''

import ConfigParser

class Cfg:
    pass         
        
class Configuration:
    
    def __init__(self):
        """Initialize the Config module"""
        self.config = ConfigParser.ConfigParser()
        self.filename = "config.cfg"
        self.config.add_section('OBAClient')
        self.config.add_section('APIKey')
        
    def getConfig(self):
        """Load Configuration and return configuration"""
        try:
            self.config.read(self.filename)        
            minutesToStop = self.config.get('OBAClient', 'minutesToStop')
            busNumber = self.config.get('OBAClient', 'busNumber')
            stopNumber = self.config.get('OBAClient', 'stopNumber')
            timeStart = self.config.get('OBAClient', 'timeStart')
            api_key = self.config.get('APIKey', 'api_key')

        except ConfigParser.NoOptionError:
            busNumber = ""
            stopNumber = ""
            minutesToStop = ""
            timeStart = ""
            api_key = ""
            
        cfg = Cfg()
        cfg.busNumber = busNumber
        cfg.stopNumber = stopNumber
        cfg.minutesToStop = minutesToStop
        cfg.timeStart = timeStart
        cfg.api_key = api_key
        return cfg

    def setBusNumber(self, value):
        """set bus number configuration"""
        self.config.set('OBAClient', 'busNumber', value)
        
    def setStopNumber(self, value):
        """set stop number configuration"""
        self.config.set('OBAClient', 'stopNumber', value)
        
    def setMinutesToStop(self, value):
        """set minutes to stop configuration"""  
        self.config.set('OBAClient', 'minutesToStop', value)
        
    def setTimeStart(self, value):
        """set time to start checking for bus"""
        self.config.set('OBAClient', 'timeStart', value)

    def setApiKey(self, value):
        """sets the API key to use for calling OneBusAway"""
        self.config.set('APIKey', 'api_key', value)
        
    def setConfig(self, cfg):
        """set configuration, passing in a Cfg object"""
        self.setBusNumber(cfg.busNumber)
        self.setMinutesToStop(cfg.minutesToStop)
        self.setStopNumber(cfg.stopNumber)
        self.setTimeStart(cfg.timeStart)
        self.setApiKey(cfg.api_key)
        
    def save(self):
        """persist/save configuration to file"""
        configfile = open(self.filename, 'wb')
        self.config.write(configfile)

if __name__ == "__main__":
    c = Configuration()
    c.setBusNumber("43")
    c.setStopNumber("10911")
    c.setMinutesToStop("3")
    c.save()
    cfg = c.getConfig()
    print "minutesToStop: " + cfg.minutesToStop + " busNumber: " + cfg.busNumber + " stopNumber: " + cfg.stopNumber + " timeStart: " + cfg.timeStart
    

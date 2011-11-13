obaclient is an intelligent reminder system on your desktop for catching the bus using One Bus Away. 

obaclient is a simple desktop application to help you remember to leave your desk in time to catch your bus.

Tell obaclient:

* your bus
* your bus stop
* how many minutes you need to get to the stop
* when you would like obaclient to start checking for your bus


    …and obaclient will notify you when your bus is that many minutes away from your stop.

---

## Installation / Running

Requirements:

* python 2.7
* python-tk

### Running

1. From src/obaclient simply run:
```
   python main.py
```

---

## Never miss your bus again

obaclient prevents missing the bus you wanted because you forgot to check One Bus Away website or mobile application in time to catch it.  Once obaclient is set up it will start checking for your bus and inform you once your bus is near your stop.  If it takes six minutes for you to get to your bus stop from your desk then tell obaclient that and it will let you know when your bus is around six minutes from your stop.

Once obaclient brings up the notification window you can click:

* '**Ok**' – dismiss the notification and tell obaclient to go to sleep until tomorrow.  This means you don’t have to exit obaclient, it will just go to sleep and start checking for your bus tomorrow at the same starting time.
* '**Snooze**' – dismiss the notification and tell obaclient you want to catch the next bus, so start checking after this bus has passed the stop.

### Why Snooze?
So you can catch the next bus instead of the one obaclient notifies you about.  This is useful if you only need a few more minutes to finish off something before catching the bus.

## How do I set up obaclient?

1. Launch obaclient
1. Click ‘Configure‘ button
1. Fill out five fields:
    1. Bus Number: this is your bus number
    1. Stop Number: this is your stop number.  If you are unfamiliar with your stop number, check One Bus Away (here) to find out how to determine your stop number.
    1. Minutes To Stop: this is the number of minutes you need to get to the stop.  Or put another way, how many minutes before your bus arrives at your stop that you want obaclient to notify you.
    1. Time to Start Checking (HHMM): this is the time you want obaclient to start checking for your bus’ arrival.  The format for this field is hour-hour-minute-minute in 24-hour time.  So 6:00PM would be entered as 1800.  5:45PM would be 1745.  8:15AM would be 0815.  You get the idea.
    1. API Key: this is an API key provided by One Bus Away so obaclient can make requests to get current bus information from One Bus Away. If you do not have one, you can request one from: http://onebusaway.org/p/OneBusAwayApiService.action (emailing contact@onebusaway.org).

---

## How do I catch the next bus?

If you want to be notified the next time your bus is approaching your stop (instead of waiting for a set time to start checking) simply leave the ‘Time to Start’ field blank in the Configure screen.  obaclient will immediately start checking for your bus’ arrival and help you catch the next bus.

## How does obaclient work?

obaclient uses the One Bus Away webservice to find out the arrival time for your bus.  It periodically checks One Bus Away to find out if your bus is arriving.  obaclient is sensitive to making too many requests to the One Bus Away webservice.  obaclient’s information is only as accurate as One Bus Away’s information. For more information on how One Bus Away works, see here: http://onebusaway.org/p/FrequentlyAskedQuestions.action.

## Why doesn’t obaclient notify me at exactly my specified time?

obaclient periodically retrieves bus arrival information from One Bus Away.  This arrival information varies by a minute here or there depending on how long the driver takes at each stop (how many boarding/leaving the bus among other things).  One Bus Away does a good job of updating the arrival times but since they vary the time you are notified within obaclient might be within a sixty seconds of the configured notification time.

## What’s next for obaclient?

* OSX support
* better error messages and configuration interface
* new notification window design
* utilize system tray (or equivalent) instead of main menu window
* what would you like to see, let me know…?


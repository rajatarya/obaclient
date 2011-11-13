'''
Created on May 6, 2009

@author: Rajat Arya (rajat@rajatarya.com)
'''
import os
import Queue
from Tkinter import *
if (os.name is "nt"):
	from ttk import *

def iconPath():
    # icon path
    cur = os.path.abspath(os.path.curdir)

    # file name
    if (os.name is "posix"):
        icon = "obaclient.xbm"
    else:
        icon = "obaclient.ico"
    
    # deployment path
    iconPath = os.path.relpath(cur+"/media/"+icon)
    
    # development path
    if (not os.path.isfile(iconPath)):
        iconPath = cur + "/../../data/media/"+icon
        iconPath = os.path.abspath(iconPath)

    if (os.name is "posix"):
        iconPath = "@" + iconPath

    return iconPath

def center_win(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    return

class Alert():
    
    def __init__(self, parent, closeEvent, snoozeEvent):
        '''set up alert UI'''
        self.message = "bus" 
        self.secondsToBus = 500
        
        self.parent = parent
        self.closeEvent = closeEvent
        self.snoozeEvent = snoozeEvent
        self.window = Toplevel(self.parent)
        self.window.iconbitmap(iconPath())
        self.window.title('Bus Arrival Status')
        root = Frame(self.window)
               
        self.window.geometry('800x480')        
        root.pack(fill=BOTH, padx=4, pady=4, expand=1)

        root.msg = Label(root, text=self.message, anchor=CENTER, justify=CENTER, font="Courier 40 bold", wraplength=792, relief="flat")
        root.msg.pack(anchor=CENTER, expand=YES, fill=BOTH, side=TOP)

        root.buttons = Frame(root)
        root.snooze = Button(root.buttons, text=" Snooze ", command=self.snooze)
        root.ok = Button(root.buttons, text=" OK ", command=self.close)
        root.snooze.pack()
        root.ok.pack()
        root.ok.focus_set()
        root.buttons.pack(anchor=CENTER, side=BOTTOM, padx=4, pady=4)
                
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        if (os.name is "nt"):
            self.window.wm_attributes("-topmost", 1)
        center_win(root.master, 800, 480)
        self.root = root
        self.window.withdraw()
        self.queue = Queue.Queue(maxsize=0)
        self.window.bind("<<Alert_UI_Update>>", self.update_e)
        
    def setFields(self, message, secondsToBus):
        self.message = message
        self.secondsToBus = secondsToBus
    
    def snooze(self):
        self.snoozeEvent.set()
        self.close()
    
    def show(self):
        self.queue.put("show")
        self.window.event_generate('<<Alert_UI_Update>>', when='tail')
        
    def hide(self):
        self.queue.put("hide")
        self.window.event_generate('<<Alert_UI_Update>>', when='tail')

    def startSound(self):
        if (os.name is "nt"):
            import winsound
            winsound.PlaySound('SystemExclamation', winsound.SND_LOOP | winsound.SND_ALIAS |  winsound.SND_ASYNC)
    
    def stopSound(self):        
        if (os.name is "nt"):
            import winsound
            winsound.PlaySound(None, winsound.SND_PURGE)
        
    def load(self):
        self.window.deiconify()
        # Play Windows exit sound.
        self.startSound()
        self.updateID = self.root.after(1000, self.update)
        msg = self.get_message()
        self.root.msg.configure(text=msg)
        self.root.update()
        
    def update_e(self, e):
        while self.queue.qsize():
            try:
                val = self.queue.get()
                if (val is "show"):
                    self.load()
                elif (val is "hide"):
                    self.close()
            except Queue.Empty:
                pass
        
    def update(self):
        self.secondsToBus -= 1
        message = self.get_message()
        self.root.msg.configure(text = message)
        self.root.update()
        self.updateID = self.root.after(1000, self.update)
        
    def get_message(self):
        '''convert message with results and return it formatted'''
        import time
        time_display = time.strftime('%M:%S', time.gmtime(self.secondsToBus))
        msg = self.message
        msg = str(msg).replace("{time}", time_display)
        return msg
    
    def close(self):
        self.stopSound()
        self.window.after_cancel(self.updateID)
        self.window.withdraw()
        self.closeEvent.set()

    def quit(self):
        self.window.unbind("<<Alert_UI_Update>>")

import Configuration
class Config():
    
    fields = ["busNumber", "Bus Number"], ["stopNumber", "Stop Number"], ["minutesToStop", "Minutes To Stop"], ["timeStart", "Start Checking (HHMM)"], ["api_key", "API Key"]
    entries = []
    
    def __init__(self, newConfigEvent, master):
        c = Configuration.Configuration()
        self.cfg = c.getConfig()
        self.saved = False
        self.newConfigEvent = newConfigEvent
        self.master = master
        self.window = None
        
    def save(self):
        """Save/Update configuration"""
        cfg = Configuration.Cfg()
        cfg.busNumber = self.entries[0].get()
        cfg.stopNumber = self.entries[1].get()
        cfg.minutesToStop = self.entries[2].get()
        cfg.timeStart = self.entries[3].get()
        cfg.api_key = self.entries[4].get()
        c = Configuration.Configuration()
        c.setConfig(cfg)
        c.save()
        self.cfg = cfg
        self.saved = True
        self.newConfigEvent.set()
        self.close()
            
    def close(self):
        self.window.destroy()
        self.window = None;
    
    def load(self):
        '''Show the UI window'''
        if (self.window != None):
            self.window.focus_set()
        else:
            self.window = Toplevel(self.master)
            self.window.withdraw()
            self.window.protocol("WM_DELETE_WINDOW", self.close)
            self.window.title('OBA Client Configuration')
            self.window.iconbitmap(iconPath())
            root = Frame(self.window)
            self.root = root
            root.pack(fill=BOTH, padx=4, pady=4)
                        
            Label(root, text="Configuration\n", justify=CENTER, anchor=CENTER).pack(expand=YES, fill=BOTH, side=TOP)
            
            self.entries = []
            for name, field in self.fields:
                row = Frame(root)
                row.pack(side=TOP, fill=X)
                Label(row, width=20, text=field).pack(side=LEFT)
                ent = Entry(row)
                if (getattr(self.cfg, name) != ""):
                    ent.insert(0, getattr(self.cfg, name))
                ent.pack(side=RIGHT, expand=YES, fill=X)
                self.entries.append(ent)
    
            Label(root, text="\n").pack()
        
            save = Button(root, text=" Save ", command=self.save)
            save.focus_set()
            save.pack(side=RIGHT)
            
            center_win(self.window, 400, 240)
            self.window.deiconify()

class Main():
    
    def __init__(self, master, config, alert):
        self.alert = alert
        self.master = Toplevel(master)
        self.master.geometry('300x140')
        f = Frame(self.master)
        f.pack(fill=BOTH, padx=4, pady=4, expand=1)
        Button(f, text="Configure", command=config.load).pack(fill=BOTH, padx=4, pady=4, expand=1)
        Button(f, text="Quit", command=self.close).pack(fill=BOTH, padx=4, pady=4, expand=1)
        f.pack(fill=BOTH, padx=4, pady=4, expand=1)
        self.master.title("OBAClient")
        self.master.iconbitmap(iconPath())
        self.master.deiconify()
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        self.parent = master

    def close(self):
        self.master.destroy()
        self.master.quit()
        
if __name__ == '__main__':
    import Tkinter
    import threading
    master = Tkinter.Tk()
    master.withdraw()
    closeEvent = threading.Event()
    snoozeEvent = threading.Event()
    alert = Alert(master, closeEvent, snoozeEvent)
    alert.load()
    master.mainloop()

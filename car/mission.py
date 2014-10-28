from threading import Thread
import time
#import logging as logr

#logr.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)

class MissionCommandListner(object):

    def __init__(self, hardware):
        
        self.hw = hardware
        self.missionComplete = False
        self.exitFlag = False
        self.hold = False
        
        
    def hold(self):
        self.hold = True
        
    def unHold(self):
        self.hold = False
        
    def hasRequest(self):
        if self.missionComplete == False:
            return True
        else:
            return False
            
    def start(self):
    
        self.th = Thread(target=self.mission1)
        self.th.setDaemon(True)
        self.th.start()
        
    def stop(self):
    
        self.exitFlag = True
            
    def mission1(self):
    
        print "mission1 thread - started"
        time.sleep(1)
        whereToGo = 'forward'
        distMin = 100.0
        cycles = 0                
        
        while cycles < 1000 and self.exitFlag == False:
            if self.hold == True:
                time.sleep(1)
            else:
                if(whereToGo == 'forward'):
                    if((self.hw['fsens'].getReading() >= distMin) or (self.hw['fsens'].getReading() == 'inf')):
                        
                        self.hw['mainEngine'].move(30.0)
                    else:
                        self.hw['mainEngine'].stop()
                        whereToGo = 'backwards'

                    
                if(self.whereToGo == 'backwards' ):
                    if((self.hw['bsens'].getReading() >= distMin) or (self.hw['bsens'].getReading() == 'inf')):
                        
                        self.hw['mainEngine'].move(-30.0)
                    else:
                        
                        self.hw['mainEngine'].stop()
                        whereToGo = 'forward'
                
                time.sleep(0.05)
                cycles += 1
            
        self.missionComplete == True
        print "mission1 thread - stopped"

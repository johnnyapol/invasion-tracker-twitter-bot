'''
Created on May 3, 2016

@author: johnnyapol
'''
import os.path
import sys
from invasion import Invasion
from twitter import Twitter
import time

class InvasionTracker:
    def __init__(self):
        print ("Starting Invasion Tracker Twitter bot!")
        print ("Loading Twitter configuration...")
        self.loadTwitter()
        self.invtracker = Invasion(self.twitt)
        self.invtracker.pulse(shouldParse=False)
        # Pulse every 2 minutes
        self.loop()
        
    def loadTwitter(self):
        if not os.path.isfile("bot.cfg"):
            self.createConfig()
            print ("Saved configuration file as 'bot.cfg'. Please edit the values and restart the bot.")
            sys.exit(0)
        else:
            print ("Loading configuration file 'bot.cfg'")
            self.loadConfig()
                
    def createConfig(self):
        with open("bot.cfg", 'w') as cfg:
            print ("#InvasionTracker Bot Config", file=cfg)
            print ("consumer.key=keyhere", file=cfg)
            print ("consumer.secret=secret", file=cfg)
            print ("access.token=token", file=cfg)
            print ("access.secret=secret", file=cfg)
            
    def loadConfig(self):
        conKey = ""
        conSecret = ""
        accessToken = ""
        accessSecret = ""
        with open("bot.cfg") as file:
            for line in file:
                if line.startswith("#"):
                    continue
                data = line.split('=')
                key = data[0]
                value = data[1]
                
                if key.lower() == "consumer.key":
                    conKey = value
                    continue
                if key.lower() == "consumer.secret":
                    conSecret = value
                    continue
                if key.lower() == "access.token":
                    accessToken = value
                    continue
                if key.lower() == "access.secret":
                    accessSecret = value
                    continue
                print ("Unrecognized configuration option: " + key)
        self.twitt = Twitter(conKey, conSecret, accessToken, accessSecret)       
    
    def loop(self):
        while True:
            time.sleep(60 * self.invtracker.CHECK_FREQUENCY)
            print ("Checking invasions")
            self.invtracker.pulse(shouldParse=True)
            
bot = InvasionTracker()
                
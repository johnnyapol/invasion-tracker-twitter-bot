'''
Created on May 3, 2016

@author: johnnyapol
'''

from urllib.request import urlopen
# Try to import simplejson, otherwise fallback to json
try: 
    import simplejson as json
except ImportError:
    import json
    
class Invasion:
    # Global Vars
    API = "https://www.toontownrewritten.com/api/invasions"
    CHECK_FREQUENCY = 2 # Frequency in minutes
    # Local cache
    updated = -1
    invList = []
    
    def __init__(self, _tweetmgr):
        print ("Init invasion tracker")
        self.tweetmgr = _tweetmgr
    
    def pulse(self, shouldParse=True):
        # Fetch invasion data at API endpoint and parse
        print ("Checking for invasions!")
        apiRequest = urlopen(self.API)
        data = json.load(apiRequest)
        print (data)
        # Don't ignore the errors! We'll pay the price later on
        errorStatus = data['error']
        if not errorStatus == None:
            print ("Failed to fetch invasion data! An error has occurred. " + errorStatus)
            return
        updateTime = data['lastUpdated']
        if not updateTime == self.updated:
            self.updated = updateTime
            if not shouldParse:
                return
            #We have an update!
            self.parse(data)
        else:
            return
        
    def parse(self, invData):
        invData = invData['invasions']
        currentInv = []
        districtList = []      
        for inv in invData:
            print ("Found invasion: " + inv)
            cog = invData[inv]['type']
            cog = cog.replace('\x03', '') # Replace Panda3d's text seperater
            currentInv.append(inv + "=" + cog)
            districtList.append(inv)
        
        for district in self.invList:
            districtList.append(district.split('=')[0])
        
        # Evaluate differences since last fetch
        for district in districtList:
            match1 = False
            match2 = False
            list1Value = ""
            list2Value = ""
            
            for dist1 in self.invList:
                dist = dist1.split('=')
                if dist[0] == district:
                    match1 = True
                    list1Value = dist[1]
            
            for dist2 in currentInv:
                dist = dist2.split('=')
                if dist[0] == district:
                    match2 = True
                    list2Value = dist[1]
            
            # District is present in both cached and updated copy
            if (match1 == True and match2 == True):
                # Check to make sure cogs are same
                if list1Value == list2Value:
                    # No updating needed, list is good
                    continue
                else:
                    # Updating needed, post some tweets
                    self.tweetmgr.postTweet("The " + list1Value + " invasion in " + district + " has ended!")
                    self.tweetmgr.postTweet(list2Value + " have invaded " + district + "!")
                    continue
            # District is present in cached copy but not updated copy, invasion has ended
            if (match1 == True and match2 == False):
                self.tweetmgr.postTweet("The " + list1Value + " invasion in " + district + " has ended!")
                continue
            # District is not present in cached copy but present in updated copy, new invasion has begun!
            if (match1 == False and match2 == True):
                self.tweetmgr.postTweet(list2Value + " have invaded " + district + "!")
                continue
            # District is not in either list, this should never happen!
            if (match1 == False and match2 == False):
                print ("The sky has fallen!")
                continue
            
        # Update district cache
        self.invList = currentInv
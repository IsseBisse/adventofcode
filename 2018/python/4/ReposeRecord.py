from datetime import datetime
from datetime import timedelta
from operator import itemgetter
#from random import shuffle
import numpy as np

def parseFile(filename):
    f = open(filename, "r")

    # Read .txt file and parse into list of strings
    eventList = list()
    for line in f:
        lineSplit = line.split("\n")
        
        if type(lineSplit) == list:
            string = lineSplit[0]
        else:
            string = lineSplit

        event = parseInputString(string)
        #print(string)
        eventList.append(event)

    # Sort input based on date
    eventList = sorted(eventList, key=itemgetter('datetime'))
    '''
    for event in eventList:
        print("Date: " + event["datetime"].strftime("%m-%d %H:%M") + ", Action: " + event["action"])
    '''
    # Group events by date
    dateList = groupEvents(eventList)

    return dateList
    
def parseInputString(string):
    # Split string
    parts = string.split("]")
    
    # Create date time
    datetimeStr = parts[0][1:]
    eventTime = datetime.strptime(datetimeStr, '%Y-%m-%d %H:%M')

    # Create event dict
    event = dict()
    event["datetime"] = eventTime
    event["action"] = parts[1]

    return event

def groupEvents(eventList):
    dateList = list()
    currDate = datetime.now()
    tempDate = []

    for event in eventList:
        eventDate = event["datetime"].date()
        # Correct if guard started shift early
        if event["datetime"].hour == 23:
            eventDate = eventDate + timedelta(days=1)

        # New date
        if eventDate != currDate:
            # Add temp date to list
            if tempDate:
                tempDate["sleeping"] = np.cumsum(tempDate["sleeping"])
                dateList.append(tempDate)

                oldID = tempDate["ID"]

            # Create new
            tempDate = dict()
            currDate = eventDate
            tempDate["date"] = currDate

            # Parse action string to guard ID
            IDstr = event["action"].split("#")
            if IDstr[0] == ' Guard ':
                tempDate["ID"] = [int(s) for s in IDstr[1].split() if s.isdigit()]
                tempDate["ID"] = tempDate["ID"][0]
            else:
                tempDate["ID"] = oldID
            
            tempDate["sleeping"] = [0] * 60

        # Falls asleep or wakes up
        else:
            minMark = event["datetime"].minute

            if event["action"] == " falls asleep":
                tempDate["sleeping"][minMark] = 1
            elif event["action"] == " wakes up":
                tempDate["sleeping"][minMark] = -1

    # Add last tempDate
    tempDate["sleeping"] = np.cumsum(tempDate["sleeping"])
    dateList.append(tempDate)

    return dateList


'''
Part 1
'''
def partOne():
    dateList = parseFile("input.txt")
    #print(dateList)

    '''
    f = open("testInput2.txt", "w")
    for event in input:
        f.write("%s\n" % event)
    f.close()
    '''

    # Print date information
    for date in dateList:
        print("Date: " + date["date"].strftime("%m-%d") + ", ID: %d, Sleeping: " % date["ID"], end='')
        for status in date["sleeping"]:
            print("%d" % status, end='')
            '''
            if status == 1:
                print("#", end='')
            else:
                print(".", end='')
            '''
        print('')

    # Compile guard information
    guards = dict()
    for date in dateList:
        ID = date["ID"]
        if ID in guards.keys():
            guards[ID]["sleeping"] += date["sleeping"]
            guards[ID]["minutesSlept"] += sum(date["sleeping"])
        else:
            guards[ID] = dict()
            guards[ID]["sleeping"] = date["sleeping"]
            guards[ID]["minutesSlept"] = sum(date["sleeping"])
    
    # Print guard information
    for ID, guard in guards.items():
        print("ID: %d" % ID)
        print("Time slept: %d" % guard["minutesSlept"], end='')
        print(", Sleeping: ", end='')
        for status in guard["sleeping"]:
            print("%d" % status, end='')
        print('')
    
    # Find sleepiest guard
    maxTimeSlept = -1
    for ID, guard in guards.items():
        if guard["minutesSlept"] > maxTimeSlept:
            sleepiestGuardID = ID
            maxTimeSlept = guard["minutesSlept"] 

    print('Guard ID: %d' % sleepiestGuardID)
    sleeping = guards[sleepiestGuardID]["sleeping"]
    print('Sleepiests minute: %d' % np.argmax(sleeping))
    print('Answer: %d' % (np.argmax(sleeping) * sleepiestGuardID))

    '''
    for event in eventList:
        print(event["datetime"].strftime("%Y-%m-%d %H:%M") + ": " + event["action"])
    '''


'''
Part 2
'''
def partTwo():
    dateList = parseFile("input.txt")

    # Compile guard information
    guards = dict()
    for date in dateList:
        ID = date["ID"]
        if ID in guards.keys():
            guards[ID]["sleeping"] += date["sleeping"]
            guards[ID]["minutesSlept"] += sum(date["sleeping"])
        else:
            guards[ID] = dict()
            guards[ID]["sleeping"] = date["sleeping"]
            guards[ID]["minutesSlept"] = sum(date["sleeping"])
    
    # Print guard information
    for ID, guard in guards.items():
        print("ID: %d" % ID)
        print("Time slept: %d" % guard["minutesSlept"], end='')
        print(", Sleeping: ", end='')
        for status in guard["sleeping"]:
            print("%d" % status, end='')
        print('')

    # Find sleepiest minute
    sleepiestMinute = -1
    maxTimesSleptOnMinute = -1

    for ID, guard in guards.items():
        guardsMaxTimesSleptOnMinute = np.max(guard["sleeping"])
        guardsSleepiestMinute = np.argmax(guard["sleeping"])

        if guardsMaxTimesSleptOnMinute > maxTimesSleptOnMinute:
            sleepiestGuardID = ID
            sleepiestMinute = guardsSleepiestMinute
            maxTimesSleptOnMinute = guardsMaxTimesSleptOnMinute

    print('')
    print('Guard ID: %d' % sleepiestGuardID)
    print('Sleepiests minute: %d' % sleepiestMinute)
    print('Answer: %d' % (sleepiestMinute * sleepiestGuardID))


'''
Main
'''
if __name__ == '__main__':
    partTwo()

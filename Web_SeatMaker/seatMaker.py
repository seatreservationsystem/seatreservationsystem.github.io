import seat
import svgwrite
import os

# Seat Sizes (change based on webpage scaling) (DONT CHANGE - IT IS HARD CODED IN routes.py)
SIZE_SEAT_WITH_SPACE = 36
SIZE_SEAT = 30

# mapDIR needs to match mDIR in routes
mapDIR = "static/roomMaps/"
csvDIR = "roomTemplates/"

def makeMAPDIR():
    try:
        os.mkdir(mapDIR)
    except FileExistsError:
        pass

def makeCSVDIR():
    try:
        os.mkdir(csvDIR)
    except FileExistsError:
        pass

# Takes array of seats, number of seats, and name of file(appends extensions in function) as parameters
def createCSV(room, roomSize, filename):
    try:
        f = open(csvDIR + filename + ".csv", "w")
        for x in range(roomSize):
            f.write(room[x].label + "," + room[x].occupationStatus + "," + room[x].accomedations + "," + room[x].user + "," + str(room[x].xVal) + "," + str(room[x].yVal))
            f.write("\n")
        f.close()
    except FileExistsError:
        pass

# Same as create, but without newline, as they aren'y stripped when reading in file, so writing back with creat() adds a blank line after every entry
def updateCSV(room, roomSize, filename):
    try:
        f = open(csvDIR + filename + ".csv", "w")
        for x in range(roomSize):
            f.write(room[x].label + "," + room[x].occupationStatus + "," + room[x].accomedations + "," + room[x].user + "," + str(room[x].xVal) + "," + str(room[x].yVal))
        f.close()
    except FileExistsError:
        pass

# Takes filename (appends extention in function) as parameter
def readFile(filename):
    try:
        f = open(csvDIR + filename + ".csv", "r")
        lines = f.readlines()
        f.close()
        return lines
    except:
        print("Could not open file.")
        quit()

# Rebuilds seating array from file contents - takes array of file as parameter
def readRoomFromFile(fileContents):
    roomSize = len(fileContents)
    room = [None] * roomSize

    l = [None] * roomSize

    for i in range(roomSize):
        l[i] = fileContents[i].split(",")

    for j in range(roomSize):
        room[j] = seat.Seat()

        room[j].label = l[j][0]
        room[j].occupationStatus = l[j][1]
        room[j].accomedations = l[j][2]
        room[j].user = l[j][3]
        room[j].xVal = l[j][4]
        room[j].yVal = l[j][5]

    return room

# Generates svg file from room array and filename (appends extension in function)
def drawMap(room, filename):
    roomMap = svgwrite.Drawing(mapDIR + filename + ".svg", profile='tiny')

    xMax = 0
    yMax = 0
    for x in range(len(room)):
        if(room[x].occupationStatus == 'not_occupied'):
            color = "green"
        elif(room[x].occupationStatus == 'unavailable'):
            color = "grey"
        else:
            color = "red"

        # This works, but the auto scaling is weird. After taking the the max vals though, change the 1000's in view box to x/y respectively and add ~50

        # if xMax < room[x].xVal:
        #     xMax = room[x].xVal

        # if yMax < room[x].yVal:
        #     yMax = room[x].yVal

        roomMap.add(roomMap.rect( (room[x].xVal, room[x].yVal), (SIZE_SEAT,SIZE_SEAT), stroke=svgwrite.rgb(0,0,0, '%'), fill=color ))
        roomMap.add(roomMap.text( room[x].label, insert=(int(room[x].xVal) + 2 ,int(room[x].yVal) + 15), fill='black'))
        
    roomMap.viewbox(0,0, 1000, 1000)
    roomMap.save()

# Assigns coordinates to seats based on user input (number of rows) and the room array
def arrange(room, numRows, seatsInRow):
    numSeats = len(room)
    row = [None] * numRows
    seatCount = 0
    while(seatCount != numSeats):
        for i in range(numRows):
            row[i] = int(seatsInRow[i])
            seatCount = seatCount + row[i]
        print("count:",seatCount)
        print("actual:",numSeats)
        if(seatCount != numSeats):
            print("Seats don't add up, please try again.")
            for i in range(numRows):
                row[i] = 0
            seatCount = 0
    xv = 0
    count = 0
    for i in range(len(row)):
        for j in range(row[i]):
            room[count].xVal = xv
            room[count].yVal = i * SIZE_SEAT_WITH_SPACE
            xv = xv + SIZE_SEAT_WITH_SPACE
            count = count + 1
        xv = 0

# For debugging - outputs all fields of each seat in a room to the command line - takes room array as input
def displayResults(room):
    roomSize = len(room)
    print("Results: ")
    for x in range(roomSize):
        print("label: ", room[x].label)
        print("occupation status: ", room[x].occupationStatus)
        print("accomedations: ", room[x].accomedations)
        print("user: ", room[x].user)
        print("location: ", str(room[x].xVal), str(room[x].yVal))
        print("\n")
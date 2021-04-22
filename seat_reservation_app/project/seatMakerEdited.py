import seat
import svgwrite
import os
import mysql.connector

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

#rebuilds seating array from sql table - takes array of file as parameter
def readRoomFromSQL(fileContents):
    roomSize = len(fileContents)
    room = [None] * roomSize  
   
    #empty lists to store tuple values of fileContents
    l = []
    s = []
    a = []
    u = []
    x = []
    y = []

    i = 0
    for label in fileContents:
        l.append(label[0])
        i+=1
    i = 0
    for status in fileContents:
        s.append(status[1])
        i+=1
    i = 0
    for accomodations in fileContents:
        a.append(accomodations[2])
        i+=1
    i = 0
    for user in fileContents:
        u.append(user[3])
        i+=1
    i = 0
    for xpos in fileContents:
        x.append(xpos[4])
        i+=1
    i = 0
    for ypos in fileContents:
        y.append(ypos[5])
        i+=1

    for j in range(roomSize):
        room[j] = seat.Seat()
        #label if offset by 1 because sql does not start at 0
        room[j].label = l[j] - 1
        room[j].occupationStatus = s[j]
        room[j].accomedations = a[j]
        room[j].user = u[j]
        room[j].xVal =  x[j]
        room[j].yVal =  y[j]

    return room

#takes table name as parameter
def readFromSQL(name):
    try:
        mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Final-Passw8rd",
        database = "test" 
        )
        mycursor = mydb.cursor()
        sql = "SELECT * FROM " + name
        mycursor.execute(sql)

        myrows = mycursor.fetchall()
        myresult = list(myrows)
        return myresult
    except:
        print("Error selecting from table " + name)
        pass

#updates one record (label) in the table(name), the column must be specified by field
def updateTableSQL(name, label, field, newVal):
    try:
           mydb = mysql.connector.connect(
               host = "localhost",
               user = "root",
               password = "Final-Passw8rd",
               database = "test" 
           ) 
           mycursor = mydb.cursor()
           #sql = "UPDATE " + name + " SET " + field + " = " + "'"+ newVal + "' WHERE id = '" + (label+1) +"'"
           sql = "UPDATE " + name + " SET " + field + " = %s WHERE id = %s"
           val = (newVal, (label + 1))
           #mycursor.execute(sql)
           mycursor.execute(sql,val)
           mydb.commit()
    except:
        print("Error updating table " + name + " " + field + " with " + newVal)
        pass

#Takes array of seat, number of seats and name of table as parameters
def createClassroomSQL(room, roomSize, name):
    try:
        mydb = mysql.connector.connect(
               host = "localhost",
               user = "root",
               password = "Final-Passw8rd",
               database = "test" 
           ) 

        mycursor = mydb.cursor()
        sql = "CREATE TABLE " + name + " (id INT AUTO_INCREMENT PRIMARY KEY, status VARCHAR(20), accomodations VARCHAR(20), user VARCHAR(20), xpos INT, ypos INT);"
        mycursor.execute(sql)
        try:
            for x in range(roomSize):
                sql = "INSERT INTO " + name + " (status, accomodations, user, xpos, ypos) VALUES(%s, %s, %s, %s, %s)"
                val = (str(room[x].occupationStatus), str(room[x].accomedations), str(room[x].user), int(room[x].xVal), int(room[x].yVal))
                mycursor.execute(sql, val)
                mydb.commit()
        except:
            print("Error inserting into SQL table " + name)
    except:
        print("Error creating SQL table " + name)
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

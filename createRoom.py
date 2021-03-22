# CREATEROOM.PY

# Ethan Payne
# CS 499
# Dr. Crk - SIUE

# NOTES - To be made compatible with website - all input needs to be taken from web input rather than stdin, and all output needs to be directed to webpage, not stdout
# These arrays will be marked with a "--UPDATE--" comment.

import seat
import svgwrite

# Seat Sizes (change based on webpage scaling)
SIZE_SEAT_WITH_SPACE = 36
SIZE_SEAT = 30

# Takes array of seats, number of seats, and name of file(appends extensions in function) as parameters
def writeToFile(room, roomSize, filename):
    try:
        f = open("roomTemplates/" + filename + ".csv", "w")
        for x in range(roomSize):
            f.write(room[x].label + "," + room[x].occupationStatus + "," + room[x].accomedations + "," + room[x].user + "," + str(room[x].xVal) + "," + str(room[x].yVal))
            f.write("\n")
        f.close()
    except FileExistsError:
        pass

# Takes filename (appends extention in function) as parameter
def readFile(filename):
    try:
        f = open("roomTemplates/" + filename + "csv", "r")
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
    roomMap = svgwrite.Drawing("roomMaps/" +filename + ".svg", profile='tiny')

    for x in range(len(room)):
        if(room[x].occupationStatus == 'not_occupied'):
            color = "green"
        elif(room[x].occupationStatus == 'unavailable'):
            color = "grey"
        else:
            color = "red"

        roomMap.add(roomMap.rect( (room[x].xVal, room[x].yVal), (SIZE_SEAT,SIZE_SEAT), stroke=svgwrite.rgb(0,0,0, '%'), fill=color ))
        roomMap.add(roomMap.text( room[x].label, insert=(int(room[x].xVal) + 5,int(room[x].yVal) + 10), fill='black'))
    roomMap.save()

# Assigns coordinates to seats based on user input (number of rows) and the room array
def arrange(room, numRows):
    numSeats = len(room)
    row = [None] * numRows
    seatCount = 0
    while(seatCount != numSeats):
        for i in range(numRows):
            print("Enter # of seats in row ", i," :")
            row[i] = int(input())
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

# Main
def main():
    print("What would you like to do?")

    selection = "-1"
    while(selection != "4"):
        print("1. Create Room")
        print("2. Redraw Room (testing)")
        print("3. Edit Room")
        print("4. Quit")

        selection = str(input())

        if(selection == "1"):
            print("Enter room name: ")
            filename = str(input())

            print("Enter # of seats: ")
            roomSize = int(input())

            print("Enter # of rows: ")
            numRows = int(input())

            room = [None] * roomSize

            # Create room and assign default seat numbers
            for x in range(roomSize):
                room[x] = seat.Seat()
                room[x].label = str(x + 1)

            arrange(room, numRows)

            writeToFile(room, roomSize, filename)

            drawMap(room, filename)

            displayResults(room)

        elif(selection == "2"):
            print("Which room would you like to redraw?")
            selectedRoom = str(input())

            fileContents = readFile(selectedRoom)

            roomFromFile = readRoomFromFile(fileContents)

            drawMap(roomFromFile, selectedRoom)

        elif(selection == "3"):
            print("Which room would you like to edit?")
            selectedRoom = str(input())

            fileContents = readFile(selectedRoom)

            roomFromFile = readRoomFromFile(fileContents)

            action = "-1"
            while(action != "3"):
                print("1. Edit seat")
                print("2. Copy room")
                print("3. Done")

                action = str(input())
                index = -1
                if action == "1":
                    print("Enter seat name: ")
                    seatName = str(input())
                    for i in range(len(roomFromFile)):
                        if roomFromFile[i].label == seatName:
                            index = i
                    if (index != -1):
                        seatAction = "z"
                        while(seatAction != "e"):
                            print("l: change label")
                            print("s: change status")
                            print("a: change accomedations")
                            print("u: change user")
                            print("m: move seat")
                            print("e: exit")
                            seatAction = str(input())
                            if seatAction == "l":
                                print("Enter new label: ")
                                roomFromFile[index].label = str(input())
                                drawMap(roomFromFile, selectedRoom)

                            elif seatAction == "s":
                                print("Enter new status: ")
                                print("1. Occupied")
                                print("2. Not Occupied")
                                print("3. Not available")
                                statusInput = str(input())
                                if statusInput == "1":
                                    updatedStatus = "occupied"
                                elif statusInput == "2":
                                    updatedStatus = "not_occupied"
                                elif statusInput == "3":
                                    updatedStatus = "unavailable"
                                else:
                                    print("Not a valid option. <", statusInput, ">")

                                roomFromFile[index].occupationStatus = updatedStatus
                                drawMap(roomFromFile, selectedRoom)

                            elif seatAction == "a":
                                print("Enter new accomedations: ")
                                roomFromFile[index].accomedations = str(input())
                                drawMap(roomFromFile, selectedRoom)

                            elif seatAction == "u":
                                print("Enter user: ")
                                roomFromFile[index].user = str(input())
                                drawMap(roomFromFile, selectedRoom)

                            elif seatAction == "m":
                                print("Directions: u,d,l,r,uh,dh,lh,rh")
                                print("Enter e when finished.")
                                movementInput = "z"
                                while(movementInput != "e"):
                                    movementInput = str(input())
                                    if(movementInput == "u"):
                                        roomFromFile[index].yVal = int(roomFromFile[index].yVal) - 36
                                        drawMap(roomFromFile, selectedRoom)
                                    elif(movementInput == "d"):
                                        roomFromFile[index].yVal = int(roomFromFile[index].yVal) + 36
                                        drawMap(roomFromFile, selectedRoom)
                                    elif(movementInput == "l"):
                                        roomFromFile[index].xVal = int(roomFromFile[index].xVal) - 36
                                        drawMap(roomFromFile, selectedRoom)
                                    elif(movementInput == "r"):
                                        roomFromFile[index].xVal = int(roomFromFile[index].xVal) + 36
                                        drawMap(roomFromFile, selectedRoom)
                                    elif(movementInput == "uh"):
                                        roomFromFile[index].yVal = int(roomFromFile[index].yVal) - 18
                                        drawMap(roomFromFile, selectedRoom)
                                    elif(movementInput == "dh"):
                                        roomFromFile[index].yVal = int(roomFromFile[index].yVal) + 18
                                        drawMap(roomFromFile, selectedRoom)
                                    elif(movementInput == "lh"):
                                        roomFromFile[index].xVal = int(roomFromFile[index].xVal) - 18
                                        drawMap(roomFromFile, selectedRoom)
                                    elif(movementInput == "rh"):
                                        roomFromFile[index].xVal = int(roomFromFile[index].xVal) + 18
                                        drawMap(roomFromFile, selectedRoom)
                                    elif(movementInput == "e"):
                                        print("Exit.")
                                    else:
                                        print("Not a valid option. <", movementInput, ">")
                                    
                            elif seatAction == "e":
                                print("Exit.")
                            else:
                                print("Not a valid option. <", seatAction, ">")
                    else:
                        print("Seat does not exist.")

                elif action == "2":
                    print("Waiting for DB - while rw to that (probably sql)")

                elif action == "3":
                    print("Done.")

                else:
                    print("Not a valid option. <", action, ">")


        elif(selection == "4"):
            print("Goodbye.")

        else:
            print("Not a valid option. <", selection, ">")

if __name__ == "__main__":
    main()
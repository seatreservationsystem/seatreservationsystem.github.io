# ROUTES.PY

# Ethan Payne
# CS 499
# Dr. Crk - SIUE

from flask import Flask, render_template, request, redirect, url_for
import seatMakerEdited
import seat
import os
import mysql.connector

app = Flask(__name__)

# So images aren't cached
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Should match roomMaps directory in seatMakerEdited.py
mDIR = "static/roomMaps/"

# --- CREATING ---

@app.route("/createRoom/", methods=['post', 'get'])
def createRoom():
    msg = ""
    roomMap = ""

    if request.method == 'POST':
        roomName = request.form.get('roomName')
        numSeats = request.form.get('numSeats')
        numRows = request.form.get("numRows")
        seats = request.form.get("seats")
        seatArr = seats.split(",")

        seatSum = 0
        for i in range(len(seatArr)):
            seatSum += int(seatArr[i])

        # Check that per-row seats equals total seats and builds room
        if len(seatArr) == int(numRows) and seatSum == int(numSeats):
            msg = "Room created with following parameters: " + "Name - " + roomName + " | Seats - " + numSeats + " | Rows - " + numRows
            roomMap = "../" + mDIR + roomName + ".svg"

            room = [None] * int(numSeats)
            
            for x in range(len(room)):
                room[x] = seat.Seat()
                room[x].label = str(x + 1)

            seatMakerEdited.arrange(room, int(numRows), seatArr)
            seatMakerEdited.createClassroomSQL(room, int(numSeats), roomName)
            #seatMaker.createCSV(room, int(numSeats), roomName)
            seatMakerEdited.drawMap(room, roomName)

        else:
            msg = "Something went wrong. Please try again."

    return render_template("createRoom.html", roomMap = roomMap, message = msg)

# --- EDITING ---

@app.route("/editRoom/")
def editRoom():
        return render_template("editRoom.html")

@app.route("/verifyRoom/", methods=['post', 'get'])
def verifyRoom():
    if request.method == 'POST':
        # Check if room exists (current check is to svg file, should probably change)
        name = request.form['name']
        fName = mDIR + name + ".svg"

        # Exists
        if os.path.isfile(fName):
            return redirect(f"/selectedRoom/{name}")
        # Does not exist
        else:
            return redirect(url_for("editRoom"))

@app.route('/selectedRoom/<name>')
def selectedRoom(name):
    roomMap = "../" + mDIR + name + ".svg"
    return render_template("seatSelect.html", name = name, roomMap = roomMap)

@app.route("/<name>/verifySeat/", methods=['post', 'get'])
def verifySeat(name):
    if request.method == 'POST':
        seatNum = request.form['seatNum']
        
        #adding the offset for arrays vs sql tables
        seatNum = seatNum - 1
        
        # Rebuild room
        fContents = seatMakerEdited.readFromSQL(name)
        #fContents = seatMaker.readFile(name)
        roomFromFile = seatMakerEdited.readRoomFromSQL(fContents)
        #roomFromFile = seatMaker.readRoomFromFile(fContents)

        # Verify that seat exists in room
        index = -1
        for i in range(len(roomFromFile)):
            if roomFromFile[i].label == int(seatNum):
                index = i
        # exists
        if index != -1:
            return redirect(f"/{name}/selectedSeat/{seatNum}")
        # does not exist
        else:
            return redirect(f"/selectedRoom/{name}")

@app.route('/<name>/selectedSeat/<seatNum>', methods=['post', 'get'])
def selectedSeat(name, seatNum):

    # Rebuild room
    fContents = seatMakerEdited.readFromSQL(name)
    #fContents = seatMaker.readFile(name)
    roomFromFile = seatMakerEdited.readRoomFromSQL(fContents)
    #roomFromFile = seatMaker.readRoomFromFile(fContents)
    roomSize = len(roomFromFile)

    # Get seat index
    index = int(seatNum) - 1

    # Some funky stuff was happening if the redrawing/rewriting happend once after the conditionals, so each action calls these functions
    if request.method == 'POST':
        # Make not occupied
        if request.form['submit_button'] == 'Not Occupied':
            roomFromFile[index].occupationStatus = "not_occupied"
            seatMakerEdited.updateTableSQL(name, index, "status", roomFromFile[index].occupationStatus)
            #seatMaker.updateCSV(roomFromFile, roomSize, name)
            seatMakerEdited.drawMap(roomFromFile, name)

        # Make occupied
        elif request.form['submit_button'] == 'Occupied':
            roomFromFile[index].occupationStatus = "occupied"
            seatMakerEdited.updateTableSQL(name, index, "status", roomFromFile[index].occupationStatus)
            #seatMaker.updateCSV(roomFromFile, roomSize, name)
            seatMakerEdited.drawMap(roomFromFile, name)

        # Make unavailable
        elif request.form['submit_button'] == 'Unavailable':
            roomFromFile[index].occupationStatus = "unavailable"
            seatMakerEdited.updateTableSQL(name, index, "status", roomFromFile[index].occupationStatus)
            #seatMaker.updateCSV(roomFromFile, roomSize, name)
            seatMakerEdited.drawMap(roomFromFile, name)

        # Move left
        elif request.form['submit_button'] == 'Left':
            roomFromFile[index].xVal = int(roomFromFile[index].xVal) - 36
            seatMakerEdited.updateTableSQL(name, index, "xpos", roomFromFile[index].xVal)
            #seatMaker.updateCSV(roomFromFile, roomSize, name)
            seatMakerEdited.drawMap(roomFromFile, name)

        # Move right
        elif request.form['submit_button'] == 'Right':
            roomFromFile[index].xVal = int(roomFromFile[index].xVal) + 36
            seatMakerEdited.updateTableSQL(name, index, "xpos", roomFromFile[index].xVal)
            #seatMaker.updateCSV(roomFromFile, roomSize, name)
            seatMakerEdited.drawMap(roomFromFile, name)

        # Move up
        elif request.form['submit_button'] == 'Up':
            roomFromFile[index].yVal = int(roomFromFile[index].yVal) - 36
            seatMakerEdited.updateTableSQL(name, index, "ypos", roomFromFile[index].yVal)
            #seatMaker.updateCSV(roomFromFile, roomSize, name)
            seatMakerEdited.drawMap(roomFromFile, name)

        # Move down
        elif request.form['submit_button'] == 'Down':
            roomFromFile[index].yVal = int(roomFromFile[index].yVal) + 36
            seatMakerEdited.updateTableSQL(name, index, "ypos", roomFromFile[index].yVal)
            #seatMaker.updateCSV(roomFromFile, roomSize, name)
            seatMakerEdited.drawMap(roomFromFile, name)

        # Move left half
        elif request.form['submit_button'] == 'Left (Half)':
            roomFromFile[index].xVal = int(roomFromFile[index].xVal) - 18
            seatMakerEdited.updateTableSQL(name, index, "xpos", roomFromFile[index].xVal)
            #seatMaker.updateCSV(roomFromFile, roomSize, name)
            seatMakerEdited.drawMap(roomFromFile, name)

        # Move right half
        elif request.form['submit_button'] == 'Right (Half)':
            roomFromFile[index].xVal = int(roomFromFile[index].xVal) + 18
            seatMakerEdited.updateTableSQL(name, index, "xpos", roomFromFile[index].xVal)
            #seatMaker.updateCSV(roomFromFile, roomSize, name)
            seatMakerEdited.drawMap(roomFromFile, name)

        # Move up half
        elif request.form['submit_button'] == 'Up (Half)':
            roomFromFile[index].yVal = int(roomFromFile[index].yVal) - 18
            seatMakerEdited.updateTableSQL(name, index, "ypos", roomFromFile[index].yVal)
            #seatMaker.updateCSV(roomFromFile, roomSize, name)
            seatMakerEdited.drawMap(roomFromFile, name)

        # Move down half
        elif request.form['submit_button'] == 'Down (Half)':
            roomFromFile[index].yVal = int(roomFromFile[index].yVal) + 18
            seatMakerEdited.updateTableSQL(name, index, "ypos", roomFromFile[index].yVal)
            #seatMaker.updateCSV(roomFromFile, roomSize, name)
            seatMakerEdited.drawMap(roomFromFile, name)

        # Returns to seat selection
        elif request.form['submit_button'] == 'Select New Seat':
            print("this do be pressed")
            return redirect(f"/selectedRoom/{name}")
    
    roomMap = "../../" + mDIR + name + ".svg"
    return render_template("seatMod.html", name = name, seatNum = seatNum, roomMap = roomMap)

# --- MAIN ---

def main():
    # Create .csv and .svg directories
    seatMakerEdited.makeCSVDIR()
    seatMakerEdited.makeMAPDIR()

    app.run(host='localhost', port=5000)

if __name__ == "__main__":
    main()

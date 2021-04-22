
# main.py

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

import seatMakerEdited
import seat
import os
import mysql.connector

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():

    user_type = current_user.user_type
    

    if user_type == True:
        return render_template('instructor_profile.html', name=current_user.name, user_type=current_user.user_type)
    return render_template('student_profile.html', name=current_user.name, user_type=current_user.user_type)


# --- CREATING ---

@main.route("/createRoom/", methods=['post', 'get'])
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

@main.route("/editRoom/")
def editRoom():
        return render_template("editRoom.html")

@main.route("/verifyRoom/", methods=['post', 'get'])
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

@main.route('/selectedRoom/<name>')
def selectedRoom(name):
    roomMap = "../" + mDIR + name + ".svg"
    return render_template("seatSelect.html", name = name, roomMap = roomMap)

@main.route("/<name>/verifySeat/", methods=['post', 'get'])
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

@main.route('/<name>/selectedSeat/<seatNum>', methods=['post', 'get'])
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



# --- STUDENT SELECTION ---

@main.route("/selectStudentRoom/")
def selectStudentRoom():
        return render_template("selectStudentRoom.html")

@main.route("/verifyStudentRoom/", methods=['post', 'get'])
def verifyStudentRoom():
    if request.method == 'POST':

        # Check if room exists (current check is to svg file, should probably change)
        name = request.form['name']
        fName = mDIR + name + ".svg"


# This portion (between comments) SHOULD ONLY BE ALLOWED IF: room is available to student (enrolled in class)


        # Exists
        if os.path.isfile(fName):
            return redirect(f"/studentPickSeat/{name}")

# END if() section

        # Does not exist
        else:
            return redirect(url_for("selectRoom"))

@main.route('/studentPickSeat/<name>', methods=['post', 'get'])
def studentPickSeat(name):
    if request.method == 'POST':
        seatNum = request.form['seatNum']
        studentName = request.form['studentName']

# This portion (between comments) SHOULD ONLY BE ALLOWED IF: student name matches that of signed in user and seat number exists

        # Rebuild room
        fContents = seatMakerEdited.readFromSQL(name)
        #fContents = seatMaker.readFile(name)
        roomFromFile = seatMakerEdited.readRoomFromSQL(fContents)
        #roomFromFile = seatMaker.readRoomFromFile(fContents)
        roomSize = len(roomFromFile)

        # Get seat index
        index = int(seatNum) - 1

        roomFromFile[index].user = studentName
        roomFromFile[index].occupationStatus = "occupied"
        #seatMaker.updateCSV(roomFromFile, roomSize, name)
        seatMakerEdited.updateTableSQL(name, index, "status", roomFromFile[index].occupationStatus)
        seatMakerEdited.updateTableSQL(name, index, "user", roomFromFile[index].user = studentName)
        seatMaker.drawMap(roomFromFile, name)

# END if() section

    roomMap = "../" + mDIR + name + ".svg"
    return render_template("studentSeatAssignment.html", name = name, roomMap = roomMap)

# --- END STUDENT SELECTION ---
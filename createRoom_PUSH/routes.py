from flask import Flask, render_template, request
import seatMaker
import seat
import os

#MAP_FOLDER = os.path.join('static', "/roomMaps")


app = Flask(__name__)
#app.config["UPLOAD_FOLDER"] = MAP_FOLDER

@app.route("/createRoom/", methods=['post', 'get'])
def createRoom():
    msg = ""
    filename = ""
    if request.method == 'POST':
        roomName = request.form.get('roomName')
        numSeats = request.form.get('numSeats')
        numRows = request.form.get("numRows")
        seats = request.form.get("seats")
        seatArr = seats.split(",")

        seatSum = 0
        for i in range(len(seatArr)):
            seatSum += int(seatArr[i])

        if len(seatArr) == int(numRows) and seatSum == int(numSeats):
            msg = roomName + " " + numSeats + " " + numRows + "Written to DB and .csv. Map created."

            room = [None] * int(numSeats)
            
            for x in range(len(room)):
                room[x] = seat.Seat()
                room[x].label = str(x + 1)

            seatMaker.arrange(room, int(numRows), seatArr)
            seatMaker.writeToFile(room, int(numSeats), roomName)
            seatMaker.drawMap(room, roomName)

            #filename = os.path.join(app.config["UPLOAD_FOLDER"], roomName + ".svg")

        else:
            msg = "Something went wrong."

    #return render_template("createRoom.html", message = msg, user_image = "roomMaps/" + filename + ".svg")
    return render_template("createRoom.html", message = msg)

def main():
    seatMaker.makeCSVDIR()
    seatMaker.makeMAPDIR()

    app.run(host='localhost', port=5000)

if __name__ == "__main__":
    main()
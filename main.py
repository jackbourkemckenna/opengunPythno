import numpy as np
import cv2
import imutils
import datetime
import time
import math
import threading
import uuid
#importing my methods
import text as txt
import s3Upload as s3
import socket
import cv2
import pickle
import struct ## new
import zlib
from flask import Flask, render_template, Response


def setup():
    try:
        global gun_cascade, camera, frameRate, property_id, length, firstFrame, framecount,i,increment,start_Time,end_Time,statusCopy,userID,s


        gun_cascade = cv2.CascadeClassifier('cascade.xml')
        #camera = cv2.VideoCapture('gun.mp4')



        firstFrame = None
        count = 0
        gun_exist = False
        increment = 0
        start_Time = 0
        end_Time = 0
        i = 0


    except Exception as e:
        print(e)
        exit(0)
def main():

    setup()
    userID = "3546"
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (320,240))
    data = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))
    while True:
        while len(data) < payload_size:
            print("Recv: {}".format(len(data)))
            data += conn.recv(4096)

        print("Done Recv: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        print("msg_size: {}".format(msg_size))
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)




        framecount =0
        framecount += 1
        #frameId = frame.get(1) #current frame number



        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #gray = cv2.GaussianBlur(gray, (21, 21), 0)

        #gray = cv2.dilate(gray, None, iterations=2)

        #stuff to try in the future
        #scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE, outputRejectLevels = True
        gun = gun_cascade.detectMultiScale(gray, 3,5)

        for (x,y,w,h) in gun:
            randID = uuid.uuid4().hex
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            rects = gun[0]
            neighbours = gun[0]
            weights = gun[0]
            #if (frameId % math.floor(frameRate) == 1):
            #cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 165, 0), 1)

            #cv2.imwrite('bin/' + userID+'-'+randID + '.jpg', frame)
            if userID == "NULL":
                print("failed due to user null")
                break
            print("working on pushing images to s3"+userID)
            #s3.uploadDirectory("bin/", "open-gun-recordings",userID)

            #picURL = "s3bucket.com/users/screenshots/"+userID+'/'+userID+'-'+randID+'.jpg'
            #out.write(frame)

            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', frame)[1].tobytes() + b'\r\n\r\n')

            #txt.fire(picURL)


        #camera = cv2.imdecode(frame, cv2.IMREAD_COLOR)

app = Flask(__name__)
#vc = cv2.VideoCapture(0)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.before_first_request
def opening_socket():
	HOST = ''
	PORT = 8089

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	s.bind((HOST, PORT))

	s.listen(10)

	global conn

	conn, addr = s.accept()

	if conn is None:
		sys.exit('conn is empty')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(main(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True,port=80)

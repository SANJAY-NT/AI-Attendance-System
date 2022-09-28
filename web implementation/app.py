from flask import Flask, render_template, Response
from camera import VideoCamera
import os

# initialize application
app = Flask(__name__)

# homepage of browser
@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame
            + b'\r\n\r\n')

# taking info from the camera
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/remote')
# def attend():
#     with open('Attendance.csv','r+') as f:
#         myDataList = f.readlines()
#         nameList =[]
#         for line in myDataList:
#             entry = line.strip().split(',')
#             nameList.append(entry[0])
#     return render_template('index.html', textlist = str(nameList))

# initialize port address/ adress of website/ run app
if __name__ == '__main__':
    app.run(debug=True)
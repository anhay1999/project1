from flask import Flask, render_template, Response
from camera import Video
import pyrebase

config = {
  "apiKey": "AIzaSyDo5ftCruflFAXEUBaZojPVBT0_EZmIsAg",
  "authDomain": "realtime-firebase-bc740.firebaseapp.com",
  "databaseURL": "https://realtime-firebase-bc740-default-rtdb.firebaseio.com",
  "projectId": "realtime-firebase-bc740",
  "storageBucket": "realtime-firebase-bc740.appspot.com",
  "messagingSenderId": "827190932861",
  "appId": "1:827190932861:web:4c81724a0b15fde916c814",
  "measurementId": "G-7HYHM949E1"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

app = Flask(__name__)
counter = 0


@app.route('/')

def index():
    return render_template('index.html')


def gen(camera):
     while (True):
         frame=camera.get_frame(0)
         yield(b'--frame1\r\n' b'Content-Typ1e:  image1/jpeg1\r\n\r\n' + frame +b'\r\n\r\n')







# @app.route("/listen")
# def listen():
#
#   def respond_to_client(camera):
#     while True:
#       frame = camera.get_frame(1)
#       db.child("fireblood").update({"so_xe": frame})
#       global counter
#       with open("color.txt", "r") as f:
#         color = f.read()
#         print("******************")
#       if(color != "white"):
#         print(counter)
#         # counter += 1
#         counter = frame
#         _data = json.dumps({"color":color, "counter":counter})
#         yield f"id: 1\ndata: {_data}\nevent: online\n\n"
#       time.sleep(0.5)
#   return Response(respond_to_client(Video()), mimetype='text/event-stream')
  # return Response(1,mimetype='text/event-stream')


@app.route('/video')

def video():

    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(debug=True)

##############################
# if __name__ == "__main__":
#   # app.run(port=80, debug=True)
#   http_server = WSGIServer(("localhost", 80), app)
#   http_server.serve_forever()

from flask import Flask, render_template, Response , jsonify
import cv2
# from Model import *

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # use 0 for web camera


#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/fight/',methods= ['GET','POST'])
def main_fight(accuracyfight=0.91):
    # camera1 = cv2.VideoCapture(0)
    vid= video_mamonreader(cv2,camera)
    res_mamon = {}

    # vidl = "{{ url_for('video_feed') }}"
    # print(vidl,'\n')

    # vid1 = video_mamonreader(cv2,vidl)

    datav = np.zeros((1, 30, 160, 160, 3), dtype=np.float)
    datav[0][:][:] = vid
    millis = int(round(time.time() * 1000))
    f , precent = pred_fight(model22,datav,acuracy=0.67)
    res_mamon = {'fight':f , 'precentegeoffight':str(precent)}

    millis2 = int(round(time.time() * 1000))
    res_mamon['processing_time'] =  str(millis2-millis)
    resnd = jsonify(res_mamon)
    resnd.status_code = 200
    return resnd



@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')

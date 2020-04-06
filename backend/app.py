import atexit
from flask import Flask, Response, render_template, request, jsonify, send_from_directory
import cv2
import numpy as np

app = Flask(__name__)

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cam.set(cv2.CAP_PROP_FPS, 5)

lower = np.array([0, 0, 0])
upper = np.array([0, 0, 0])


def exit_handler():
    cam.release()


atexit.register(exit_handler)


def process(frame):
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower, upper)

    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # opencv 3
    # _, contours, _ = cv2.findContours(
    #    mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    return frame


@app.route('/', methods=['GET'])
def main():
    return render_template('app.html')


@app.route('/stream.mjpg', methods=['GET'])
def stream():
    def display():
        while True:
            _, frame = cam.read()
            frame = process(frame)
            _, buf = cv2.imencode('.jpg', frame)
            img = bytes(buf)
            content = (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n'
                       + img +
                       b'\r\n')
            yield content

    return Response(
        display(),
        headers={
            'Age': '0',
            'Cache-Control': 'no-cache, private',
            'Pragma': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        },
        mimetype='application/octet-stream',
        content_type='multipart/x-mixed-replace; boundary=frame',
        direct_passthrough=True
    )

# curl --data '{"h": 30, "s": 50, "l": 50}' -H "Content-Type: application/json" http://localhost:5000/colors/low
@app.route('/colors/low',  methods=['POST'])
def color_low():
    '''
    set the lower color for mask
    '''
    content = request.json
    h, s, v = content["h"], content["s"], content["v"]
    global lower
    lower = np.array([int(h), int(s), int(v)])
    return {'message': 'color.low.set'}, 200, {'Access-Control-Allow-Origin': '*'}

# curl --data '{"h": 90, "s": 255, "l": 255}' -H "Content-Type: application/json" http://localhost:5000/colors/high
@app.route('/colors/high',  methods=['POST'])
def color_high():
    '''
    set the upper color for mask
    '''
    content = request.json
    h, s, v = content["h"], content["s"], content["v"]
    global upper
    upper = np.array([int(h), int(s), int(v)])
    return {'message': 'color.high.set'}, 200, {'Access-Control-Allow-Origin': '*'}


@app.route('/app/<path:path>')
def send_app(path):
    return send_from_directory('app', path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)

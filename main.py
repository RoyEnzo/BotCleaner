"""
AlphaCleaner
"""

__author__ = "Enzo Roy"
__version__ = "1.0.0"
__email__ = "enzo.r@eduge.ch"
__status__ = "Development"

from flask import Flask, Response, render_template, request, jsonify, send_file
from streaming import StreamingOutput
from controller import Controller
from alphabot2 import AlphaBot2
import picamera
import io

# Serveur flask
app = Flask(__name__)

URL_ANALYSE_IMG = '/api/analyse'
INDEX = '/'
URL_WEB_CNTLR = '/api/robot'
URL_WEB_CNTLR_CMD = URL_WEB_CNTLR + '/cmd'
IDX_WEB_CNTLR_CMD = 'cmd'

URL_VIDEO_FEED = '/api/camera/video_feed'
URL_LAST_FRAME = '/api/camera/last_frame'

TEMPLATE_CNTLR = 'index.html'

CAM_RESOLUTION = '320x240'
CAM_IMAGE_FORMAT = 'mjpeg'

FOLLOW_OBJECT = True

# Robot
robot = AlphaBot2()
controller = Controller(robot)

# Flux video
camera = picamera.PiCamera(resolution=CAM_RESOLUTION)
streaming_output = StreamingOutput()
camera.start_recording(streaming_output, format=CAM_IMAGE_FORMAT)


# CAMERA
@app.route(INDEX)
def index():
    return render_template(TEMPLATE_CNTLR)


@app.route(URL_WEB_CNTLR_CMD, methods=['POST'])
def web_controller():
    cmd = request.form[IDX_WEB_CNTLR_CMD]

    controller.command(cmd)

    return jsonify(status=200)


@app.route(URL_ANALYSE_IMG, methods=['POST'])
def analyse_controller():
    x0 = int(request.form['x0'])
    y0 = int(request.form['y0'])
    x1 = int(request.form['x1'])
    y1 = int(request.form['y1'])
    distance = int(request.form['distance'])
    x_center = int(request.form['x_center'])
    y_center = int(request.form['y_center'])
    mask = io.BytesIO

    coords = (y0, x0, y1, x1)
    center = (y_center, x_center)

    streaming_output.set_coords_object((x0, y0, x1, y1))
    #controller.follow_object(center, coords, distance)
    return jsonify(status=200)


@app.route(URL_VIDEO_FEED)
def video_feed():
    return Response(streaming_output.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route(URL_LAST_FRAME)
def last_frame():
    return Response(io.BytesIO(streaming_output.frame), mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

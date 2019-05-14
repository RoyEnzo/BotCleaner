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

URL_WEB_CNTLR = '/web_controller'
URL_WEB_CNTLR_CMD = URL_WEB_CNTLR + '/cmd'
IDX_WEB_CNTLR_CMD = 'cmd'
TEMPLATE_CNTLR = 'index.html'

URL_VIDEO_FEED = '/camera/video_feed'
URL_LAST_FRAME = '/camera/last_frame'

CAM_RESOLUTION = '640x480'

# Robot
robot = AlphaBot2()
controller = Controller(robot)

# Flux video
camera = picamera.PiCamera(resolution=CAM_RESOLUTION)
output = StreamingOutput()
camera.start_recording(output, format='mjpeg')


# CAMERA
@app.route(URL_WEB_CNTLR)
def live_streaming():
    """
    Affiche la page de controles du robot
    :return: Page de controles
    """
    return render_template(TEMPLATE_CNTLR)

@app.route(URL_WEB_CNTLR_CMD, methods=['POST'])
def web_controller():
    """
    Envoie les requetes de la page de commande au controleur du robot
    :return: resultat fonction
    """
    cmd = request.form[IDX_WEB_CNTLR_CMD]  # pas du json

    controller.command(cmd)

    return jsonify(status=200)  # pas encore gestion error


@app.route(URL_VIDEO_FEED)
def video_feed():
    """
    Flux video mjpeg de la picamera
    :return: generateur d'un SteamingOutput
    """
    return Response(gen(output), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route(URL_LAST_FRAME)
def last_frame():
    """
    Obtient la dernière image du flux video
    :return: image jpeg
    """
    return Response(io.BytesIO(output.frame), mimetype='image/jpeg')


def gen(self):
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + self.frame + b'\r\n')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

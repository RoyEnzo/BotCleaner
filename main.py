"""
AlphaCleaner
"""

__author__ = "Enzo Roy"
__version__ = "1.0.0"
__email__ = "enzo.r@eduge.ch"
__status__ = "Development"

from flask import Flask, Response, render_template, request, jsonify
from streaming import StreamingOutput
from controller import Controller
from alphabot2 import AlphaBot2

# Serveur flask
app = Flask(__name__)

# Robot
robot = AlphaBot2()

# Controller
controller = Controller(robot)

# Flux video
output = StreamingOutput()
robot.camera.start_recording(output, format='mjpeg')


# CAMERA
@app.route('/camera/live_streaming')
def live_streaming():
    """Affichage page de streaming"""
    return render_template('index.html')


@app.route('/camera/video_feed')
def video_feed():
    """Flux video de la camera"""
    return Response(output.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/web_controller/cmd', methods=['POST'])
def web_controller():
    """ Recois les informations de la manette web """
    cmd = request.form['cmd']

    controller.command(cmd)

    return jsonify(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

"""
AlphaCleaner
"""

__author__ = "Enzo Roy"
__version__ = "1.0.0"
__email__ = "enzo.r@eduge.ch"
__status__ = "Development"

from flask import Flask, Response, render_template
from streaming import StreamingOutput
import picamera

# Serveur flask
app = Flask(__name__)

# Flux video
camera = picamera.PiCamera(resolution='640x480')
output = StreamingOutput()
camera.start_recording(output, format='mjpeg')


# CAMERA
@app.route('/camera/live_streaming')
def live_streaming():
    """Affichage page de streaming"""
    return render_template('index.html')


@app.route('/camera/video_feed')
def video_feed():
    """Flux video de la camera"""
    return Response(output.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

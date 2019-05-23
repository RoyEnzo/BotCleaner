
from flask import Flask, Response, render_template, request, jsonify
from streaming import StreamingOutput
from controller import Controller
import picamera
import io


# Constante Flask
# - App route
URL_MODE_MANU = '/'
URL_MODE_AUTO = '/auto'
URL_VIDEO_FEED = '/api/camera/video_feed'
URL_LAST_FRAME = '/api/camera/last_frame'
URL_ANALYSE_IMG = '/api/analyse'
URL_WEB_CNTLR = '/api/robot'
URL_WEB_CNTLR_CMD = URL_WEB_CNTLR + '/cmd'
# - Index POST
IDX_WEB_CNTLR_CMD = 'cmd'
IDX_WEB_MODE = 'mode'
# - Mode
MODE_AUTO = 'auto'
MODE_MANU = 'manuel'
# - Template
TEMPLATE_CNTLR = 'index.html'
TEMPLATE_AUTO = 'auto.html'

# Constant Pi Camera
CAM_RESOLUTION = '160x120'
CAM_IMAGE_FORMAT = 'mjpeg'


# WEB app
app = Flask(__name__)


# Contrôleur
controller = Controller()
mode = MODE_MANU

# Flux video
camera = picamera.PiCamera(resolution=CAM_RESOLUTION)
streaming_output = StreamingOutput()
camera.start_recording(streaming_output, format=CAM_IMAGE_FORMAT)


@app.route(URL_MODE_MANU)
def index():
    """
    Page de contrôles du AlphaBot2.

    Notes:
        Le flux vidéo est disponible sur la page.
        Les flèches directionnelles permettent de déplacer le robot.
        Le curseur permet de changer la vitesse du robot.

    Returns:
        Le modèle de la page index
    """
    global mode
    mode = MODE_MANU

    return render_template(TEMPLATE_CNTLR)


@app.route(URL_MODE_AUTO)
def auto():
    """
    Page de flux vidéo.

    Notes:
        Le curseur permet de changer la vitesse du robot.

    Returns:
        Le modèle de la page auto
    """
    global mode
    mode = MODE_AUTO

    return render_template(TEMPLATE_AUTO)


@app.route(URL_WEB_CNTLR_CMD, methods=['POST'])
def web_controller():
    """
    Transfert les commandes reçues depuis l'application WEB au contrôleur du robot.

    Notes:
        Les différentes commandes possible:
            "forward"
                Robot avance.
            "backward"
                Robot recule.
            "turn_left"
                Robot tourne a gauche.
            "turn_right"
                Robot tourne a droite.
            "stop"
                Robot s'arrête
            "speed=XXX"
                Change la vitesse du robot.
                Remplacer XXX par la vitesse 0-100

        Returns:
            Reponse json
    """
    cmd = request.form[IDX_WEB_CNTLR_CMD]

    controller.command(cmd)

    return jsonify(status=200)


@app.route(URL_ANALYSE_IMG, methods=['POST'])
def analyse_controller():
    """
    Retour de l'analyseur d'image.

    Notes:
        Si le mode est manuelle, affiche uniquement le flux
        Si le mode est automatique, le robot effectue son nettoyage

        x0, y0 (int):
            Point en haut à gauche de l'objet
        x1 y1 (int):
            Point en bas à droite de l'objet
        distance (int):
            Distance entre le centre de l'image et le centre de l'image
        x_center, y_center (int):
            Point du centre de l'image

    Returns:
        Reponse json

    """
    x0 = int(request.form['x0'])
    y0 = int(request.form['y0'])
    x1 = int(request.form['x1'])
    y1 = int(request.form['y1'])
    distance = int(request.form['distance'])
    x_center = int(request.form['x_center'])
    y_center = int(request.form['y_center'])

    coords = (y0, x0, y1, x1)
    center = (y_center, x_center)

    if mode is MODE_AUTO:
        streaming_output.set_coords_object((x0, y0, x1, y1))
        controller.push_object(center, coords, distance)
    elif mode is MODE_MANU:
        streaming_output.set_coords_object((x0, y0, x1, y1))

    return jsonify(status=200)


@app.route(URL_VIDEO_FEED)
def video_feed():
    """
    Flux d'image

    Notes:
        Obtient la prochaine image lorsque qu'elle est disponible

    Returns (jpeg):
        Dernière image disponible
    """
    return Response(streaming_output.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route(URL_LAST_FRAME)
def last_frame():
    """
    Envoie la dernière image prise

    Returns (jpeg):
        Dernière image prise

    """
    return Response(io.BytesIO(streaming_output.frame), mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

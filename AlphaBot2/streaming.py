from threading import Condition
from PIL import Image, ImageDraw
import io


class StreamingOutput(object):
    """
    Classe permettant de créer le flux d'image

    Notes:
        Parties de codes reprises dans la documentation de la Pi Camera:
        https://picamera.readthedocs.io/en/release-1.13/recipes2.html

    Attributes:
        SQUARE_COLOR (tuple):
            Couleur RGB du carré à afficher autour de l'objet trouvé dans la zone.
        FRAME_FOMRAT (str):
            Format de l'image (utiliser pour de la conversion après l'ajout du carré).
        frame (bytes):
            Dernière image de la caméra.
        buffer (bytes):
            Récuperation du flux raw.
        conditon (Condition):
            Notificateur pour les processus.
        coords_object (tuple):
            Coordonnées de l'object dans la zone

    Methods:
        write(buf):
            Récupère le flux de la caméra
        gen():
            Génère une image jpeg avec l'analyse si activé.
        set_coord_object(coords):
            Modifie les dernières coordonées de l'objet.
        add_square_on_target():
            Ajoute un carré vert autour de l'objet.
        convert_img_to_bytes(img):
            Convertit une image en bytes.

    """
    SQUARE_COLOR = (0,255,0)
    FRAME_FORMAT = 'jpeg'

    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()
        self.coords_object = ((-1,-1),(-1,-1))

    def write(self, buf):
        """
        Récupération du flux d'image brut de la caméra.
        Args:
            buf (bytes):
                Flux d'images.

        Returns (bytes):

        """
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

    def gen(self):
        """
        Générateur.

        Notes:
            L'image générée comporte un carré vert autour de l'objet visible dans la zone.

        Yields (bytes):
            Dernière image traitée au format binaire.
        """
        while True:
            analyse_frame = self.add_square_on_target()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + analyse_frame + b'\r\n')

    def set_coords_object(self, coords):
        """
        Définit les nouvelles coordonnées de l'objet.

        Args:
            coords (tuple):
                Coordonnées (x0, y0, x1, y1) de l'objet
        """
        self.coords_object = coords

    def add_square_on_target(self):
        """
        Ajoute un carré sur l'image.
        Les coordonnées du carrée sont celles de l'objets.

        Returns (bytes):
            Image avec le carré vert au format binaire.

        """
        img = Image.open(io.BytesIO(self.frame))
        draw = ImageDraw.Draw(img)

        draw.rectangle(self.coords_object, outline=StreamingOutput.SQUARE_COLOR)

        return self.convert_img_to_bytes(img)

    def convert_img_to_bytes(self, img):
        """
        Convert une image au format binaire.

        Args:
            img (Image):
                Image.

        Returns (bytes):
            Image au format binaire.


        """
        bytes = io.BytesIO()
        img.save(bytes, format=StreamingOutput.FRAME_FORMAT)

        return bytes.getvalue()


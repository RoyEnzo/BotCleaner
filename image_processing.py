import sys
import os

import cv2
from skimage import io
from math import sqrt, pow, hypot
import requests
from datetime import datetime

ip_port_server = sys.argv[1]

URL_SERVER = 'http://' + ip_port_server
print(URL_SERVER)

PATH_LAST_FRAME = '/api/camera/last_frame'
PATH_ANALYSE_CNTLR = '/api/analyse'

PROCESS_SCALE = 0.5
REVERSE_PROCESS_SCALE = 1 / PROCESS_SCALE

DEFAULT_OBJECT_COORD: int = -1

BLACK_VALUE = 0  # GRAYSCALE
WHITE_VALUE = 255


LOWER_COLOR = (0, 120, 120)  # HSV
UPPER_COLOR = (20, 255, 255)


def rescale_image(image, scale):
    """
    Redimensionne l'image à l'échelle donnée.

    Args:
        image (imageio.core.util.Array): Image.
        scale (float): Echelle.

    Returns (imageio.core.util.Array):
        Image redimensionnée

    """
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)

    return cv2.resize(image, (width, height))


def scale_coords(coords, scale):
    """
    Change l'échelle des coordonnées.

    Args:
        coords (tuple): Coordonnées ((x0,y0),(x1,y1)).
        scale (float): Echelle.

    Returns (tuple):
        Coordonnées misent à l'échelle ((x0,y0),(x1,y1)).

    """
    (y0, x0), (y1, x1) = coords

    y0_scaled = int(y0 * scale)
    x0_scaled = int(x0 * scale)
    y1_scaled = int(y1 * scale)
    x1_scaled = int(x1 * scale)

    return ((y0_scaled, x0_scaled), (y1_scaled, x1_scaled))


def get_mask_color_range(image, lower_color, upper_color):
    """
    Obtient le masque des pixels situés entre deux couleurs HSV - OpenCV2.

    Args:
        image (imageio.core.util.Array): Image RGB.
        lower_color (tuple): Couleur HSV la plus claire.
        upper_color (tuple): Couleur HSV la plus foncée.

    Notes:
        HSV de OpenCV est différent -> H 0-180 S 0-255 V 0-255.

    Returns (ndarray):
        Masque.
        Le masque est noir et blanc (0-255).
        Les pixels blancs du masque sont ceux entre les deux couleurs.

    """
    image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    return cv2.inRange(image_hsv, lower_color, upper_color)


def get_first_white_pixel_column(mask):
    """
    Obtient les coordonnées du premier pixel blanc de toutes les colonnes si existant
    
    Args:
        mask (ndarray): Masque en noir et blanc (0-255).

    Returns (list(tuple)):
        Liste des coordonnées (y, x) du premier pixel blanc de toutes les colonnes.
        Si aucun pixel blanc dans la colonne, n'ajoute rien à la liste.

    """
    start_row_index = get_index_first_line_with_white(mask)
    list_white_pixels = []
    mask_width = mask.shape[1]

    for column_index in range(mask_width):
        cropped_mask = mask[start_row_index::]
        column = array2d_column(cropped_mask, column_index)

        for row_index, value in enumerate(column):
            if value == WHITE_VALUE:

                list_white_pixels.append((row_index + start_row_index, column_index))  # mask cropped before, adjust row
                break

    return list_white_pixels


def find_object(mask, list_first_white):
    """
    Obtient les coordonnées d'un objet dans la zone

    Notes:
        L'algorithme cherche les y0,x0,y1,x1 de la manière suivante:

        - Pour chaque pixels blanc de la liste
            - Verifier en dessous si pixel noir
             - SI permiere colonne avec du noir: x0
             - SI derniere colonne avec du noir: x1
             - POUR chaque lignes dans chaque colonnes
                - SI première ligne avec du noir: y0
                - SI dernière ligne avec du noir: y1

        Donc, si deux objets sont dans la surface, il y aura interférences.
        Si un objet est au bord de la surface, peut ne pas être détecté.

    Args:
        mask (ndarray): masque de la surface de travail à analyse, couleur noir et blanc (0-255).
        list_first_white (list): Liste des coordonnées (y, x) du premier pixel blanc de toutes les colonnes.

    Returns (tuple):
        Cordonnées de l'objet ((y0,x0),(y1,x1)).
        Si rien n'est trouvé ->((-1,-1),(-1,-1))
    """

    y0_object = DEFAULT_OBJECT_COORD
    x0_object = DEFAULT_OBJECT_COORD
    y1_object = DEFAULT_OBJECT_COORD
    x1_object = DEFAULT_OBJECT_COORD

    for start_row_index, column_index in list_first_white:

        column_crop = mask[start_row_index::]
        column_values = array2d_column(column_crop, column_index)

        # SI il y a du noir
        if min(column_values) == BLACK_VALUE:

            if x0_object == DEFAULT_OBJECT_COORD:
                x0_object = column_index
            else:
                x1_object = column_index

            for row_index, value in enumerate(column_values):
                row_index += start_row_index  # Colonne coupé à partir du premier pixel blanc

                if (y0_object > row_index or y0_object == DEFAULT_OBJECT_COORD) and value == BLACK_VALUE:
                    y0_object = row_index
                if y1_object < row_index and value == BLACK_VALUE:
                    y1_object = row_index

    if min(y0_object, x0_object, y1_object, x1_object) < 0:
        (y0_object, x0_object, y1_object, x1_object) = (DEFAULT_OBJECT_COORD,) * 4

    return (y0_object, x0_object), (y1_object, x1_object)


def array2d_column(array_2d, index):
    """
    Récupère les valeurs de la colonne d'un tableau 2d

    Args:
        array_2d (ndarray): Tableau 2 dimensions.
        index (int): Index de la colonne.

    Returns (ndarray):
        Tableau de valeurs de la colonne.
    """
    return [row[index] for row in array_2d]


def get_index_first_line_with_white(mask):
    """
    Récupère l'index de la première ligne comportant du blanc.

    Args:
        mask (ndarray): masque en noir et blanc (0-255).

    Returns (int):
        Index de la première ligne comportant du blanc.
    """
    row_index_first_white = 0
    lines_value = [sum(line) for line in mask]

    for row_index, line_value in enumerate(lines_value):
        if row_index > 0:
            if lines_value[row_index - 1] == 0 and line_value > 0:
                row_index_first_white = row_index

    return row_index_first_white


def get_distance(point0, point1):
    """
    Calcul la distance entre deux points.

    Args:
        point0 (tuple): Point (y,x).
        point1 (tuple): Point (y,x).

    Returns (int):
        Distance entre les deux points.
    """
    y0, x0 = point0
    y1, x1 = point1

    adj = y0 - y1
    opp = x0 - x1

    distance_to_center = int(hypot(adj,opp))

    return distance_to_center


def get_center_image(image):
    """
    Calcul le centre de l'image

    Args:
        image (ndarray): Image.

    Returns (tuple):
        Centre (y,x) de l'image
    """
    height, width, _ = image.shape

    return int(height / 2), int(width / 2)


if __name__ == '__main__':
    try:
        while True:
            timer = datetime.now()

            # -- Get Image --
            img = io.imread(URL_SERVER + PATH_LAST_FRAME)

            img_ask_timer = datetime.now() - timer
            timer = datetime.now()

            # -- Analyse --
            img_rescaled = rescale_image(img, PROCESS_SCALE)

            # Récupère la surface de travail du robot et sa delimitation supérieure
            surface_mask = get_mask_color_range(img_rescaled, LOWER_COLOR, UPPER_COLOR)
            surface_border_coord = get_first_white_pixel_column(surface_mask)

            # Cherche l'objet
            coords_object = find_object(surface_mask, surface_border_coord)
            ((y0, x0), (y1, x1)) = scale_coords(coords_object, REVERSE_PROCESS_SCALE)

            y_center, x_center = get_center_image(img)
            y,x = ((DEFAULT_OBJECT_COORD,))*2

            # SI une des valeurs negatives -> il y a pas d'objet
            if min(y0, x0, y1, x1) < 0:
                (y0, x0, y1, x1) = ((DEFAULT_OBJECT_COORD,))*4
                distance = -1
            else:
                y = int((y0 + y1) / 2)
                x = int((x0 + x1) / 2)
                distance = get_distance((y_center, x_center), (y, x))

            analyse_timer = datetime.now() - timer
            timer = datetime.now()

            # -- POST serveur --
            coords = {'x0': x0,
                      'y0': y0,
                      'x1': x1,
                      'y1': y1,
                      'distance': distance,
                      'y_center': y_center,
                      'x_center': x_center
                      }

            path = URL_SERVER + PATH_ANALYSE_CNTLR
            r = requests.post(path, data=coords)
            post_timer = datetime.now() - timer

            # -- Console output--
            print("--------------")
            try:
                os.system('clear')
            except:
                pass
            if  r.status_code == 200:
                print("Center image (y,x) : ", y_center, x_center )
                print("Center object (y,x): ", y,x )
                print("Distance           : ", distance)
                print("")
                print("Get img time  : ", img_ask_timer.total_seconds())
                print("Analyse time  : ", analyse_timer.total_seconds())
                print("Post img time : ", post_timer.total_seconds())
                print("Total time    : ", (img_ask_timer + analyse_timer + post_timer).total_seconds())
            else:
                print("ERROR: ", r.status_code)
    except KeyboardInterrupt:
        exit(0)
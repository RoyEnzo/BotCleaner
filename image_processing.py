import cv2
from skimage import io, transform
from matplotlib import pyplot as plt
import requests

URL_SERVER = 'http://10.134.99.231:5000'
PATH_LAST_FRAME = '/api/camera/last_frame'
PATH_ANALYSE_CNTLR = '/api/analyse'

PROCESS_SCALE = 0.02
REVERSE_PROCESS_SCALE = 1 / PROCESS_SCALE

DEFAULT_OBJECT_COORD = -1

BLACK_VALUE = 0  # GRAYSCALE
WHITE_VALUE = 255
LOWER_COLOR = (0, 100, 100)  #HSV
UPPER_COLOR = (20, 255, 255)

def get_image_url(url):
    """
    Récupère l'image à partir de url
    Args:
        url: str url de l'image

    Returns:
        imageio image de l'url ou -1

    """
    try:
        return io.imread(url)
    except:
        print('Cannot get image image from url :'+url)
        return -1

def rescale_image(image, scale):
    """
    Redimensionne l'image à l'échelle donnée
    Args:
        image:  imageio image à redimensionner
        scale:  float échelle

    Returns:
        imageio image redi

    """
    try:
        width = int(img.shape[1] * scale)
        height = int(img.shape[0] * scale)

        return cv2.resize(image, (width, height))
    except:
        print('Cannot rescale image')
        return -1

def rescale_coords(coords,scale):
    """
    Redimensionne les coordonnées à l'échelle
    Args:
        coords: tuple((x0,y0),(x1,y1)) coordonnées à redimensionner
        scale:  float échelle

    Returns:
        coordonnées misent à l'échelle

    """
    (y0, x0), (y1, x1) = coords

    y0_scaled = int(y0 * scale)
    x0_scaled = int(x0 * scale)
    y1_scaled = int(y1 * scale)
    x1_scaled = int(x1 * scale)

    return ((y0_scaled,x0_scaled),(y1_scaled,x1_scaled))

def get_mask_color_range(image,lower_color,upper_color):
    """
    Obtient le masque des pixels situés entre deux couleurs HSV
    Args:
        image: imageio image à filtrer
        lower_color: tuple(h,s,v) couleur la plus claire
        upper_color: tuple(h,s,v) couleur la plus foncée

    Returns:
        ndarray masque des pixels entre les deux couleurs

    """
    image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    return cv2.inRange(image_hsv, lower_color, upper_color)

def get_coords_top_surface(mask_surface):
    """
    Obtient tous les pixels du bord supérieur de la surface
    Args:
        mask_surface: ndarray masque à traiter

    Returns:
        list coordonnées de la bordure supérieure

    """
    start_index_y = get_start_index_border_surface(mask_surface)
    border_coords = []

    for column_index in range(mask_surface.shape[1]):
        column = array2d_column(mask_surface[start_index_y::], column_index)
        for row_index, value in enumerate(column):
            if value > 0:
                border_coords.append((row_index+start_index_y, column_index))
                break

    return border_coords

def find_object(mask_surface, border_surface_coords):
    """
    Obtient les coordonnées de l'objet dans la zone
    Args:
        mask_surface: ndarray masque de la surface
        border_surface_coords: list coordonnées des points de la face suppérieur de la zone

    Returns:
        tuple((y0,x0),(y1,x1)) Cordonnées de l'objet, tout a -1 si rien trouvé
    """
    
    y0 = DEFAULT_OBJECT_COORD
    x0 = DEFAULT_OBJECT_COORD
    y1 = DEFAULT_OBJECT_COORD
    x1 = DEFAULT_OBJECT_COORD

    # Scan pour chaque colonnes
    for start_row_index, column_index in border_surface_coords:

        # Coupe la colonne a partir du bord de la surface
        column_crop = mask_surface[start_row_index::]

        column_values = array2d_column(column_crop, column_index)

        # SI il y a du noir
        if min(column_values) == BLACK_VALUE:

            # Premiere ligne comportant du noir -> x0
            # Derniere ligne comportant du noir -> x1
            if x0 == DEFAULT_OBJECT_COORD:
                x0 = column_index
            else:
                x1 = column_index

            # PCherche le y0 le plus bas et y1 le plus haut dans la colonne
            for row_index, value in enumerate(column_values):
                row_index += start_row_index  # Colonne coupé à partir du bord précédemment
                if (y0 > row_index or y0 == DEFAULT_OBJECT_COORD) and value == BLACK_VALUE:
                    y0 = row_index
                if y1 < row_index and value == BLACK_VALUE:
                    y1 = row_index

    return ((y0,x0),(y1,x1))

def array2d_column(array_2d, index):
    """
    Récupère la colonne d'un tableau 2d
    Args:
        array_2d: ndarray tableau 2 dimensions
        index: int index de la colonne

    Returns:
        ndarray colonne du tableau 2d
    """
    return [row[index] for row in array_2d]

def get_start_index_border_surface(mask_surface):
    """
    Récupère index de la première ligne comportant la surface
    Args:
        mask_surface: ndarray masque à analyser

    Returns:
        index de la première ligne comportant la surface
    """
    index_y_border = 0
    lines_value = [sum(i) for i in mask_surface]

    for index, line_value in enumerate(lines_value):
        if index > 0:
            if lines_value[index-1] == 0 and line_value > 0:
                index_y_border = index

    return index_y_border

def draw_square(image, coords):
    """
    Dessine un carré sur l'image
    Args:
        image: ndarray image à modifier
        coords: tuple coordonnées du carré
    Returns:
        image dessinée
    """
    (y1,x1),(y2, x2) = coords

    image_drawn = cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 10)

    return image_drawn

def show_image(image):
    """
    Affiche l'image
    Args:
        image: ndarray image à afficher
    """
    io.imshow(image)
    plt.show()

if __name__ == '__main__':
    while True:
        # Récupération de l'image et mise à l'échelle
        img = get_image_url(URL_SERVER+PATH_LAST_FRAME)
        img_rescaled = rescale_image(img, PROCESS_SCALE)

        # Récupère la surface de travail du robot
        surface_mask = get_mask_color_range(img_rescaled, LOWER_COLOR, UPPER_COLOR)
        surface_border_coord = get_coords_top_surface(surface_mask)

        # Cherche l'objet
        coords_object = find_object(surface_mask, surface_border_coord)
        ((y0,x0),(y1,x1)) = rescale_coords(coords_object,REVERSE_PROCESS_SCALE)

        # Envoie au serveur les données
        coords = {'x0': x0,'y0': y0, 'x1': x1, 'y1': y1}
        path = URL_SERVER+PATH_ANALYSE_CNTLR
        r = requests.post(path, data=coords)
        print(r.status_code)


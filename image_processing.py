import cv2
from skimage import io, transform
from matplotlib import pyplot as plt

SCALE = 0.1
URL = 'http://192.168.1.141:5000/camera/last_frame?scale=' + str(SCALE)
LOWER_ORANGE = (0, 100, 100)  #HSV
UPPER_ORANGE = (20, 255, 255)
LOWER_BLACK = ()
UPPER_BLACK = ()

def get_image_url(url: str):
    """
    Recupere image depuis une url
    :param url: str url
    :return: image
    """
    return io.imread(url)

def rescale_image(img,scale):
    """
    Change l echelle de l image
    :param img: image
    :param scale: echelle
    :return: image a l echelle
    """
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)

    return cv2.resize(img, (width, height))

def get_mask_color_range(img,lower_color,upper_color):
    """
    Obtient le masque des pixels d'une image compris entre deux couleurs HSV
    :param img: image RGB
    :param lower_color: couleur HSV minimum
    :param upper_color: couleur HSV maximum
    :return: masque 2d (couleur binaire) des pixels compris entre les deux couleurs
    """
    image_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    return cv2.inRange(image_hsv, lower_color, upper_color)

def show_image(img):
    """
    Affiche l'image
    :param img: image
    """
    io.imshow(img)
    plt.show()

def find_border_surface(img):
    """
    Retourne masque bord de la surface
    :param surface: masque 2d (binaire) de la surface
    :return: tableau 2d bord de la surface (x,y) de chaque pixels
    """
    start_index_y = start_index_surface_border_y(img)
    img_height, img_width = img.shape
    border_coord = []

    for column_index in range(img.shape[1]):
        row = array2d_column(img[start_index_y::],column_index)
        for row_index, value in enumerate(row):
            if value > 0:
                border_coord.append((row_index+start_index_y, column_index))
                break

    return border_coord

def array2d_column(matrix, i):
    return [row[i] for row in matrix]


def start_index_surface_border_y(surface):
    """
    Trouve l'index y comportant le bord de la surface
    Returns: index y du bord de la surface
    """
    index_y_border = 0
    lines_value = [sum(i) for i in surface]

    for index, line_value in enumerate(lines_value):
        if index > 0:
            if lines_value[index-1] == 0 and line_value > 0:
                index_y_border = index

    return index_y_border


img = get_image_url(URL)
img_rescaled = rescale_image(img, 0.02)
surface = get_mask_color_range(img_rescaled,LOWER_ORANGE,UPPER_ORANGE)


for y,x in find_border_surface(surface):
    surface[y][x] = 127
#show_image(img_rescaled)
show_image(surface)


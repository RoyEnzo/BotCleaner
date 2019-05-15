import cv2
from skimage import io, transform
from matplotlib import pyplot as plt

SCALE = 0.1
URL = 'http://10.134.97.49:5000/camera/last_frame?scale=' + str(SCALE)
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

def find_border_surface(surface):
    """
    Retourne masque bord de la surface
    :param surface: masque 2d (binaire) de la surface
    :return: masque 2d (binaire) bord de la surface
    """



img = get_image_url(URL)
img_rescaled = rescale_image(img, 0.03)
surface = get_mask_color_range(img_rescaled,LOWER_ORANGE,UPPER_ORANGE)
#show_image(img)
#show_image(img_rescaled)
show_image(surface)


import cv2
from skimage import io, transform
from matplotlib import pyplot as plt

URL = 'http://10.134.99.231:5000/camera/last_frame'
LOWER_ORANGE = (0, 100, 100)  #HSV
UPPER_ORANGE = (20, 255, 255)
LOWER_BLACK = ()
UPPER_BLACK = ()
PROCESS_SCALE = 0.05
REVERSE_PROCESS_SCALE = 1 / PROCESS_SCALE

def get_image_url(url: str):
    return io.imread(url)

def rescale_image(img,scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)

    return cv2.resize(img, (width, height))
def rescale_coords(coords):
    (y1, x1), (y2, x2) = coords

    y1_scaled = int(y1 * REVERSE_PROCESS_SCALE)
    x1_scaled = int(x1 * REVERSE_PROCESS_SCALE)
    y2_scaled = int(y2 * REVERSE_PROCESS_SCALE)
    x2_scaled = int(x2 * REVERSE_PROCESS_SCALE)

    return ((y1_scaled,x1_scaled),(y2_scaled,x2_scaled))

def get_mask_color_range(img,lower_color,upper_color):
    image_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    return cv2.inRange(image_hsv, lower_color, upper_color)

def find_border_surface(img):
    start_index_y = start_index_surface_border_y(img)
    border_coord = []

    for column_index in range(img.shape[1]):
        column = array2d_column(img[start_index_y::],column_index)
        for row_index, value in enumerate(column):
            if value > 0:
                border_coord.append((row_index+start_index_y, column_index))
                break

    return border_coord

def find_object(img, mask_surface, border_surface):
    y1_object = -1
    x1_object = -1
    y2_object = -1
    x2_object = -1

    # Pour chaque colonne
    for column_index in range(mask_surface.shape[1]):
        # Debut de la col
        start_row_index = border_surface[column_index][0]
        # La colonne a partir le bord de la surface
        column = array2d_column(mask_surface[start_row_index::], column_index)

        # SI il y a du noir
        if sum(column) != len(column) * 255:
            # Enregistre le x1 le plus bas
            if x1_object == -1:
                x1_object = column_index
                
            # Enregistre le x2 le plus eleve
            x2_object = column_index

            # Pour chaque colonne cherche le y1 le plus bas et y2 le plus haut
            for row_index, value in enumerate(column):
                row_index += start_row_index
                if (y1_object > row_index or y1_object == -1) and value == 0:
                    y1_object = row_index
                if y2_object < row_index and value == 0:
                    y2_object = row_index

    return ((y1_object,x1_object),(y2_object,x2_object))

def array2d_column(matrix, i):
    return [row[i] for row in matrix]

def start_index_surface_border_y(surface):
    index_y_border = 0
    lines_value = [sum(i) for i in surface]

    for index, line_value in enumerate(lines_value):
        if index > 0:
            if lines_value[index-1] == 0 and line_value > 0:
                index_y_border = index

    return index_y_border

def draw_square(img, coords):
    (y1,x1),(y2, x2) = coords

    cv2.rectangle(img, (x1,y1), (x2,y2), (0, 255, 0), 10)

def show_image(img):
    io.imshow(img)
    plt.show()

if __name__ == '__main__':
    img = get_image_url(URL)
    print(type(img))
    img_rescaled = rescale_image(img, PROCESS_SCALE)

    surface_mask = get_mask_color_range(img_rescaled,LOWER_ORANGE,UPPER_ORANGE)
    surface_border_coord = find_border_surface(surface_mask)

    coords_object = rescale_coords(find_object(img, surface_mask, surface_border_coord))

    draw_square(img, coords_object)
    print(type(img))
    show_image(img)
    #show_image(surface)


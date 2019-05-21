from threading import Condition
from PIL import Image, ImageDraw
import io


class StreamingOutput(object):
    SQUARE_COLOR = (0,255,0)
    FRAME_FORMAT = 'jpeg'

    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()
        self.coords_object = ((-1,-1),(-1,-1))

    def write(self, buf):
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
        while True:
            self.add_square_target_on_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + self.frame + b'\r\n')

    def set_coords_object(self, coords):
        self.coords_object = coords

    def add_square_target_on_frame(self):
        img = Image.open(io.BytesIO(self.frame))
        draw = ImageDraw.Draw(img)
        draw.rectangle(self.coords_object, outline=StreamingOutput.SQUARE_COLOR)

        self.frame = self.convert_img_to_bytes(img)

    def convert_img_to_bytes(self, img):
        bytes = io.BytesIO()
        img.save(bytes, format=StreamingOutput.FRAME_FORMAT)

        return bytes.getvalue()


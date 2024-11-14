from PIL import Image
import io

class ImageHandler:
    def __init__(self, image_path=None):
        self.image_path = image_path

    def image_to_bytes(self):
        """Konwertuje obraz na bajty."""
        with Image.open(self.image_path) as img:
            with io.BytesIO() as byte_io:
                img.save(byte_io, format='BMP')  # Zapis obrazu jako BMP
                return byte_io.getvalue()  # Zwraca bajty obrazu

    def bytes_to_image(self, byte_data, output_path):
        """Konwertuje bajty z powrotem na obraz i zapisuje go."""
        with io.BytesIO(byte_data) as byte_io:
            img = Image.open(byte_io)
            img.save(output_path)

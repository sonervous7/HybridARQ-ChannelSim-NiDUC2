from PIL import Image
import io

class ImageHandler:
    def __init__(self, image_path=None):
        self.image_path = image_path

    def image_to_bytes(self):
        """Konwertuje obraz na bajty."""
        with Image.open(self.image_path) as img:
            print(f"Wymiary oryginalnego obrazu: {img.size}, Format: {img.format}") #debug print
            with io.BytesIO() as byte_io:
                img.save(byte_io, format='bmp')  # Zapis obrazu jako png
                data = byte_io.getvalue() #debug statement
                print(f"Rozmiar danych BMP: {len(data)} bajtów") #debug print
                return byte_io.getvalue()  # Zwraca bajty obrazu

    # def image_to_bytes(self):
    #     """Zwraca bajty oryginalnego obrazu bez konwersji."""
    #     with open(self.image_path, 'rb') as file:
    #         return file.read()

    def bytes_to_image(self, byte_data, output_path):
        """Konwertuje bajty z powrotem na obraz za pomocą Pillow."""
        with io.BytesIO(byte_data) as byte_io:
            img = Image.open(byte_io)
            img.save(output_path)



class Frame:
    def __init__(self, packet_num, data, encoding_info, checksum):
        self.packet_num = packet_num      # Numer pakietu
        self.data = data                  # Dane (np. fragment obrazu)
        self.encoding_info = encoding_info # Informacje o kodowaniu
        self.checksum = checksum          # Suma kontrolna (np. CRC)

    @staticmethod
    def create_frame(packet_num, data, error_detection_code):
        checksum = error_detection_code.calculate_checksum(data)
        return Frame(packet_num, data, encoding_info=type(error_detection_code).__name__, checksum=checksum)

from reedsolo import RSCodec
import numpy as np


class ErrorCorrectionCode:
    def __init__(self, symbols): # Długość części korekcyjnej
        self.rs = RSCodec(symbols)

    def encode(self, data_bytes):
        print("Dane przed kodowaniem (RS):", data_bytes)
        encoded_data = self.rs.encode(data_bytes)
        # print("Dane po kodowaniu (RS):", encoded_data)
        data_length = len(data_bytes)
        correction_data = encoded_data[data_length:]
        return correction_data

    def decode(self, data_bytes):
        try:
            if isinstance(data_bytes, (bytearray, list, np.ndarray)):
                data_bytes = bytes(data_bytes)
            print("Dane przed dekodowaniem (RS):", data_bytes)
            decoded_data, _, _ = self.rs.decode(data_bytes) # (decoded_data, repair, erasures)
            # print("Dane po dekodowaniu (RS):", decoded_data)
            return decoded_data
        except Exception as e:
            print("Błąd korekcji Reed-Solomon:", e)
            return None

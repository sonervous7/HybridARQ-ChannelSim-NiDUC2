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

    def encode_bits(self, bit_array):
        """Kodowanie korekcyjne dla bitów."""
        byte_data = self.bits_to_bytes(bit_array)
        correction_bytes = self.encode(byte_data)
        return self.bytes_to_bits(correction_bytes)

    def decode_bits(self, bit_array, original_bit_length):
        """Dekodowanie korekcyjne dla bitów."""
        byte_data = self.bits_to_bytes(bit_array)
        decoded_bytes = self.decode(byte_data)
        if decoded_bytes:
            decoded_bits = self.bytes_to_bits(decoded_bytes)
            decoded_bits_diff = len(decoded_bits) - len(original_bit_length)
            # Debug print
            print("Długosc decoded_bytes: ", len(decoded_bits))
            print("Długosc parametru original_bit_length: ", len(original_bit_length))
            print("Obliczona różnica aby mieć odpowiedni zakres: ", decoded_bits_diff)
            decoded_bits = decoded_bits[decoded_bits_diff:]
        return decoded_bits if decoded_bytes else None

    @staticmethod
    def bits_to_bytes(bit_array):
        """Konwersja tablicy bitów na bajty."""
        byte_array = bytearray()
        for i in range(0, len(bit_array), 8):
            byte = 0
            for bit in bit_array[i:i+8]:
                byte = (byte << 1) | bit
            byte_array.append(byte)
        return bytes(byte_array)

    @staticmethod
    def bytes_to_bits(byte_array):
        """Konwersja bajtów na tablicę bitów."""
        bit_array = []
        for byte in byte_array:
            for i in range(7, -1, -1):
                bit_array.append((byte >> i) & 1)
        return bit_array

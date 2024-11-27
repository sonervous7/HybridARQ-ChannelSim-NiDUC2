from abc import ABC, abstractmethod
import zlib
import crcmod


class ErrorDetectionCode(ABC):
    @abstractmethod
    def encode(self, data):
        pass

    @abstractmethod
    def decode(self, data):
        pass

    @abstractmethod
    def encode_bits(self, bits):
        pass

    @abstractmethod
    def decode_bits(self, bits):
        pass

    @abstractmethod
    def calculate_checksum(self, data):
        pass

    @staticmethod
    def bits_to_bytes(bit_array):
        """Konwersja bitów na bajty."""
        byte_array = bytearray()
        for i in range(0, len(bit_array), 8):
            byte = 0
            for bit in bit_array[i:i + 8]:
                byte = (byte << 1) | bit
            byte_array.append(byte)
        return bytes(byte_array)

    @staticmethod
    def bytes_to_bits(byte_array):
        """Konwersja bajtów na bity."""
        bit_array = []
        for byte in byte_array:
            for i in range(7, -1, -1):
                bit_array.append((byte >> i) & 1)
        return bit_array


class ParityCode(ErrorDetectionCode):
    def encode(self, data):
        parity_bit = sum(data) % 2
        return data + bytes([parity_bit])

    def decode(self, data):
        if not data:
            print("Błąd: brak danych do dekodowania w ParityCode.")
            return None
        original_data, parity_bit = data[:-1], data[-1]
        if sum(original_data) % 2 == parity_bit:
            return original_data
        else:
            print("Błąd detekcji w kodzie parzystości.")
            return None

    def encode_bits(self, bit_array):
        """Kodowanie detekcyjne dla bitów."""
        parity_bit = sum(bit_array) % 2
        return bit_array + [parity_bit]

    def decode_bits(self, bit_array):
        """Dekodowanie detekcyjne dla bitów."""
        if not bit_array:
            print("Błąd: brak danych do dekodowania w ParityCode.")
            return None

        original_data, parity_bit = bit_array[:-1], bit_array[-1]

        if self.calculate_checksum(original_data) == parity_bit:
            return original_data
        else:
            print("Błąd detekcji w kodzie parzystości.")
            return None

    def calculate_checksum(self, data):
        return sum(data) % 2


class CRC8(ErrorDetectionCode):
    def __init__(self):
        self.crc8_fun = crcmod.mkCrcFun(0x107, initCrc=0x00, xorOut=0x00)

    def encode(self, data):
        checksum = self.calculate_checksum(data)
        # Dołączamy sumę kontrolną jako 1 bajt za pomocą to_bytes
        return data + checksum.to_bytes(1, byteorder='big')

    def decode(self, data):
        # Rozdzielamy dane i sumę kontrolną
        original_data, checksum = data[:-1], int.from_bytes(data[-1:], byteorder='big')
        # Porównujemy obliczoną sumę kontrolną z przesłaną
        if self.calculate_checksum(original_data) == checksum:
            return original_data
        else:
            print("Błąd detekcji CRC8.")
            return None

    def encode_bits(self, bit_array):
        """Zakoduj tablicę bitów za pomocą CRC8."""
        byte_data = self.bits_to_bytes(bit_array)
        encoded_data = self.encode(byte_data)
        return self.bytes_to_bits(encoded_data)

    def decode_bits(self, bit_array):
        """Dekoduj tablicę bitów za pomocą CRC8."""
        byte_data = self.bits_to_bytes(bit_array)
        decoded_data = self.decode(byte_data)
        return self.bytes_to_bits(decoded_data) if decoded_data else None

    def calculate_checksum(self, data):
        return self.crc8_fun(data)


class CRC16(ErrorDetectionCode):

    def __init__(self):
        # Definicja wielomianu CRC-16: x^16 + x^12 + x^5 + 1
        self.crc16_fun = crcmod.mkCrcFun(0x11021, initCrc=0x0000, xorOut=0x0000)

    def encode(self, data):
        checksum = self.calculate_checksum(data)
        return data + checksum.to_bytes(2, byteorder='big')

    def decode(self, data):
        # Oryginalne dane (wszystkie poza ostatnimi dwoma bajtami)
        original_data = data[:-2]
        # Sumę kontrolną odczytujemy z dwóch ostatnich bajtów
        checksum = int.from_bytes(data[-2:], byteorder='big')  # Konwersja z 2 bajtów na liczbę całkowitą
        # Sprawdzamy, czy obliczona suma zgadza się z przesłaną
        if self.calculate_checksum(original_data) == checksum:
            return original_data
        else:
            print("Błąd detekcji CRC16.")
            return None

    def encode_bits(self, bit_array):
        """Zakoduj tablicę bitów za pomocą CRC16."""
        byte_data = self.bits_to_bytes(bit_array)
        encoded_data = self.encode(byte_data)
        return self.bytes_to_bits(encoded_data)

    def decode_bits(self, bit_array):
        """Dekoduj tablicę bitów za pomocą CRC16."""
        byte_data = self.bits_to_bytes(bit_array)
        decoded_data = self.decode(byte_data)
        return self.bytes_to_bits(decoded_data) if decoded_data else None

    def calculate_checksum(self, data):
        return self.crc16_fun(data)


class CRC32(ErrorDetectionCode):
    def encode(self, data):
        checksum = self.calculate_checksum(data)
        # Dołączamy sumę kontrolną jako 4 bajty
        return data + checksum.to_bytes(4, byteorder='big')

    def decode(self, data):
        # Oryginalne dane (wszystkie poza ostatnimi czterema bajtami)
        original_data = data[:-4]
        # Odczytujemy sumę kontrolną z 4 ostatnich bajtów
        checksum = int.from_bytes(data[-4:], byteorder='big')
        # Porównujemy obliczoną sumę kontrolną z przesłaną
        if self.calculate_checksum(original_data) == checksum:
            return original_data
        else:
            print("Błąd detekcji CRC32.")
            return None

    def encode_bits(self, bit_array):
        """Zakoduj tablicę bitów za pomocą CRC32."""
        byte_data = self.bits_to_bytes(bit_array)
        encoded_data = self.encode(byte_data)
        return self.bytes_to_bits(encoded_data)

    def decode_bits(self, bit_array):
        """Dekoduj tablicę bitów za pomocą CRC32."""
        byte_data = self.bits_to_bytes(bit_array)
        decoded_data = self.decode(byte_data)
        return self.bytes_to_bits(decoded_data) if decoded_data else None

    def calculate_checksum(self, data):
        return zlib.crc32(data)

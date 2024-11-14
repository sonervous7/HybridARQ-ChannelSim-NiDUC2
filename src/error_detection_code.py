from abc import ABC, abstractmethod
import zlib


class ErrorDetectionCode(ABC):
    @abstractmethod
    def encode(self, data):
        pass

    @abstractmethod
    def decode(self, data):
        pass

    @abstractmethod
    def calculate_checksum(self, data):
        pass

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

    def calculate_checksum(self, data):
        return sum(data) % 2

class CRC8(ErrorDetectionCode):
    def encode(self, data):
        checksum = self.calculate_checksum(data)
        return data + bytes([checksum])

    def decode(self, data):
        original_data, checksum = data[:-1], data[-1]
        if self.calculate_checksum(original_data) == checksum:
            return original_data
        else:
            print("Błąd detekcji CRC8.")
            return None

    def calculate_checksum(self, data):
        return zlib.crc32(data) & 0xFF

class CRC16(ErrorDetectionCode):
    def encode(self, data):
        checksum = self.calculate_checksum(data)
        return data + bytes([checksum >> 8, checksum & 0xFF])

    def decode(self, data):
        original_data, high_byte, low_byte = data[:-2], data[-2], data[-1]
        checksum = (high_byte << 8) | low_byte
        if self.calculate_checksum(original_data) == checksum:
            return original_data
        else:
            print("Błąd detekcji CRC16.")
            return None

    def calculate_checksum(self, data):
        return zlib.crc32(data) & 0xFFFF

class CRC32(ErrorDetectionCode):
    def encode(self, data):
        checksum = self.calculate_checksum(data)
        return data + bytes([checksum >> 24, (checksum >> 16) & 0xFF, (checksum >> 8) & 0xFF, checksum & 0xFF])

    def decode(self, data):
        original_data = data[:-4]
        byte1, byte2, byte3, byte4 = data[-4:]
        checksum = (byte1 << 24) | (byte2 << 16) | (byte3 << 8) | byte4
        if self.calculate_checksum(original_data) == checksum:
            return original_data
        else:
            print("Błąd detekcji CRC32.")
            return None

    def calculate_checksum(self, data):
        return zlib.crc32(data)



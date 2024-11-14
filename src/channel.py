import komm
import numpy as np
from gilbert_elliott_channel import GilbertElliottChannel


class Channel:
    def __init__(self, channel_type="BSC", **kwargs):
        self.channel_type = channel_type

        if channel_type == "BSC":
            self.channel = komm.BinarySymmetricChannel(crossover_probability=kwargs.get("ber", 0.1))
        elif channel_type == "GilbertElliott":
            self.channel = GilbertElliottChannel(
                good_to_bad=kwargs.get("good_to_bad", 0.05),
                bad_to_good=kwargs.get("bad_to_good", 0.1),
                good_error_prob=kwargs.get("good_error_prob", 0.01),
                bad_error_prob=kwargs.get("bad_error_prob", 0.2),
            )

    def _bytes_to_bits(self, byte_data):
        bit_list = []
        for byte in byte_data:
            for i in range(8):
                bit_list.append((byte >> (7 - i)) & 1)
        return np.array(bit_list)

    def _bits_to_bytes(self, bit_list):
        # Dodaj padding, jeśli potrzeba, aby uzyskać pełne bajty
        if len(bit_list) % 8 != 0:
            padding = 8 - (len(bit_list) % 8)
            bit_list = np.pad(bit_list, (0, padding), constant_values=0)

        byte_list = []
        for i in range(0, len(bit_list), 8):
            byte = 0
            for bit in bit_list[i:i + 8]:
                byte = (byte << 1) | bit
            byte_list.append(byte)
        return bytes(byte_list)



    def channel_transmit(self, data):
        # Przesyłanie danych przez kanał

        if self.channel_type == 'BSC':
            # Konwersja bajtów na bity przed transmisją
            bit_data = self._bytes_to_bits(data)
            # print("Dane w bitach przed transmisją:", bit_data)

            # Przesyłanie bitów przez kanał
            transmitted_bits = self.channel(bit_data)
            # print("Dane w bitach po transmisji:", transmitted_bits)

            # Konwersja bitów z powrotem na bajty
            transmitted_data = self._bits_to_bytes(transmitted_bits)
            # print("Dane po transmisji w bajtach:", transmitted_data)

            return transmitted_data
        else:
            return self.channel.transmit(data)









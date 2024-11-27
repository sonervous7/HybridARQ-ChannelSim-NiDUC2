import random
from channel import Channel
from error_detection_code import ErrorDetectionCode, ParityCode, CRC8, CRC16, CRC32
from error_correction_code import ErrorCorrectionCode
from image_handler import ImageHandler
from gilbert_elliott_channel import GilbertElliottChannel
from frame import Frame


class Pipeline:
    def __init__(self, image_path, output_path):
        self.image_handler = ImageHandler(image_path)
        self.output_path = output_path
        self.channel = None
        self.error_detection_code = None
        self.error_correction_code = None

    def select_channel(self):
        print("Wybierz kanał transmisji:")
        print("1. Binary Symmetric Channel (BSC)")
        print("2. Gilbert-Elliott Channel")
        choice = int(input("Twój wybór: "))

        if choice == 1:
            ber = float(input("Podaj prawdopodobieństwo błędu bitu (0-1) dla BSC: "))
            self.channel = Channel(channel_type="BSC", ber=ber)
        elif choice == 2:
            good_to_bad = float(input("Podaj wartość dla goodToBadProbability: "))
            bad_to_good = float(input("Podaj wartość dla badToGoodProbability: "))
            good_error_prob = float(input("Podaj wartość dla goodChannelErrorProbability: "))
            bad_error_prob = float(input("Podaj wartość dla badChannelErrorProbability: "))
            self.channel = Channel(
                channel_type="GilbertElliott",
                good_to_bad=good_to_bad,
                bad_to_good=bad_to_good,
                good_error_prob=good_error_prob,
                bad_error_prob=bad_error_prob,
            )
        else:
            print("Niepoprawny wybór kanału transmisji.")
            return False
        return True

    def select_error_detection_code(self):
        print("Wybierz kod detekcyjny:")
        print("1. Bit parzystości")
        print("2. CRC8")
        print("3. CRC16")
        print("4. CRC32")
        choice = int(input("Twój wybór: "))

        if choice == 1:
            self.error_detection_code = ParityCode()
        elif choice == 2:
            self.error_detection_code = CRC8()
        elif choice == 3:
            self.error_detection_code = CRC16()
        elif choice == 4:
            self.error_detection_code = CRC32()
        else:
            print("Niepoprawny wybór kodu detekcyjnego.")
            return False
        return True

    def select_error_correction_code(self):
        print("Wybierz kod korekcyjny:")
        print("1. Reed-Solomon")
        choice = int(input("Twój wybór: "))

        if choice == 1:
            self.error_correction_code = ErrorCorrectionCode(30)  # Liczba symboli korekcyjnych (długość kodu w bajtach) RS
        else:
            print("Niepoprawny wybór kodu korekcyjnego.")
            return False
        return True

    def run_image_transmission(self):
        self.select_channel()
        self.select_error_detection_code()
        self.select_error_correction_code()

        data = self.image_handler.image_to_bytes()  # Załaduj obraz i konwertuj na dane bajtowe
        header = data[:54]
        pixel_data = data[54:]
        print("Uruchamianie symulacji transmisji obrazu...")

        packets = [pixel_data[i : i + 64] for i in range(0, len(pixel_data), 64)]  # Dzielenie danych na pakiety 64-bajtowe
        print(f"Rozmiar danych: {len(pixel_data)} bajtów")
        print(f"Liczba pakietów: {len(packets)}")
        retransmission_counts = [0] * 12  # Licznik transmisji za X razem
        errors_detected = 0  # Liczba pakietów, które nie zostały poprawnie odebrane
        received_data = bytearray(header)  # Inicjalizuj otrzymane dane nagłówkiem

        for packet_num, packet in enumerate(packets, start=1):

            print(f"\n--- Pakiet nr {packet_num} ---")
            print("Dane oryginalne:", packet)

            frame = Frame.create_frame(packet_num, packet, self.error_detection_code)

            success = False
            retries = 0

            while not success and retries < 10:
                retries += 1
                print(f"Próba nr {retries} dla pakietu {packet_num}")

                # Kodowanie detekcyjne
                detected_data = self.error_detection_code.encode(packet)
                print("Dane po kodowaniu detekcyjnym:", detected_data)

                # Transmisja przez kanał
                transmitted_data = self.channel.channel_transmit(detected_data)
                print("Dane po transmisji przez kanał:", transmitted_data)

                # Dekodowanie detekcyjne - aby sprawdzić czy potrzebna jest retransmisja z kodami korekcyjnymi
                decoded_data = self.error_detection_code.decode(transmitted_data)
                if decoded_data is None:

                    # Kodowanie detekcyjne ponownie
                    # detected_data = self.error_detection_code.encode(packet)
                    # print("Dane po kodowaniu detekcyjnym:", detected_data)

                    # Kodowanie korekcyjne (Reed-Solomon)
                    correction_data = self.error_correction_code.encode(packet) # Koduje dane korekcyjne na podstawie oryginalnych danych
                    print("Suma Kontrolna zakodowoana: ", correction_data)

                    # Transmisja samych kodów korekcyjnych
                    transmitted_correction_codes = self.channel.channel_transmit(correction_data)
                    print("Suma kontrolna po transmisji przez kanał:", transmitted_correction_codes)

                    # Dodanie kodów korekcyjnych do całości
                    combined_data = transmitted_data + correction_data

                    # Krok 4: Dekodowanie korekcyjne
                    decoded_data = self.error_correction_code.decode(combined_data)
                    print(f"Dane po dekodowaniu korekcyjnym (bez kodów korekcyjnych): {decoded_data}")
                    if decoded_data is None:
                        print(f"Błąd korekcji Reed-Solomon dla pakietu {packet_num} przy próbie {retries}")
                        continue

                    print("Dane po dekodowaniu korekcyjnym (RS):", decoded_data)

                    # Dekodowanie detekcyjne
                    final_data = self.error_detection_code.decode(decoded_data)
                    if final_data is not None:
                        # Weryfikacja sumy kontrolnej na ramce
                        if frame.checksum == self.error_detection_code.calculate_checksum(final_data):
                            print("Suma kontrolna jest poprawna.")
                            success = True
                            retransmission_counts[retries+1] += 1
                            received_data.extend(final_data)  # Dodajemy pakiet po transmisji do skumulowanych danych
                            print(f"Pakiet nr {packet_num} poprawnie odebrany przy próbie nr {retries + 1}.\n")
                        else:
                            print(f"Błąd detekcji w pakiecie nr {packet_num} po transmisji - nieprawidłowa suma kontrolna.")
                    else:
                        print(f"Błąd detekcji w pakiecie nr {packet_num} po transmisji.")
                else:
                    success = True
                    received_data.extend(decoded_data)
                    retransmission_counts[retries] += 1
                    print(f"Pakiet nr {packet_num} został odebrany poprawnie bez użycia kodów detekcyjnych")

            if not success:
                # received_data.extend([0] * 64) # Tutaj było na czarno
                received_data.extend([random.randint(0, 255) for _ in range(64)]) # Tutaj bardziej losowy jest szum
                errors_detected += 1
                print(f"Pakiet nr {packet_num} nie udało się poprawnie przesłać po 10 próbach.\n")

        # Wyświetlanie wyników
        print(f"\nIlość pakietów przepuszczonych z błędem: {errors_detected}")
        print("Statystyka pakietów przesyłanych za X razem:")
        for i, count in enumerate(retransmission_counts[1:], start=1):
            print(f"{i}: {count}")
        print(f"Pakiety przesłane powyżej 10 razy: {retransmission_counts[10] + retransmission_counts[11]}")

        # Wyświetlanie statystyk kanału
        if isinstance(self.channel.channel, GilbertElliottChannel):
            good_percentage, bad_percentage = self.channel.channel.get_channel_statistics()
            print(f"\nTyle % czasu kanał przebywał w stanie dobrym: {good_percentage:.2f}%")
            print(f"Tyle % czasu kanał przebywał w stanie złym: {bad_percentage:.2f}%")

        # Konwersja odebranych danych z powrotem do obrazu i zapisanie
        self.image_handler.bytes_to_image(bytes(received_data), self.output_path)
        print(f"Obraz został zapisany jako {self.output_path}")

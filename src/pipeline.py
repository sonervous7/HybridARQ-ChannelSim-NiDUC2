import random
from channel import Channel
from error_detection_code import ParityCode, CRC8, CRC16, CRC32
from error_correction_code import ErrorCorrectionCode
from image_handler import ImageHandler
from gilbert_elliott_channel import GilbertElliottChannel
from frame import Frame
from src.column_plots import PlotGenerator
import logging


# Konfiguracja logowania informacji
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Pipeline:
    def __init__(self, image_path, output_path):
        self.image_handler = ImageHandler(image_path)
        self.output_path = output_path
        self.channel = None
        self.error_detection_code = None
        self.error_correction_code = None

    def select_type(self):
        choice = 0
        while choice != 1 and choice != 2:
            logger.info("Wybierz co chcesz transmitować:")
            logger.info("1. Symulacja transmisji bitów")
            logger.info("2. Symulacja transmisji obrazka")
            try:
                choice = int(input("Twój wybór: "))
            except IOError:
                choice = 1
            if choice == 1:
                self.bit_array_transmission()
            elif choice == 2:
                self.run_image_transmission()
            else:
                logger.error("Niepoprawny wybór, spróbuj ponownie")

    def select_channel(self):
        logger.info("Wybierz kanał transmisji:")
        logger.info("1. Binary Symmetric Channel (BSC)")
        logger.info("2. Gilbert-Elliott Channel")
        try:
            choice = int(input("Twój wybór: "))
        except IOError:
            choice = 1

        if choice == 1:
            ber = float(input("Podaj prawdopodobieństwo błędu bitu (0-1) dla BSC: "))
            self.channel = Channel(channel_type="BSC", ber=ber)
        elif choice == 2:
            good_to_bad = float(input("Podaj wartość dla goodToBadProbability: "))
            bad_to_good = float(input("Podaj wartość dla badToGoodProbability: "))
            try:
                good_error_prob = float(
                    input("Podaj wartość dla goodChannelErrorProbability: ")
                )
                bad_error_prob = float(
                    input("Podaj wartość dla badChannelErrorProbability: ")
                )
            except IOError:
                good_error_prob = 0.5
                bad_error_prob = 0.01
            self.channel = Channel(
                channel_type="GilbertElliott",
                good_to_bad=good_to_bad,
                bad_to_good=bad_to_good,
                good_error_prob=good_error_prob,
                bad_error_prob=bad_error_prob,
            )
        else:
            logger.error("Niepoprawny wybór kanału transmisji.")
            return False
        return True

    def select_error_detection_code(self):
        logger.info("Wybierz kod detekcyjny:")
        logger.info("1. Bit parzystości")
        logger.info("2. CRC8")
        logger.info("3. CRC16")
        logger.info("4. CRC32")
        try:
            choice = int(input("Twój wybór: "))
        except IOError:
            choice = 1
        if choice == 1:
            self.error_detection_code = ParityCode()
        elif choice == 2:
            self.error_detection_code = CRC8()
        elif choice == 3:
            self.error_detection_code = CRC16()
        elif choice == 4:
            self.error_detection_code = CRC32()
        else:
            logger.error("Niepoprawny wybór kodu detekcyjnego.")
            return False
        return True

    def select_error_correction_code(self):
        logger.info("Wybierz kod korekcyjny:")
        logger.info("1. Reed-Solomon")
        try:
            choice = int(input("Twój wybór: "))
            correction_number = int(
                input("Wpisz wybraną długość kodu korekcyjnego w bajtach: ")
            )
        except IOError:
            choice = 1
            correction_number = 8
        if choice == 1:
            self.error_correction_code = ErrorCorrectionCode(
                correction_number
            )  # Liczba symboli korekcyjnych (długość kodu w bajtach) RS
        else:
            logger.error("Niepoprawny wybór kodu korekcyjnego.")
            return False
        return True

    def bit_array_transmission(self):
        self.select_channel()
        self.select_error_detection_code()
        self.select_error_correction_code()

        # Pobieranie tablicy bitów od użytkownika
        logger.info("Wprowadź tablicę bitów, oddzielając je spacjami (np. 1 0 1 0 1):")
        try:
            bit_array = list(map(int, input().split()))
        except IOError:
            bit_array = {1, 0, 1, 0, 1}
        logger.info("Oryginalne bity:", bit_array)

        # Kodowanie detekcyjne
        detected_bits = self.error_detection_code.encode_bits(bit_array)
        logger.info("Zakodowane bity detekcyjne:", detected_bits)

        # Transmisja przez kanał
        transmitted_bits = self.channel.channel_transmit(detected_bits, as_bits=True)
        transmitted_bits = list(map(int, transmitted_bits))
        logger.info("Bity po transmisji przez kanał:", transmitted_bits)

        # Dekodowanie detekcyjne
        decoded_bits = self.error_detection_code.decode_bits(transmitted_bits)
        logger.info("Bity po dekodowaniu detekcyjnym:", decoded_bits)

        if decoded_bits is None:
            logger.error(
                "Błąd detekcji. Generowanie i retransmisja kodów korekcyjnych..."
            )

            # Kodowanie korekcyjne
            correction_bits = self.error_correction_code.encode_bits(bit_array)
            logger.info("Kody korekcyjne:", correction_bits)

            # Transmisja kodów korekcyjnych
            transmitted_correction_bits = self.channel.channel_transmit(
                correction_bits, as_bits=True
            )
            transmitted_correction_bits = list(
                map(int, transmitted_correction_bits)
            )  # Konwersja NumPy do listy

            logger.info("Kody korekcyjne po transmisji:", transmitted_correction_bits)

            # Połączenie danych i kodów korekcyjnych
            combined_bits = transmitted_bits + transmitted_correction_bits
            logger.info("Połączone bity:", combined_bits)

            # Dekodowanie korekcyjne
            decoded_bits = self.error_correction_code.decode_bits(
                combined_bits, bit_array
            )
            if decoded_bits is None:
                logger.error("Nie udało się poprawić danych nawet po korekcji!")
                return

        # Wyświetlanie ostatecznych wyników
        logger.info("Ostateczne zdekodowane bity:", decoded_bits)

        # Porównanie oryginalnych i zdekodowanych bitów
        if decoded_bits == bit_array:
            logger.info("Dane zostały poprawnie przesłane!")
        else:
            logger.warning("Niektóre dane zostały utracone lub zmodyfikowane.")

    def run_image_transmission(self):
        self.select_channel()
        self.select_error_detection_code()
        self.select_error_correction_code()

        data = (
            self.image_handler.image_to_bytes()
        )  # Załaduj obraz i konwertuj na dane bajtowe
        header = data[:54]
        pixel_data = data[54:]
        logger.info("Uruchamianie symulacji transmisji obrazu...")

        packets = [
            pixel_data[i : i + 64] for i in range(0, len(pixel_data), 64)
        ]  # Dzielenie danych na pakiety 64-bajtowe
        logger.info(f"Rozmiar danych: {len(pixel_data)} bajtów")
        logger.info(f"Liczba pakietów: {len(packets)}")
        retransmission_counts = [0] * 12  # Licznik transmisji za X razem
        errors_detected = 0  # Liczba pakietów, które nie zostały poprawnie odebrane
        received_data = bytearray(header)  # Inicjalizuj otrzymane dane nagłówkiem

        for packet_num, packet in enumerate(packets, start=1):
            logger.info(f"\n--- Pakiet nr {packet_num} ---")
            logger.info("Dane oryginalne:", packet)

            frame = Frame.create_frame(packet_num, packet, self.error_detection_code)

            success = False
            retries = 0

            while not success and retries < 10:
                retries += 1
                logger.info(f"Próba nr {retries} dla pakietu {packet_num}")

                # Kodowanie detekcyjne
                detected_data = self.error_detection_code.encode(packet)
                logger.info("Dane po kodowaniu detekcyjnym:", detected_data)

                # Transmisja przez kanał
                transmitted_data = self.channel.channel_transmit(detected_data)
                logger.info("Dane po transmisji przez kanał:", transmitted_data)

                # Dekodowanie detekcyjne - aby sprawdzić czy potrzebna jest retransmisja z kodami korekcyjnymi
                decoded_data = self.error_detection_code.decode(transmitted_data)
                if decoded_data is None:
                    # Kodowanie detekcyjne ponownie
                    # detected_data = self.error_detection_code.encode(packet)
                    # print("Dane po kodowaniu detekcyjnym:", detected_data)

                    # Kodowanie korekcyjne (Reed-Solomon)
                    correction_data = self.error_correction_code.encode(
                        packet
                    )  # Koduje dane korekcyjne na podstawie oryginalnych danych
                    logger.info("Suma Kontrolna zakodowana: ", correction_data)

                    # Transmisja samych kodów korekcyjnych
                    transmitted_correction_codes = self.channel.channel_transmit(
                        correction_data
                    )
                    logger.info(
                        "Suma kontrolna po transmisji przez kanał:",
                        transmitted_correction_codes,
                    )

                    # Dodanie kodów korekcyjnych do całości
                    combined_data = transmitted_data + correction_data

                    # Krok 4: Dekodowanie korekcyjne
                    decoded_data = self.error_correction_code.decode(combined_data)
                    logger.info(
                        f"Dane po dekodowaniu korekcyjnym (bez kodów korekcyjnych): {decoded_data}"
                    )
                    if decoded_data is None:
                        logger.error(
                            f"Błąd korekcji Reed-Solomon dla pakietu {packet_num} przy próbie {retries}"
                        )
                        continue

                    logger.info("Dane po dekodowaniu korekcyjnym (RS):", decoded_data)

                    # Dekodowanie detekcyjne
                    final_data = self.error_detection_code.decode(decoded_data)
                    if final_data is not None:
                        # Weryfikacja sumy kontrolnej na ramce
                        if (
                            frame.checksum
                            == self.error_detection_code.calculate_checksum(final_data)
                        ):
                            logger.info("Suma kontrolna jest poprawna.")
                            success = True
                            retransmission_counts[retries + 1] += 1
                            received_data.extend(
                                final_data
                            )  # Dodajemy pakiet po transmisji do skumulowanych danych
                            logger.info(
                                f"Pakiet nr {packet_num} poprawnie odebrany przy próbie nr {retries + 1}.\n"
                            )
                        else:
                            logger.error(
                                f"Błąd detekcji w pakiecie nr {packet_num} po transmisji - nieprawidłowa suma kontrolna."
                            )
                    else:
                        logger.error(
                            f"Błąd detekcji w pakiecie nr {packet_num} po transmisji."
                        )
                else:
                    success = True
                    received_data.extend(decoded_data)
                    retransmission_counts[retries] += 1
                    logger.info(
                        f"Pakiet nr {packet_num} został odebrany poprawnie bez użycia kodów korekcyjnych"
                    )

            if not success:
                # received_data.extend([0] * 64) # Tutaj było na czarno
                received_data.extend(
                    [random.randint(0, 255) for _ in range(64)]
                )  # Tutaj bardziej losowy jest szum
                errors_detected += 1
                logger.error(
                    f"Pakiet nr {packet_num} nie udało się poprawnie przesłać po 10 próbach.\n"
                )



        # Wyświetlanie wyników
        logger.info(f"\nIlość pakietów przepuszczonych z błędem: {errors_detected}")
        logger.info("Statystyka pakietów przesyłanych za X razem:")
        for i, count in enumerate(retransmission_counts[1:], start=1):
            logger.info(f"{i}: {count}")
        logger.info(
            f"Pakiety przesłane powyżej 10 razy: {retransmission_counts[10] + retransmission_counts[11]}"
        )

        success_rate = (len(packets) - errors_detected) / len(packets)
        print(f"Success Rate: {success_rate * 100}%")

        # Wyświetlanie statystyk kanału
        if isinstance(self.channel.channel, GilbertElliottChannel):
            (
                good_percentage,
                bad_percentage,
            ) = self.channel.channel.get_channel_statistics()
            logger.info(
                f"\nTyle % czasu kanał przebywał w stanie dobrym: {good_percentage:.2f}%"
            )
            logger.info(
                f"Tyle % czasu kanał przebywał w stanie złym: {bad_percentage:.2f}%"
            )

        # Konwersja odebranych danych z powrotem do obrazu i zapisanie
        self.image_handler.bytes_to_image(bytes(received_data), self.output_path)
        logger.info(f"Obraz został zapisany jako {self.output_path}")

        plot_generator = PlotGenerator()
        plot_generator.plot_transmissions(retransmission_counts)

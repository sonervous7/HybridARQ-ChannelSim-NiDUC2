import random


class GilbertElliottChannel:
    def __init__(self, good_to_bad, bad_to_good, good_error_prob, bad_error_prob):
        # Inicjalizacja kanału i parametrów przejść
        self.good_to_bad = good_to_bad
        self.bad_to_good = bad_to_good
        self.good_error_prob = good_error_prob
        self.bad_error_prob = bad_error_prob
        self.state = 'good'  # Początkowy stan kanału
        self.good_state_count = 0  # Licznik czasu w stanie dobrym
        self.bad_state_count = 0  # Licznik czasu w stanie złym

    def transmit(self, data):
        transmitted_data = []
        for bit in data:
            if self.state == 'good':
                self.good_state_count += 1
                if random.random() < self.good_error_prob:
                    transmitted_data.append(1 - bit)  # Przełącz bit, jeśli jest błąd
                else:
                    transmitted_data.append(bit)
                if random.random() < self.good_to_bad:
                    self.state = 'bad'
            else:  # Stan zły
                self.bad_state_count += 1
                if random.random() < self.bad_error_prob:
                    transmitted_data.append(1 - bit)  # Przełącz bit, jeśli jest błąd
                else:
                    transmitted_data.append(bit)
                if random.random() < self.bad_to_good:
                    self.state = 'good'
        return transmitted_data

    def get_channel_statistics(self):
        total = self.good_state_count + self.bad_state_count
        good_state_percentage = (self.good_state_count / total) * 100 if total > 0 else 0
        bad_state_percentage = (self.bad_state_count / total) * 100 if total > 0 else 0
        return good_state_percentage, bad_state_percentage


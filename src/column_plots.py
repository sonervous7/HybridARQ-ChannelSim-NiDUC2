import matplotlib.pyplot as plt
import logging

class PlotGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def plot_transmissions(self, retransmission_counts):
        # Usunięcie zerowych wartości z początku listy
        retransmission_counts = retransmission_counts[1:]

        x_values = range(1, len(retransmission_counts) + 1)  # Oś X (ilość transmisji)
        y_values = retransmission_counts  # Oś Y (ilość pakietów)

        plt.figure(figsize=(10, 6))
        plt.bar(x_values, y_values, width=0.6, edgecolor="black", alpha=0.75)
        plt.xlabel("Ilość transmisji", fontsize=12)
        plt.ylabel("Ilość pakietów", fontsize=12)
        plt.title("Rozkład ilości transmisji dla przesłanych pakietów", fontsize=14)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.xticks(x_values)
        plt.tight_layout()

        # Zapis wykresu do pliku lub wyświetlenie
        plt.savefig("transmissions_distribution.png")
        plt.show()
        self.logger.info("Wykres został wygenerowany i zapisany jako 'transmissions_distribution.png'")

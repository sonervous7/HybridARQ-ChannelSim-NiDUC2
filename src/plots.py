import matplotlib.pyplot as plt

# Dane dla wykresu
ber_values = [0.0001, 0.007, 0.01]
errors_detected = [0, 0, 2935]  # Przykładowe dane: liczba pakietów przepuszczonych z błędem
success_rates = [100, 48.76, 4.66]  # Procent poprawnie przesłanych danych

def bsc_plot1():
    # Wykres liczby błędów
    plt.figure(figsize=(10, 6))
    plt.plot(ber_values, errors_detected, marker='o', label='Liczba błędów wykrytych')
    plt.xscale('log')
    plt.xlabel('BER (Bit Error Rate)')
    plt.ylabel('Liczba błędów')
    plt.title('Liczba błędów w zależności od BER (BSC)')
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.show()

# Wykres skuteczności
    plt.figure(figsize=(10, 6))
    plt.plot(ber_values, success_rates, marker='o', label='Skuteczność transmisji (%)')
    plt.xscale('log')
    plt.xlabel('BER (Bit Error Rate)')
    plt.ylabel('Skuteczność (%)')
    plt.title('Skuteczność transmisji w zależności od BER (BSC)')
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.show()

def bar_plot_bsc():

    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    values = [1788, 762, 333, 112, 44, 18, 8, 5, 0, 2]
    plt.bar(nums, values)
    plt.xlabel('Próba')
    plt.ylabel('Ilość przesłanych pakietów w n-próbie')
    plt.show()
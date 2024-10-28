import math
import matplotlib.pyplot as plt
import numpy as np

def generateDeviation(variance, u):
    # Generujemy odchylenie na podstawie wartości sinusoidy w punkcie x
    c = math.sqrt(6 * variance)  # Stała do obliczenia odchylenia
    if u <= 0.5:
        base_deviation = c * (math.sqrt(2 * u) - 1)
    else:
        base_deviation = c * (1 - math.sqrt(2 - (2 * u)))
    return base_deviation

# Amplituda fali
amplitude = 1
# Okres fali
period = 6 * math.pi
# Liczba punktów na osi x
length = 1000
# Odległość między punktami na osi x
step = period / length
# Definicja fali sinusoidalnej
sin = [amplitude * math.sin(x) for x in np.arange(0, period, step)]

uValues = open("uValues.txt", 'r').read().splitlines()
uValues = [float(i) for i in uValues]

# wartości od 0.1 do 10.0 z krokiem 0.1
variance_values = np.arange(0, 2.1, 0.1)

# Funkcje do obliczania średniej ruchomej
def moving_average(signal, H):
    smoothed_signal = []
    for i in range(len(signal)):
        # Filtrujemy tylko istniejące wartości (nie `None`)
        window = [signal[j] for j in range(max(0, i - H + 1), i + 1) if signal[j] is not None]
        # Obliczamy średnią tylko, jeśli mamy jakieś wartości
        smoothed_signal.append(np.mean(window) if window else None)
    return smoothed_signal

# Funkcja do obliczania średniej ruchomej z H ostatnich punktów, nawet jeśli niektóre z nich są `None`
def moving_average_with_None(signal, H):
    smoothed_signal = []
    for i in range(len(signal)):
        # Wyznaczamy zakres okna do uśredniania
        start = max(0, i - H + 1)
        end = i + 1
        window = [signal[j] for j in range(start, end) if signal[j] is not None]
        if not window:
            estimated_value = np.mean([x for x in signal if x is not None])
        else:
            estimated_value = np.mean(window)
        smoothed_signal.append(estimated_value)
    return smoothed_signal

# Funkcja do obliczania MSE
def calculate_mse(original, smoothed):
    mse_values = [(o - s) ** 2 for o, s in zip(original, smoothed) if s is not None]
    return np.mean(mse_values)

# Analiza dla różnych wartości wariancji
optimal_H_values = []
optimal_mse_values = []


for variance in variance_values:
    copyOfUValues = uValues.copy()
    variance = round(variance, 1)
    print(f'Calculating for Variance: {variance}')
    # Generowanie zaszumionego sygnału tylko dla co 10. punktu
    #noisy_signal = [sin[i] + generateDeviation(variance) if i % 10 == 0 else None 
                    #for i in enumerate(np.arange(0, period, step))]
    
    noisy_signal = [sin[i] + generateDeviation(variance, copyOfUValues.pop(0)) for i, x in enumerate(np.arange(0, period, step))]

    H_values = range(1, 100)
    mse_values = []
    for H in H_values:
        smoothed_signal = moving_average(noisy_signal, H)
        mse = calculate_mse(sin, smoothed_signal)
        mse_values.append(mse)

    # Wybierz najlepsze H na podstawie minimalnego MSE
    best_H = H_values[np.argmin(mse_values)]
    optimal_H_values.append(best_H)
    optimal_mse_values.append(min(mse_values))
    smoothed_best = moving_average(noisy_signal, best_H)

    # Wykres zaszumionego sygnału
    plt.figure()
    plt.plot([x if x is not None else np.nan for x in noisy_signal], label='Noisy Signal', color='red', linestyle='solid', marker='o', markersize=1)
    plt.plot(sin, label='Original Signal', linestyle='solid', color='blue')
    plt.title(f'Noisy Signal (Variance={variance})')
    plt.xlabel('X')
    plt.legend()
    plt.tight_layout()
    # plt.show()
    plt.savefig(f'noisy_signal_{variance}.png')

    # Wykres wygładzonego sygnału dla optymalnego H
    plt.figure()
    plt.plot([x if x is not None else np.nan for x in smoothed_best], label=f'Smoothed Signal (H={best_H})', color='green')
    plt.plot(sin, label='Original Signal', linestyle='solid', color='blue')
    plt.title(f'Smoothed Signal with Optimal H={best_H} (Variance={variance})')
    plt.xlabel('X')
    plt.legend()
    plt.tight_layout()
    # plt.show()
    plt.savefig(f'smoothed_signal_{variance}.png')

    # Wykres MSE w zależności od H
    plt.figure()
    plt.plot(H_values, mse_values, marker='o', color='purple', markersize=3)
    plt.title(f'MSE vs H (Variance={variance})')
    plt.xlabel('H')
    plt.ylabel('MSE')
    plt.legend(['MSE'])
    plt.tight_layout()
    # plt.show()
    plt.savefig(f'mse_{variance}.png')
    
    plt.close("all")

# Wykres MSE dla optymalnego H w zależności od wartości wariancji
plt.figure()
plt.plot(variance_values, optimal_mse_values, marker='o', color='orange', markersize=3)
plt.title('MSE for Optimal H vs Variance')
plt.xlabel('Variance')
plt.ylabel('MSE')
plt.legend(['MSE'])
plt.tight_layout()
plt.savefig('mse_optimal_vs_variance.png')
plt.show()
plt.close()
import math
import matplotlib.pyplot as plt
import numpy as np

def generateDeviation(x):
    # Generujemy odchylenie na podstawie wartości sinusoidy w punkcie x
    # Używamy rozkładu trójkątnego, gdzie:
    # - minimum to -1, maksimum to 1, a moda to 1/2 (środek)
    base_deviation = np.random.triangular(-1, 1/2, 1) * math.sin(x)
    return base_deviation

# Okres fali
period = 6 * math.pi
# Liczba punktów na osi x
length = 1000
# Odległość między punktami na osi x
step = period / length
# Definicja fali sinusoidalnej
sin = [math.sin(x) for x in np.arange(0, period, step)]

# Generowanie zaszumionego sygnału tylko dla co 10. punktu
noisy_signal = [sin[i] + generateDeviation(x) if i % 10 == 0 else None 
                for i, x in enumerate(np.arange(0, period, step))]

# Funkcja do obliczania średniej ruchomej z H ostatnich punktów, pomijając wartości `None`
def moving_average(signal, H):
    smoothed_signal = []
    for i in range(len(signal)):
        # Filtrujemy tylko istniejące wartości (nie `None`)
        window = [signal[j] for j in range(max(0, i - H + 1), i + 1) if signal[j] is not None]
        # Obliczamy średnią tylko, jeśli mamy jakieś wartości
        smoothed_signal.append(np.mean(window) if window else None)
    return smoothed_signal


# Funkcja do obliczania średniej ruchoemj z H ostatnich punktów, nawet jeśli niektóre z nich są `None`
def moving_average_with_None(signal, H):
    smoothed_signal = []
    for i in range(len(signal)):
        # Wyznaczamy zakres okna do uśredniania
        start = max(0, i - H + 1)
        end = i + 1
        
        # Zbieramy dostępne wartości (pomijamy None)
        window = [signal[j] for j in range(start, end) if signal[j] is not None]
        
        # Jeśli okno jest puste (brak dostępnych wartości), przyjmujemy wartość 0 lub inny zastępczy sposób
        # Tutaj dla uproszczenia użyjemy średniej z całego sygnału jako wartości zastępczej.
        if not window:
            estimated_value = np.mean([x for x in signal if x is not None])  # Uśrednianie po dostępnych punktach
        else:
            # W przeciwnym razie obliczamy średnią z dostępnych wartości
            estimated_value = np.mean(window)
        
        smoothed_signal.append(estimated_value)
    
    return smoothed_signal


# Funkcja do obliczania MSE - bierzemy tylko te punkty, gdzie zaszumiony sygnał nie jest None
def calculate_mse(original, smoothed):
    mse_values = [(o - s) ** 2 for o, s in zip(original, smoothed) if s is not None]
    return np.mean(mse_values)

# Analiza dla różnych wartości H
H_values = range(1, 100)  # Zakres wartości H do przetestowania
mse_values = []

for H in H_values:
    smoothed_signal = moving_average_with_None(noisy_signal, H)
    mse = calculate_mse(sin, smoothed_signal)  # Obliczamy MSE między oryginalnym sygnałem a wygładzonym
    mse_values.append(mse)

# Wykresy
figure, axis = plt.subplots(3, 1, figsize=(10, 12))

# Wykres zaszumionego sygnału
axis[0].plot(sin, label='Original Signal', linestyle='solid', color='blue')
axis[0].plot([x if x is not None else np.nan for x in noisy_signal], label='Noisy Signal', color='red', linestyle='solid', marker='o', markersize=1)
axis[0].set_title('Noisy Signal')
axis[0].set_xlabel('X')
axis[0].legend()

# Wybierz najlepsze H na podstawie minimalnego MSE
best_H = H_values[np.argmin(mse_values)]
smoothed_best = moving_average_with_None(noisy_signal, best_H)

# Rysowanie wygładzonego sygnału dla optymalnego H
axis[1].plot(sin, label='Original Signal', linestyle='solid', color='blue')
axis[1].plot([x if x is not None else np.nan for x in smoothed_best], 
             label=f'Smoothed Signal (H={best_H})', color='green')
axis[1].set_title(f'Smoothed Signal with Optimal H={best_H}')
axis[1].set_xlabel('X')
axis[1].legend()


# Wykres MSE w zależności od H
axis[2].plot(H_values, mse_values, marker='o', color='purple', markersize=3)
axis[2].set_title('MSE vs H')
axis[2].set_xlabel('H')
axis[2].set_ylabel('MSE')
axis[2].legend(['MSE'])

plt.tight_layout()
plt.show()

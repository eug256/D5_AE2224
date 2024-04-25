from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt
import time

start = time.time()


N=600
T=1/800

t = np.linspace(0.0, N*T, N, endpoint=False)
y = np.sin(50.0 * 2.0*np.pi*t) + 0.5*np.sin(80.0 * 2.0*np.pi*t)

yf = fft(y)
dt = t[1] - t[0]
freq = fftfreq(len(y), dt)
freq_0 = []
amplitude_spectrum_0 = []
amplitude_spectrum = 2*np.abs(yf)

for i in range(len(freq)):
    if freq[i] >= 0:
        freq_0.append(freq[i])
        amplitude_spectrum_0.append(amplitude_spectrum[i])

end = time.time()
print(end - start)

plt.plot(freq_0,amplitude_spectrum_0)
plt.show()


# Number of sample points

start = time.time()

N = 600

# sample spacing

T = 1.0 / 800.0

x = np.linspace(0.0, N*T, N, endpoint=False)

y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)

yf = fft(y)

xf = fftfreq(N, T)[:N//2]

end = time.time()
print(end - start)

plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))

plt.grid()

plt.show()


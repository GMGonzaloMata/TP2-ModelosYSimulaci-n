import math
from collections import Counter

# Tabla de valores críticos de chi-cuadrado para alfa=0.05 y gl de 1 a 30
VALORES_CRITICOS = {
    1: 3.841, 2: 5.991, 3: 7.815, 4: 9.488, 5: 11.070,
    6: 12.592, 7: 14.067, 8: 15.507, 9: 16.919, 10: 18.307,
    11: 19.675, 12: 21.026, 13: 22.362, 14: 23.685, 15: 24.996,
    16: 26.296, 17: 27.587, 18: 28.869, 19: 30.144, 20: 31.410,
    21: 32.671, 22: 33.924, 23: 35.172, 24: 36.415, 25: 37.652,
    26: 38.885, 27: 40.113, 28: 41.337, 29: 42.557, 30: 43.773
}

# Test de Chi-Cuadrado
class ChiCuadradoTest:
    def __init__(self, generator, cantidad=100, clases=10):
        self.generator = generator
        self.n = cantidad
        self.k = clases
        self.frecuencias = [0] * self.k

    def generar_numeros(self):
        for _ in range(self.n):
            r = self.generator.next_float()
            index = min(int(r * self.k), self.k - 1)
            self.frecuencias[index] += 1

    def calcular_chi_cuadrado(self):
        esperada = self.n / self.k
        chi2 = sum(((obs - esperada) ** 2) / esperada for obs in self.frecuencias)
        return chi2

    def resultado(self):
        self.generar_numeros()
        chi2 = self.calcular_chi_cuadrado()
        grados_libertad = self.k - 1
        chi_critico = VALORES_CRITICOS.get(grados_libertad, None)
        if chi_critico is None:
            conclusion = "No disponible: grados de libertad fuera de rango"
        else:
            conclusion = "No se rechaza la hipótesis" if chi2 < chi_critico else "Se rechaza la hipótesis"
        return self.frecuencias, chi2, chi_critico, conclusion
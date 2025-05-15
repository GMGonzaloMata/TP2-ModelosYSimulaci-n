class FibonacciRNG:
    def __init__(self, seed1=1, seed2=2, modulo=1000):
        """
        Constructor del generador.
        - seed1 y seed2: valores iniciales de la secuencia (X_{n-2} y X_{n-1}).
        - modulo: define el rango de los números generados (0 a m-1).
        """
        self.x1 = seed1   # Primer valor de la secuencia
        self.x2 = seed2   # Segundo valor de la secuencia
        self.m = modulo   # Módulo (tamaño del rango de salida)

    def next(self):
        """
        Genera el siguiente número pseudoaleatorio usando la fórmula de Fibonacci:
        X_n = (X_{n-1} + X_{n-2}) mod m
        """
        xn = (self.x1 + self.x2) % self.m  # Suma los dos anteriores y aplica el módulo
        self.x1, self.x2 = self.x2, xn     # Desplaza los valores para la próxima llamada
        return xn                          # Devuelve el nuevo número

    def next_float(self):
        """
        Devuelve un número pseudoaleatorio entre 0 y 1.
        Ideal para simulaciones que requieren probabilidades o tiempos aleatorios.
        """
        return self.next() / self.m  # Normaliza el número dividiéndolo por el módulo
    
    def next_delay(self, min_ms=1500, max_ms=5000):
        """
        Devuelve un tiempo de espera aleatorio en milisegundos entre min_ms y max_ms
        """
        rnd = self.next_float()
        return int(min_ms + rnd * (max_ms - min_ms))

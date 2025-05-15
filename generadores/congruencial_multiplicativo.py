class CongruencialMultiplicativoRNG:
    def __init__(self, seed=7, a=5, m=97):
        """
        Constructor:
        - seed: valor inicial
        - a: multiplicador
        - m: módulo
        """
        self.x = seed
        self.a = a
        self.m = m

    def next(self):
        """
        Genera el siguiente número: X_{n+1} = (a * X_n) % m
        """
        self.x = (self.a * self.x) % self.m
        return self.x

    def next_float(self):
        """
        Devuelve un número entre 0 y 1.
        """
        return self.next() / self.m
    
    def next_delay(self, min_ms=1500, max_ms=5000):
        """
        Devuelve un tiempo de espera aleatorio en milisegundos entre min_ms y max_ms
        """
        rnd = self.next_float()
        return int(min_ms + rnd * (max_ms - min_ms))

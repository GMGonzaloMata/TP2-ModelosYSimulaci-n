class CongruencialMixtoRNG:
    def __init__(self, seed=1, a=17, c=43, m=100):
        """
        Constructor:
        - seed: semilla inicial
        - a: multiplicador
        - c: incremento
        - m: módulo
        """
        self.x = seed
        self.a = a
        self.c = c
        self.m = m

    def next(self):
        """
        Aplica la fórmula: X_{n+1} = (a * X_n + c) % m
        """
        self.x = (self.a * self.x + self.c) % self.m
        return self.x

    def next_float(self):
        """
        Devuelve un valor entre 0 y 1.
        """
        return self.next() / self.m
    
    def next_delay(self, min_ms=1500, max_ms=5000):
        """
        Devuelve un tiempo de espera aleatorio en milisegundos entre min_ms y max_ms
        """
        rnd = self.next_float()
        return int(min_ms + rnd * (max_ms - min_ms))

class CongruencialAditivoRNG:
    def __init__(self, seeds, m=100):
        """
        Constructor:
        - seeds: lista de semillas iniciales (al menos 2)
        - m: módulo
        """
        self.history = seeds[:]  # Copia de las semillas
        self.k = len(seeds)
        self.m = m

    def next(self):
        """
        Genera el próximo valor usando los dos últimos:
        X_n = (X_{n-1} + X_{n-k}) % m
        """
        xn = (self.history[-1] + self.history[-self.k]) % self.m
        self.history.append(xn)  # Se agrega a la historia
        return xn

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

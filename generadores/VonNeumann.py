class VonNeumannRNG:
    def __init__(self, seed=6752, digits=4):
        """
        Constructor del generador.
        - seed: semilla inicial, debe tener la misma cantidad de dígitos que 'digits'.
        - digits: cantidad fija de dígitos que se mantendrán en cada iteración.
        """
        self.seed = seed
        self.digits = digits

    def next(self):
        """
        Genera el siguiente número pseudoaleatorio usando el método de cuadrados medios:
        1. Eleva la semilla al cuadrado.
        2. Extrae los dígitos centrales del resultado.
        3. Esos dígitos se convierten en la nueva semilla.
        4. Retorna ese valor como número pseudoaleatorio.
        """
        squared = str(self.seed ** 2).zfill(self.digits * 2)  # Cuadrado y relleno con ceros
        mid = len(squared) // 2                              # Índice central
        start = mid - self.digits // 2                       # Desde dónde extraer
        end = start + self.digits                            # Hasta dónde extraer
        self.seed = int(squared[start:end])                  # Nueva semilla
        return self.seed                                     # Retorna el número generado

    def next_float(self):
        """
        Devuelve un número entre 0 y 1.
        Se obtiene dividiendo el número generado por 10^digits.
        """
        return self.next() / (10 ** self.digits)
    
    def next_delay(self, min_ms=1500, max_ms=5000):
        """
        Devuelve un tiempo de espera aleatorio en milisegundos entre min_ms y max_ms
        """
        rnd = self.next_float()
        return int(min_ms + rnd * (max_ms - min_ms))
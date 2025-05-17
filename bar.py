import tkinter as tk
import math
from tkinter import messagebox
import random
import tkinter as tk
from tkinter import ttk
from generadores.VonNeumann import VonNeumannRNG
from generadores.fibonacci import FibonacciRNG
from generadores.congruencial_aditivo import CongruencialAditivoRNG
from generadores.congruencial_multiplicativo import CongruencialMultiplicativoRNG
from generadores.congruencial_mixto import CongruencialMixtoRNG

class BarSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Bar Universitario")
        self.root.geometry("600x700")
        self.contador = 1
        self.total_atendidos = 0
        self.tiempos_espera = []

        # Colas
        self.cola_caja = []
        self.cola_barra = []

        self.atendiendo_caja = False
        self.atendiendo_barra = False
        self.simulando = False

        # Simulación
        self.rng = VonNeumannRNG(seed=1234)
        self.generadores = {
            "Von Neumann": VonNeumannRNG(seed=1234),
            "Fibonacci":FibonacciRNG(),
            "Congruencial Mixto":CongruencialMixtoRNG(),
            "Congruencial Aditivo":CongruencialAditivoRNG(seeds=[1,2]),
            "Congruecnial Multiplicativo": CongruencialMultiplicativoRNG()
        }
        self.rng_nombre = tk.StringVar(value="Von Neumann")

        self.pedidos_posibles = {
            "Café": 2000,
            "Tostado": 3000,
            "Empanadas": 2500,
            "Jugos": 1800,
            "Tarta": 3200,
            "Sandwich": 2800,
            "Agua": 1000
        }

        # Interfaz
        tk.Label(root, text="🍽️ Bar - Univ. de la Cuenca del Plata", font=("Arial", 14, "bold")).pack(pady=10)
        # Inputs de configuración
        tk.Label(root, text="Cantidad de cajas:").pack()
        self.entry_cajas = tk.Entry(root)
        self.entry_cajas.insert(0, "1")
        self.entry_cajas.pack(pady=2)

        tk.Label(root, text="Cantidad de barras:").pack()
        self.entry_barras = tk.Entry(root)
        self.entry_barras.insert(0, "1")
        self.entry_barras.pack(pady=2)
        # Selección de generador
        tk.Label(root, text="Seleccionar método de generación:").pack()

        self.rng_nombre = tk.StringVar(value="Von Neumann")
        generador_menu = tk.OptionMenu(root, self.rng_nombre, *self.generadores.keys())
        generador_menu.pack(pady=5)

        # Contenedor para parámetros de generadores
        self.param_frame = tk.Frame(root)
        self.param_frame.pack(pady=5)
        self.parametros_inputs = {}

        # Mostrar campos por defecto
        self.mostrar_parametros(self.rng_nombre.get())

        # Actualizar parámetros al cambiar selección
        self.rng_nombre.trace_add("write", lambda *_: self.mostrar_parametros(self.rng_nombre.get()))
        
        # Botón de inicio
        self.boton_inicio = tk.Button(root, text="Iniciar Simulación", command=self.iniciar_simulacion)
        self.boton_inicio.pack(pady=10)

        # Caja
        tk.Label(root, text="🧾 En caja", font=("Arial", 12, "bold")).pack()
        self.lista_caja = tk.Listbox(root, width=50, height=6)
        self.lista_caja.pack(pady=5)

        # Barra
        tk.Label(root, text="🍴 En barra (esperando pedido)", font=("Arial", 12, "bold")).pack()
        self.lista_barra = tk.Listbox(root, width=50, height=6)
        self.lista_barra.pack(pady=5)

        # Estado
        self.estado_label = tk.Label(root, text="Estado: Esperando inicio...", fg="blue")
        self.estado_label.pack(pady=10)

        # Estadísticas
        self.estadisticas_label = tk.Label(root, text="Media: 0 m | Máximo: 0 m")
        self.estadisticas_label.pack(pady=5)


        # Total atendidos
        self.total_atendidos_label = tk.Label(root, text="Total entregados: 0")
        self.total_atendidos_label.pack(pady=5)

    def mostrar_parametros(self, seleccion):
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        self.parametros_inputs = {}

        if seleccion == "Von Neumann":
            tk.Label(self.param_frame, text="Semilla(numero de 4 digitos):").pack()
            seed = tk.Entry(self.param_frame)
            seed.insert(0, "1234")
            seed.pack()
            self.parametros_inputs["seed"] = seed


        elif seleccion == "Fibonacci":
            tk.Label(self.param_frame, text="Semilla 1(Entero>0)=:").pack()
            s1 = tk.Entry(self.param_frame)
            s1.insert(0, "1")
            s1.pack()
            self.parametros_inputs["s1"] = s1

            tk.Label(self.param_frame, text="Semilla 2(Entero>0):").pack()
            s2 = tk.Entry(self.param_frame)
            s2.insert(0, "2")
            s2.pack()
            self.parametros_inputs["s2"] = s2

        elif seleccion == "Congruencial Aditivo":
            tk.Label(self.param_frame, text="Semillas (coma separadas):").pack()
            seeds = tk.Entry(self.param_frame)
            seeds.insert(0, "1,2,3")
            seeds.pack()
            self.parametros_inputs["seeds"] = seeds
            tk.Label(self.param_frame, text="m:").pack()
            m = tk.Entry(self.param_frame)
            m.insert(0, "1000")
            m.pack()

        elif seleccion == "Congruencial Mixto":
            for param, val in [("Semilla", "1"), ("a", "5"), ("c", "3"), ("m", "16")]:
                tk.Label(self.param_frame, text=f"{param}:").pack()
                entry = tk.Entry(self.param_frame)
                entry.insert(0, val)
                entry.pack()
                self.parametros_inputs[param.lower()] = entry

        elif seleccion == "Congruecnial Multiplicativo":
            for param, val in [("Semilla", "1"), ("a", "5"), ("m", "16")]:
                tk.Label(self.param_frame, text=f"{param}:").pack()
                entry = tk.Entry(self.param_frame)
                entry.insert(0, val)
                entry.pack()
                self.parametros_inputs[param.lower()] = entry

        elif seleccion == "Random (Python)":
            tk.Label(self.param_frame, text="Este generador no requiere configuración.").pack()
    def iniciar_simulacion(self):
        seleccion = self.rng_nombre.get()

        try:
            if seleccion == "Von Neumann":
                seed_text = self.parametros_inputs["seed"].get()
                if not seed_text.isdigit() or len(seed_text) != 4:
                    raise ValueError("La semilla debe ser un número entero de 4 dígitos.")
                seed = int(seed_text)
                self.rng = VonNeumannRNG(seed=seed, digits=4)

            elif seleccion == "Fibonacci":
                s1 = int(self.parametros_inputs["s1"].get())
                s2 = int(self.parametros_inputs["s2"].get())
                if s1 <= 0 or s2 <= 0:
                    raise ValueError("Las semillas deben ser enteros positivos.")
                if s1 == s2:
                    raise ValueError("Las semillas deben ser distintas.")
                self.rng = FibonacciRNG(s1, s2)

            elif seleccion == "Congruencial Aditivo":
                seeds_raw = self.parametros_inputs["seeds"].get().split(",")
                seeds = [int(x.strip()) for x in seeds_raw]
                if len(seeds) < 2:
                    raise ValueError("Debe ingresar al menos dos semillas separadas por coma.")
                if any(s < 0 for s in seeds):
                    raise ValueError("Las semillas deben ser números enteros no negativos.")
                self.rng = CongruencialAditivoRNG(seeds)

            elif seleccion == "Congruencial Mixto":
                seed = int(self.parametros_inputs["semilla"].get())
                a = int(self.parametros_inputs["a"].get())
                c = int(self.parametros_inputs["c"].get())
                m = int(self.parametros_inputs["m"].get())
                if m <= 0:
                    raise ValueError("El módulo 'm' debe ser mayor que cero.")
                if not (0 < a < m and 0 <= c < m and 0 <= seed < m):
                    raise ValueError("Los parámetros deben cumplir: 0 <= semilla <m, c < m y 0 < a < m .")
                self.rng = CongruencialMixtoRNG(seed=seed, a=a, c=c, m=m)

            elif seleccion == "Congruecnial Multiplicativo":
                seed = int(self.parametros_inputs["semilla"].get())
                a = int(self.parametros_inputs["a"].get())
                m = int(self.parametros_inputs["m"].get())
                if m <= 0:
                    raise ValueError("El módulo 'm' debe ser mayor que cero.")
                if not (0 < seed < m):
                    raise ValueError("La semilla debe estar en el rango (0, m).")
                if a <= 0 or math.gcd(a, m) != 1:
                    raise ValueError("El multiplicador 'a' debe ser positivo y coprimo con 'm'.")
                self.rng = CongruencialMultiplicativoRNG(seed=seed, a=a, m=m)

        except ValueError as ve:
            messagebox.showerror("Error de parámetros", str(ve))
            return
        except Exception as e:
            messagebox.showerror("Error de parámetros", f"Ocurrió un error inesperado: {e}")
            return

        self.simulando = True
        self.simular_llegada()
    def simular_llegada(self):
        if not self.simulando:
            return

        nombre = f"Estudiante {self.contador}"
        pedido = random.choice(list(self.pedidos_posibles.keys()))
        self.cola_caja.append((nombre, pedido))
        self.lista_caja.insert(tk.END, f"{nombre} - Pedido: {pedido}")
        self.estado_label.config(text=f"🟢 {nombre} llegó a la caja (Pedido: {pedido})")
        self.contador += 1

        if not self.atendiendo_caja:
            self.root.after(500, self.atender_caja)

        delay = self.rng.next_delay(min_ms=2000, max_ms=15000)
        self.root.after(delay, self.simular_llegada)

    def atender_caja(self):
        if self.cola_caja:
            nombre, pedido = self.cola_caja.pop(0)
            self.lista_caja.delete(0)
            self.estado_label.config(text=f"💰 {nombre} está pagando su pedido ({pedido})")
            self.root.after(1500, lambda: self.pasar_a_barra(nombre, pedido))

    def pasar_a_barra(self, nombre, pedido):
        self.cola_barra.append((nombre, pedido))
        self.lista_barra.insert(tk.END, f"{nombre} - Pedido: {pedido}")
        self.estado_label.config(text=f"➡️ {nombre} fue a la barra a esperar su pedido")
        self.atendiendo_caja = False
        self.root.after(500, self.atender_caja)

        if not self.atendiendo_barra:
            self.root.after(500, self.atender_barra)

    def atender_barra(self):
        if self.cola_barra:
            nombre, pedido = self.cola_barra.pop(0)
            self.lista_barra.delete(0)
            tiempo = self.pedidos_posibles[pedido]
            self.estado_label.config(text=f"👨‍🍳 Preparando {pedido} para {nombre}...")
            self.root.after(tiempo, lambda: self.entregar_pedido(nombre, pedido))

    def entregar_pedido(self, nombre, pedido):
        tiempo_espera = self.root.winfo_pointerx()/100  # Proxy del tiempo de espera
        self.tiempos_espera.append(tiempo_espera)
        self.actualizar_estadisticas()
        self.estado_label.config(text=f"✅ Pedido de {nombre} entregado ({pedido})")
        self.total_atendidos += 1
        self.total_atendidos_label.config(text=f"Total entregados: {self.total_atendidos}")
        self.atendiendo_barra = False
        self.root.after(500, self.atender_barra)
    def actualizar_estadisticas(self):
        if self.tiempos_espera:
            media = sum(self.tiempos_espera) / len(self.tiempos_espera)
            maximo = max(self.tiempos_espera)
            self.estadisticas_label.config(
                text=f"Media: {int(media)} m | Máximo: {maximo} m"
            )


# Ejecutar la interfaz
if __name__ == "__main__":
    root = tk.Tk()
    app = BarSimulator(root)
    root.mainloop()

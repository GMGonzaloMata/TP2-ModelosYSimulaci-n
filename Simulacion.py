import tkinter as tk
from tkinter import ttk
from generadores.VonNeumann import VonNeumannRNG
from generadores.fibonacci import FibonacciRNG
from generadores.congruencial_aditivo import CongruencialAditivoRNG
from generadores.congruencial_multiplicativo import CongruencialMultiplicativoRNG
from generadores.congruencial_mixto import CongruencialMixtoRNG
from Validacion.ChiCuadrado import ChiCuadradoTest


# Interfaz gráfica con pestañas
class ChiCuadradoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación y Chi-Cuadrado")

        notebook = ttk.Notebook(root)
        self.tab_generador = ttk.Frame(notebook)
        self.tab_test = ttk.Frame(notebook)

        notebook.add(self.tab_generador, text='Generador')
        notebook.add(self.tab_test, text='Chi-Cuadrado')
        notebook.pack(expand=True, fill='both')

        self.generador_var = tk.StringVar()
        self.generador_combo = ttk.Combobox(self.tab_generador, textvariable=self.generador_var, values=[
            "Congruencial Mixto", "Congruencial Multiplicativo", "Congruencial Aditivo", "Fibonacci", "Von Neumann"
        ], state="readonly")
        self.generador_combo.pack(pady=5)
        self.generador_combo.current(0)
        self.generador_combo.bind("<<ComboboxSelected>>", self.actualizar_parametros)

        self.param_frame = ttk.Frame(self.tab_generador)
        self.param_frame.pack(pady=5)
        self.param_entries = {}

        ttk.Button(self.tab_generador, text="Generar Números", command=self.generar_numeros).pack(pady=5)
        self.text_generador = tk.Text(self.tab_generador, height=15, width=60)
        self.text_generador.pack(pady=5)

        self.test_combo = ttk.Combobox(self.tab_test, values=[
            "Congruencial Mixto", "Congruencial Multiplicativo", "Congruencial Aditivo", "Fibonacci", "Von Neumann"
        ], state="readonly")
        self.test_combo.pack(pady=5)
        self.test_combo.current(0)
        self.test_combo.bind("<<ComboboxSelected>>", self.actualizar_parametros_test)

        self.param_test_frame = ttk.Frame(self.tab_test)
        self.param_test_frame.pack(pady=5)
        self.param_test_entries = {}

        ttk.Button(self.tab_test, text="Ejecutar Test", command=self.ejecutar_test).pack(pady=5)
        self.text_test = tk.Text(self.tab_test, height=15, width=60)
        self.text_test.pack(pady=5)

        self.actualizar_parametros()
        self.actualizar_parametros_test()

    def actualizar_parametros(self, event=None):
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        self.param_entries.clear()

        tipo = self.generador_combo.get()
        if tipo == "Congruencial Mixto":
            campos = ["Semilla", "a", "c", "m"]
        elif tipo == "Congruencial Multiplicativo":
            campos = ["Semilla", "a", "m"]
        elif tipo == "Congruencial Aditivo":
            campos = ["Semilla 1", "Semilla 2", "m"]
        elif tipo == "Fibonacci":
            campos = ["Semilla 1", "Semilla 2", "Módulo"]
        else:
            campos = ["Semilla", "Dígitos"]

        for campo in campos:
            label = ttk.Label(self.param_frame, text=campo + ":")
            entry = tk.Entry(self.param_frame)
            label.pack()
            entry.pack()
            self.param_entries[campo] = entry

    def actualizar_parametros_test(self, event=None):
        for widget in self.param_test_frame.winfo_children():
            widget.destroy()
        self.param_test_entries.clear()

        tipo = self.test_combo.get()
        if tipo == "Congruencial Mixto":
            campos = ["Semilla", "a", "c", "m"]
        elif tipo == "Congruencial Multiplicativo":
            campos = ["Semilla", "a", "m"]
        elif tipo == "Congruencial Aditivo":
            campos = ["Semilla 1", "Semilla 2", "m"]
        elif tipo == "Fibonacci":
            campos = ["Semilla 1", "Semilla 2", "Módulo"]
        else:
            campos = ["Semilla", "Dígitos"]

        for campo in campos:
            label = ttk.Label(self.param_test_frame, text=campo + ":")
            entry = tk.Entry(self.param_test_frame)
            label.pack()
            entry.pack()
            self.param_test_entries[campo] = entry

    def obtener_generador(self, tipo, entries):
        if tipo == "Congruencial Mixto":
            valores = [int(entries[campo].get()) for campo in ["Semilla", "a", "c", "m"]]
            return CongruencialMixtoRNG(*valores)
        elif tipo == "Congruencial Multiplicativo":
            valores = [int(entries[campo].get()) for campo in ["Semilla", "a", "m"]]
            return CongruencialMultiplicativoRNG(*valores)
        elif tipo == "Congruencial Aditivo":
            valores = [int(entries[campo].get()) for campo in ["Semilla 1", "Semilla 2", "m"]]
            return CongruencialAditivoRNG(*valores)
        elif tipo == "Fibonacci":
            valores = [int(entries[campo].get()) for campo in ["Semilla 1", "Semilla 2", "Módulo"]]
            return FibonacciRNG(*valores)
        else:
            valores = [int(entries[campo].get()) for campo in ["Semilla", "Dígitos"]]
            return VonNeumannRNG(*valores)

    def generar_numeros(self):
        tipo = self.generador_combo.get()
        gen = self.obtener_generador(tipo, self.param_entries)
        numeros = [f"{gen.next_float():.4f}" for _ in range(20)]
        self.text_generador.delete(1.0, tk.END)
        self.text_generador.insert(tk.END, "Números generados:\n")
        self.text_generador.insert(tk.END, "\n".join(numeros))

    def ejecutar_test(self):
        tipo = self.test_combo.get()
        gen = self.obtener_generador(tipo, self.param_test_entries)
        test = ChiCuadradoTest(gen, cantidad=200, clases=10)
        frec, chi2, critico, conclusion = test.resultado()

        self.text_test.delete(1.0, tk.END)
        self.text_test.insert(tk.END, f"Frecuencias observadas: {frec}\n")
        self.text_test.insert(tk.END, f"Chi-Cuadrado calculado: {chi2:.4f}\n")
        if critico:
            self.text_test.insert(tk.END, f"Valor crítico (α=0.05): {critico:.4f}\n")
        else:
            self.text_test.insert(tk.END, "Valor crítico no disponible para estos grados de libertad.\n")
        self.text_test.insert(tk.END, f"Resultado: {conclusion}\n")

# Ejecutar
if __name__ == '__main__':
    root = tk.Tk()
    app = ChiCuadradoApp(root)
    root.mainloop()

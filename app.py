"""
@Author:
"""

import os
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from controller import Controller
import matplotlib.pyplot as plt

class MainGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.relativePath = os.getcwd()
        self.controller = Controller()
        self.mensaje = None
        self.crearWidgets()

    def crearWidgets(self):
        labelTitulo = tk.Label(
            text="Demanda Colombia", fg="blue", font=("arial bold", 20))
        labelTitulo.pack()

        self.frameBotones = tk.Frame(self, bg='cornsilk3')
        self.frameBotones.pack()

        self.frameGrafica = tk.Frame(self, bg='cyan2')
        self.frameGrafica.pack()

        botonCargarCarpeta = tk.Button(
            self.frameBotones, text="Cargar carpeta", command=self.cargarCarpeta, fg="blue", bg="white", width=15)
        botonCargarCarpeta.grid(row=0, column=1, padx=10, pady=5)

        botonCargarArchivo = tk.Button(
            self.frameBotones, text="Cargar archivo", command=self.cargarArchivo, fg="blue", bg="white", width=15)
        botonCargarArchivo.grid(row=0, column=2, padx=10, pady=5)

        botonGuardarDatos = tk.Button(
            self.frameBotones, text="Guardar datos", command=self.guardarDatos, fg="blue", bg="white", width=15)
        botonGuardarDatos.grid(row=0, column=3, padx=10, pady=5)

    def graficar(self, figura): 
        for widget in self.frameGrafica.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(figura, master=self.frameGrafica)
        canvas.draw()
        canvas.get_tk_widget().pack(anchor="center")
      
    def cargarCarpeta(self):
        # opciones de busqueda
        opcionesDirectorio = {
            'initialdir': self.relativePath,
            'mustexist': False,
            'title': "Select Directory"
        }
        try:
            pathArchivos = filedialog.askdirectory(**opcionesDirectorio)
            figura = self.controller.graficarMaximaDemanda(pathArchivos)
            self.graficar(figura)
        except:
            print('se debe seleccionar un directorio')

    def cargarArchivo(self):
        """
        permite selecionar un archivo con las opciones de busqueda
        """
        opcionesArchivo = {
            'defaultextension': "*.csv",
            'filetypes': [("files csv", "*.csv"), ('all files', '*.*')],
            'initialdir': self.relativePath,
            'title': "Select File",
        }
        try:
            pathArchivo = filedialog.askopenfilename(**opcionesArchivo)
            self.controller.cargarArchivo(pathArchivo)
            minDia, maxDia = self.seleccionarItervalo()
            figura, self.nombreArchivo = self.controller.setIntervalo(minDia, maxDia)
            self.graficar(figura)
        except:
            print('se debe seleccionar un archivo')
        
    def guardarDatos(self):
        opcionesArchivo = {
            'defaultextension': "*.csv",
            'filetypes': [("files csv", "*.csv"), ('all files', '*.*')],
            'initialdir': self.relativePath,
            'title': "Select File",
            'initialfile': self.nombreArchivo
        }
        try:
            pathArchivo = filedialog.asksaveasfilename(
                **opcionesArchivo)
            print(pathArchivo)
            self.controller.guardarNuevosDatos(pathArchivo)
        except:
            print('se debe seleccionar una ruta')

    def seleccionarItervalo(self):
        minDia = 5
        maxDia = 10
        return minDia, maxDia
        

if __name__ == "__main__":
    root = MainGUI()
    root.title("Demanda Colombia")  # Título de la ventana
    root.geometry("1100x600")  # tamaño de la ventana
    root.mainloop()


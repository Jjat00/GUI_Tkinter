"""
@author: Jhon_Tutalcha
"""

import os
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from controller import Controller
import matplotlib.pyplot as plt

class MainGUI():
    """ 
    Interfaz gráfica principal
    """
    def __init__(self):
        super().__init__()
        window = tk.Tk()
        window.title("Demanda Colombia")  
        window.geometry("1100x600")  

        self.relativePath = os.getcwd()
        self.controller = Controller()
        self.mensaje = None
        self.crearWidgets(window)
        window.mainloop()

    def crearWidgets(self, window):
        """ 
        Pone todos los elementos gráficos en la interfaz
        """
        labelTitulo = tk.Label(window, 
            text="Demanda Colombia", fg="blue", font=("arial bold", 20))
        labelTitulo.pack()

        self.frameBotones = tk.Frame(window, bg='cornsilk3')
        self.frameBotones.pack()

        # configuración intervalo de días
        self.frameConfig = tk.Frame(window, bg='cyan2')
        self.frameConfig.pack()
        #self.seleccionarItervalo()

        labelminIntervalo = tk.Label(self.frameConfig, 
            text="min intervalo:", fg="black", font=("arial bold", 10))
        labelminIntervalo.pack()
        
        self.minIntervalo = tk.Entry(self.frameConfig)
        self.minIntervalo.insert(0, 1)
        self.minIntervalo.pack()

        labelmaxIntervalo = tk.Label(self.frameConfig, 
            text="max intervalo:", fg="black", font=("arial bold", 10))
        labelmaxIntervalo.pack()

        self.maxIntervalo = tk.Entry(self.frameConfig)
        self.maxIntervalo.insert(0, 30)
        self.maxIntervalo.pack()

        self.frameGrafica = tk.Frame(window, bg='cyan2')
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
        """
        Pone en la interfaz gráfica una figura de matplotlib

        parameters: figura de matplotlib 
        """

        for widget in self.frameGrafica.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(figura, master=self.frameGrafica)
        canvas.draw()
        canvas.get_tk_widget().pack(anchor="center")
      
    def cargarCarpeta(self):
        """
        Abre un cuadro de dialogo para selccionar el directorio en donde 
        se encuentran los archivos .csv
        """
        
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
        Abre un cuado de dialogo para selecionar un archivo con las opciones de busqueda
        """

        opcionesArchivo = {
            'defaultextension': "*.csv",
            'filetypes': [("files csv", "*.csv"), ('all files', '*.*')],
            'initialdir': self.relativePath,
            'title': "Select File",
        }
        try:
            pathArchivo = filedialog.askopenfilename(**opcionesArchivo)
            maxDiasMes = self.controller.cargarArchivo(pathArchivo)
            minDia, maxDia = self.seleccionarItervalo()
            if minDia < 0 or maxDia >= maxDiasMes:
                tk.messagebox.showinfo(message="El intervalo debe ser mayor que 1 y menor que " + str(maxDiasMes)
                , title="Advertencia")
            else:
                figura, self.nombreArchivo = self.controller.setIntervalo(minDia, maxDia)
                self.graficar(figura)
        except:
            print('se debe seleccionar un archivo')
        
    def guardarDatos(self):
        """
        Abre un dialogo para seleccionar la ruta en donde se guardarán los archivos
        """

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
        """
        Configura el intervalo de visualización de los datos al cargar un archivo .csv
        """
        minDia = int(self.minIntervalo.get())-1
        maxDia = int(self.maxIntervalo.get())-1
        return minDia, maxDia
        

if __name__ == "__main__":
    MainGUI()
    

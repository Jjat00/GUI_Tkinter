import datetime as dt
import os
import matplotlib.pyplot as plt

class Controller():
    def __init__(self):
        super().__init__()
        #self.pathDirectorio = os.getcwd() + '/demanda_col'
        #self.pathDirectorio = pathArchivos#os.getcwd() + '/demanda_col'

    def cargarNombreArchivos(self, pathArchivos):
        listaArchivos = os.listdir(pathArchivos)
        listaArchivos.sort()  # ordenar la lista de los archivos
        nombreArchivos = []
        for nombreArchivo in listaArchivos:
            if nombreArchivo.lower().endswith(".csv"):
                nombreArchivos.append(nombreArchivo)
        return (pathArchivos, nombreArchivos)

    def procesarDatos(self, file):
        fechas = []
        valoresDemanda = []
        for datos in file:
            # separar por punto y coma
            datosLinea = datos.split(";")
            fecha = datosLinea[2]
            demandaDia = datosLinea[4:-1]
            fechaDia = []
            # transformar datos a float y construir fecha
            for index in range(len(demandaDia)):
                demandaDia[index] = float(demandaDia[index].replace(",","."))
                fechaDia.append(dt.datetime.strptime(
                    fecha + " " + str(index), "%Y-%m-%d %H"))
            # agregar los datos de cada día a la lista del mes
            valoresDemanda.extend(demandaDia)
            fechas.extend(fechaDia)
        return fechas, valoresDemanda

    def cargarDatosDirectorio(self, pathDirectorio, nombreArchivos):
        listaDatos = []
        datosCompletos = {}
        for nombre in nombreArchivos:
            file = open(pathDirectorio + '/' + nombre)
            # leer primera linea de encabezado
            file.readline()
            fechaMes, demandaMes = self.procesarDatos(file)
            # guardar los datos de cada mes en un diccionario
            datosCompletos = {
                'nombreArchivo': nombre,
                'fecha': fechaMes,
                'valorDemanda': demandaMes,
            } 
            listaDatos.append(datosCompletos)
        return listaDatos

    def cargarDatosArchivo(self, pathArchivo):
        datosCompletos = {}
        file = open(pathArchivo)
        # leer primera linea de encabezado
        file.readline()
        fechaMes, demandaMes = self.procesarDatos(file)
        # guardar los datos del mes en un diccionario
        datosCompletos = {
            'nombreArchivo': pathArchivo.split('/')[-1],
            'fecha': fechaMes,
            'valorDemanda': demandaMes,
        }
        return datosCompletos

    def encontrarDemandaMaxima(self, datos):
        maximosValores = []
        fechaMaxValor = None
        maxValor = None
        for datosMes in datos:
            valorDemanda = datosMes['valorDemanda']
            maximosValores.append(max(valorDemanda))
        
        mesMaxValor = maximosValores.index(max(maximosValores))
        indexMaxValor = datos[mesMaxValor]['valorDemanda'].index(
            maximosValores[mesMaxValor])

        nombreArchivo = datos[mesMaxValor]['nombreArchivo']
        fechaMaxValor = datos[mesMaxValor]['fecha'][indexMaxValor]
        maxValor = datos[mesMaxValor]['valorDemanda'][indexMaxValor]

        return (nombreArchivo, fechaMaxValor, maxValor)

    def graficarMaximaDemanda(self, pathArchivos):
        pathDirectorio, nombreArchivos = self.cargarNombreArchivos(pathArchivos)
        datos = self.cargarDatosDirectorio(pathDirectorio, nombreArchivos)
        nombreArchivo, fechaMaxValor, maxValor = self.encontrarDemandaMaxima(datos)
        datosDemanda = self.cargarDatosArchivo(pathDirectorio + '/' + nombreArchivo)
        mensaje = 'La demanda máxima se dió el %s y fue %fW'% (fechaMaxValor, maxValor)
        # crear figura
        fig = plt.Figure(figsize=(11, 5), dpi=100)
        # máximo valor
        fig.add_subplot().plot(
            fechaMaxValor, maxValor, 'o', c='r')
        # gráfica del mes que tiene el máximo valor
        fig.add_subplot().plot(
            datosDemanda['fecha'], datosDemanda['valorDemanda'])
        fig.add_subplot().set_title(nombreArchivo + '\n' + mensaje)

        return fig

    def cargarArchivo(self, pathArchivo):
        self.datosArchivo = self.cargarDatosArchivo(pathArchivo)
        valoresDemanda = self.datosArchivo['valorDemanda']
        diasMes = int(len(valoresDemanda) / 24)

    def setIntervalo(self, min, max):
        self.nuevasFechas = self.datosArchivo['fecha'][min * 24 : max * 24]
        self.nuevosDatos = self.datosArchivo['valorDemanda'][min * 24 : max * 24]
        nombreArchivo = 'mes_%i_dia_%i_al%i.txt' % (
            self.nuevasFechas[0].month, min, max)
        # crear figura
        fig = plt.Figure(figsize=(10, 5), dpi=100)
        fig.add_subplot().plot(
            self.nuevasFechas, self.nuevosDatos)
        fig.add_subplot().set_title(self.datosArchivo['nombreArchivo'])
        return fig, nombreArchivo

    def guardarNuevosDatos(self, pathArchuivo):
        file = open(pathArchuivo, "w")
        lines = []
        for index in range(len(self.nuevosDatos)):
            line =  str(self.nuevasFechas[index]) + ';' + str(self.nuevosDatos[index]) + '\n'
            lines.append(line)
        file.writelines(lines)
        file.close()



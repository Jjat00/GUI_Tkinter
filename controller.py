import datetime as dt
import os
import matplotlib.pyplot as plt

class Controller():
    """
    Lógica para la interfaz de usuario
    """
    def __init__(self):
        super().__init__()

    def cargarNombreArchivos(self, pathArchivos):
        """
        Dado la ruta del directorio retorna los nombres de todos los archivos .csv

        paremeters: 
            pathArchivos: String
            string de la ruta del directorio

        return:  
            pathArchivos: string
            ruta del directorio

            nombreArchivos: lista de string
            lista con los nombres de los archivos ubicados en el directorio
        """

        listaArchivos = os.listdir(pathArchivos)
        listaArchivos.sort()  # ordenar la lista de los archivos
        nombreArchivos = []
        for nombreArchivo in listaArchivos:
            if nombreArchivo.lower().endswith(".csv"):
                nombreArchivos.append(nombreArchivo)
        return (pathArchivos, nombreArchivos)

    def procesarDatos(self, file):
        """
        dado un archivo .csv extrae la fecha y los valores de la demanda del mes

        parameters: 
            file: File
            archivo .csv abierto

        return:
            fechas: lista 
            lista de todas las fechas

            valoresDemanda: lista de float
            lista de todos los valores de la demanda
        """

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
        """
        Dado la ruta del directorio y los nombres de los archivos retorna 
        una lista con los datos de cada mes

        parameters: 
            pathDirectorio: String
            string de la ruta del directorio donde se cuentran los archivos

            nombreArchivos: lista de string
            lista con los nombres de los archivos

        return:
            listaDatos: lista de diccionarios
            lista de diccionarios con los datos de cada mes 

        """

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
        """
        Carga los datos a partir de la ruta de un archivo .csv seleccionado

        parameters: 
            pathArchivo: String
            string de la ruta del archivo

        return:
            datosCompletos: diccionario
            diccionario con los datos del mes selecciondo
        """

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
        """
        Encuentra el mes en donde hubo la máxima demanda entre todos los archivos

        parameters: 
            datos: lista de diccionarios
            lista de diccionarios con la información de todos los meses

        return:
            nombreArchivo: string
            string con el nombre del archivo en donde se encuentra la máxima demanda

            fechaMaxValor: date
            fecha en donde se encuentra la máxima demanda            

            maxValor: float
            float del máximo valor encontrado

        """

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
        """
        gráfica el mes con la máxima demanda encontrada

        parameters: 
            pathArchivos: String
            string con la ruta en donde se encuentran los archivos

        return:
            fig: figura matplotlib
            figura matplotlib del mes de la máxima demanda
        """

        pathDirectorio, nombreArchivos = self.cargarNombreArchivos(pathArchivos)
        datos = self.cargarDatosDirectorio(pathDirectorio, nombreArchivos)
        nombreArchivo, fechaMaxValor, maxValor = self.encontrarDemandaMaxima(datos)
        datosDemanda = self.cargarDatosArchivo(pathDirectorio + '/' + nombreArchivo)
        mensaje = 'La demanda máxima se dió el %s y fue %fW'% (fechaMaxValor, maxValor)
        # crear figura
        fig = plt.Figure(figsize=(11, 5), dpi=100)
        # máximo valor
        ax = fig.add_subplot()
        ax.plot(fechaMaxValor, maxValor, 'o', c='r')
        # gráfica del mes que tiene el máximo valor
        ax.plot(datosDemanda['fecha'], datosDemanda['valorDemanda'])
        ax.set_title(nombreArchivo + '\n' + mensaje)
        #plt.show()
        return fig

    def cargarArchivo(self, pathArchivo):
        """
        carga los datos a partir de un archivo .csv

        parameters: 
            pathArchivo: string
            string de la ruta en donde se encuentra el archivo
        """
        self.datosArchivo = self.cargarDatosArchivo(pathArchivo)
        valoresDemanda = self.datosArchivo['valorDemanda']
        maxDiasMes = int(len(valoresDemanda) / 24)
        return maxDiasMes

    def setIntervalo(self, min, max):
        """
        retorna la figura dado un intervalo de dias

        parameters: 
            min: int
            entero donde empieza el intervalo de dias

            max: int
            entero donde finaliza el intervalo de dias

        return:
            fig: figura matplotlib
            figura con el intervalo de dias dado

            nombreArchivo: string
            string del nombre del archivo que se seleccionó
        """

        self.nuevasFechas = self.datosArchivo['fecha'][min * 24 : max * 24]
        self.nuevosDatos = self.datosArchivo['valorDemanda'][min * 24 : max * 24]
        nombreArchivo = 'mes_%i_dia_%i_al_%i.txt' % (
            self.nuevasFechas[0].month, min, max)
        # crear figura
        fig = plt.Figure(figsize=(10, 5), dpi=100)
        fig.add_subplot().plot(
            self.nuevasFechas, self.nuevosDatos)
        fig.add_subplot().set_title(self.datosArchivo['nombreArchivo'])
        return fig, nombreArchivo

    def guardarNuevosDatos(self, pathArchivo):
        """
        Guarda los datos del intervalo que se seleccinó

        parameters: 
            pathArchivo: String 
            string de la ruta del archivo
        """
        
        file = open(pathArchivo, "w")
        lines = []
        for index in range(len(self.nuevosDatos)):
            line =  str(self.nuevasFechas[index]) + ';' + str(self.nuevosDatos[index]) + '\n'
            lines.append(line)
        file.writelines(lines)
        file.close()



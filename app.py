# GraphicImport
import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
import pandas as pd
from pip._internal.utils.misc import tabulate
from scipy import stats
from tabulate import tabulate
from time import process_time
import matplotlib.pyplot as plt
from PyQt5.QtGui import QPixmap
import numpy as np
import random

class ejemplo_GUI(QMainWindow):

    # Creación de variables globales para uso dentro de cualquier función de Python
    # Variables creation  for use into everyone function of Python
    global contadorColumnas
    contadorColumnas = 0
    global preprocessed_data
    global cols
    global tic
    global toc
    global difTime    
    global _start_time 
    global n 
    n = 50 
    global maxColumnas
    maxColumnas = 0
    cols = []

    # Función que se ejecuta cuando se inicia el aplicativo
    # Function execute when the app start
    def __init__(self):
        super().__init__()
        uic.loadUi("GUI.ui", self)
        # Definición de elementcdos gráficos asociados a funciones - Cuando se dé clic se ejecuta una función
        # Definition of Graph elements asociate to functions - When the user give clic the app excecute a relate function
        self.cargarArchivo.clicked.connect(self.fn_cargarArchivo)
        self.cerrarAplicativo.clicked.connect(self.fn_closeEvent)
        #self.procesarArchivo.clicked.connect(self.fn_procesarArchivo)
        self.Adicionar.clicked.connect(self.fn_adicionarColumnas)
        self.borrarColumnas.clicked.connect(self.fn_borrarColumnas)
        # Metodos para evaluar cual item esta check
        self.ckboxOneSample.stateChanged.connect(self.Check_OneSample)
        self.checkBox_2.stateChanged.connect(self.Check_Paired)
        self.CkboxCorrelaciones.stateChanged.connect(self.Check_Correlations)
        
        #self.procesarArchivo.clicked.connect(self.Ttest_1samp)
        # Definición de campos deshabilitados u ocultos cuando se inicia la aplicación
        # Definition of disabled or hidden fields  when the app start
        self.ListadoCampos.setEnabled(False)
        self.Adicionar.setEnabled(False)
        self.borrarColumnas.setEnabled(False)
        self.mensajeErrorColumnas.setHidden(True)
        self.ImagenColores.setHidden(True)
        self.label_3.setEnabled(False)
        self.SbCantidaRegis.setEnabled(False)
        self.procesarArchivo.setEnabled(False)

    def Check_OneSample(self):
        if self.ckboxOneSample.isChecked():
            self.label_3.setEnabled(True)
            self.SbCantidaRegis.setEnabled(True)
            self.checkBox_2.setChecked(False)
            self.CkboxCorrelaciones.setChecked(False)
            self.procesarArchivo.clicked.connect(self.Ttest_1samp)
            self.procesarArchivo.setEnabled(True)
            self.ImagenColores.setHidden(False)
            global maxColumnas
            maxColumnas = 1

    def Check_Paired(self):
        if self.checkBox_2.isChecked():
            self.label_3.setEnabled(False)
            self.SbCantidaRegis.setEnabled(False)
            self.CkboxCorrelaciones.setChecked(False)
            self.ckboxOneSample.setChecked(False)
            self.procesarArchivo.setEnabled(True)
            self.procesarArchivo.clicked.connect(self.fn_generarPairedTTest)
            self.ImagenColores.setHidden(True)
            global maxColumnas
            maxColumnas = 2

    def Check_Correlations(self):
        if self.CkboxCorrelaciones.isChecked():
            self.label_3.setEnabled(False)
            self.SbCantidaRegis.setEnabled(False)
            self.ckboxOneSample.setChecked(False)
            self.checkBox_2.setChecked(False)
            self.procesarArchivo.clicked.connect(self.fn_procesarArchivo)
            self.procesarArchivo.setEnabled(True)   
            self.ImagenColores.setHidden(False)     
            global maxColumnas
            maxColumnas = 4
        
### Metodo de ONE SAMPLE

    def Ttest_1samp(self):
        _start_time = process_time()
        # seasons_mapping = {1: 'winter', 2: 'spring', 3: 'summer', 4: 'fall'}
        # preprocessed_data['season'] = preprocessed_data['season'].apply(lambda x: seasons_mapping[x])

        # # transform yr
        # yr_mapping = {0: 2011, 1: 2012}
        # preprocessed_data['yr'] = preprocessed_data['yr'].apply(lambda x: yr_mapping[x])

        # # transform weekday
        # weekday_mapping = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
        # preprocessed_data['weekday'] = preprocessed_data['weekday'].apply(lambda x: weekday_mapping[x])

        # # transform weathersit
        # weather_mapping = {1: 'clear', 2: 'cloudy', 3: 'light_rain_snow', 4: 'heavy_rain_snow'}
        # preprocessed_data['weathersit'] = preprocessed_data['weathersit'].apply(lambda x: weather_mapping[x]) 

        # # transorm hum and windspeed
        # preprocessed_data['hum'] = preprocessed_data['hum']*100
        # preprocessed_data['hum'] = preprocessed_data['hum'].astype(str).str[0:3]

        # preprocessed_data['windspeed'] = preprocessed_data['windspeed']*67
        # preprocessed_data['windspeed'] = preprocessed_data['windspeed'].astype(str).str[0:3]

        cabecera = cols
        columna = cols[0]        
        print('Esto' + str(preprocessed_data['mnth'].mnth))
        resultado = random.sample(preprocessed_data[columna], self.SbCantidaRegis.value());
        population_mean = resultado.mean()
        print('Media' + str(population_mean))
        test_res = stats.ttest_1samp(resultado, population_mean)
        print("TEst " + str(population_mean))
        t1_stop = process_time()
        tiempo = t1_stop-_start_time

        self.resultadoCorrelacion.setText(tabulate(resultado,cabecera) + " \n " 
        + "_--------------------------------------------------------------" 
        + "\n Tiempo de procesamiento de la muestra: " + str(tiempo) + " segundos"
        + "\n Resultado del analisis de la muestra" + " \n "
        +f"Statistic value: {test_res[0]:.03f}, \ p-value: {test_res[1]:.03f}" )

# Función para borrar los campos o columnas seleccionadas que se incluirán en el analisis de correlación
# Function for erase the selected fields o selected columns that will be includ in the correlation analysis
    def fn_borrarColumnas(self):
        # Se habilitan los controles bloqueado al seleccionar los campos o las columnas del archivo CSV cargado
        # The blocked controls will be enabled, those controls or fields was blocked when the user selected from the file CSV uploaded
        self.textColumnas.setText('')
        self.mensajeErrorColumnas.setHidden(True)
        self.ListadoCampos.setEnabled(True)
        self.Adicionar.setEnabled(True)
        # Se reinician los valores de las variables globales
        # The value of global variables are restart
        global cols
        cols = []
        global contadorColumnas
        contadorColumnas = 0


# Función para adicionar campos o columnas del archivo .CSV cargado para el analisis de correlación
# Function for add fields or columns from the file CVS uploaded for the analysis of correlation
    def fn_adicionarColumnas(self):
        # Varible global que controla 4 campos o columnas para el analisis de correlación
        # Global variable that manage four fields or columns fro the correlations analysis      
        global contadorColumnas
        contadorColumnas += 1
        # Validación de selección de máximo 4 columnas o campos
        # Validation of selection from maximum four columns or fields
        if contadorColumnas <= maxColumnas:
            self.textColumnas.setText(self.textColumnas.toPlainText() + self.ListadoCampos.currentText() + '\n')
            global cols
            cols.append(str(self.ListadoCampos.currentText()))
        # Si ya fueron seleccionados los 4 campos para el analisis de correlación
        # If the four fields or columns already been selected for the correlations analysis
            if contadorColumnas == maxColumnas:
                self.mensajeErrorColumnas.setHidden(False)
                self.ListadoCampos.setEnabled(False)
                self.Adicionar.setEnabled(False)

# Función para seleccionar y cargar el archivo .CVS - Adicionalmente cuando se carga el arhcivo se alimenta el listado de campos
# Function for select and upload tha .CSV file - Further when the file is uploaded, the list from fields or columns is filled
    def fn_cargarArchivo(self):
        # Se cargan los datos del archivo CSV
        # The data from the CSV file is upload
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'C:','Excel (*.csv)')
        self.textArchivo.setText(fname[0])
        dataInFile = pd.read_csv(fname[0])
        global  preprocessed_data
        preprocessed_data = dataInFile.copy()
        # Se habilitan los controles del formulario del aplicativo
        # The controls from the form of app will be enable
        self.ListadoCampos.addItems(preprocessed_data.columns.tolist())
        self.ListadoCampos.setEnabled(True)
        self.Adicionar.setEnabled(True)
        self.borrarColumnas.setEnabled(True)

# Función para realizar el analisis de correlacion con el archivo cargado y las variables seleccionadas
# Function for make the correlation analysis with the uploaded file and the variables selected
    def fn_procesarArchivo(self):
        _start_time = process_time()
        def compute_correlations(data, col):
            pearson_reg = stats.pearsonr(data[col], data["registered"])[0]
            pearson_cas = stats.pearsonr(data[col], data["casual"])[0]
            spearman_reg = stats.spearmanr(data[col], data["registered"])[0]
            spearman_cas = stats.spearmanr(data[col], data["casual"])[0]

            # Se realiza el cálculo de la correlación de la serie seleccionada
            # The correlation calculation from the selected series is performed
            return pd.Series({"Pearson (registered)": pearson_reg,
                              "Spearman (registered)": spearman_reg,
                              "Pearson (casual)": pearson_cas,
                              "Spearman (casual)": spearman_cas})

        # Se calculan las  medidas de correlación entre diferentes características
        # The correlation measures is compute between different features
        corr_data = pd.DataFrame(
            index=["Pearson (registered)", "Spearman (registered)", "Pearson (casual)", "Spearman (casual)"])
        global cols
        for col in cols:
            print(f'Data: {col}');
            corr_data[col] = compute_correlations(preprocessed_data, col)

        t1_stop = process_time()
        tiempo = t1_stop-_start_time

        self.resultadoCorrelacion.setText(tabulate(corr_data.T,headers='keys', tablefmt='psql') + " \n " 
        + "_--------------------------------------------------------------" 
        + "\n Tiempo de procesamiento de la muestra: " + str(tiempo) + " segundos")

        self.ImagenColores.setHidden(False)
               
        # Matriz de colores
        plot_data = preprocessed_data[cols]
        corr = plot_data.corr()
        fig = plt.figure(figsize=(10,5))
        plt.matshow(corr, fignum=fig.number)
        plt.xticks(range(len(plot_data.columns)), plot_data.columns)
        plt.yticks(range(len(plot_data.columns)), plot_data.columns)
        plt.colorbar()
        plt.ylim([5.5, -0.5])

        fig.savefig('C:/DataAnalysis/Analisis/GraficoCorrelacion.png', format='png')
        pixmap = QPixmap('C:/DataAnalysis/Analisis/GraficoCorrelacion.png')
        self.ImagenColores.setPixmap(pixmap)
        self.ImagenColores.setScaledContents(True)
        self.resize(pixmap.width(), pixmap.height())

    def fn_generarPairedTTest(self, event):
        _start_time = process_time()
        resultado = stats.ttest_ind(preprocessed_data[cols[0]], preprocessed_data[cols[1]], equal_var=True)
        t1_stop = process_time()
        tiempo = t1_stop-_start_time
        self.resultadoCorrelacion.setText('Resultado Paired T-Test: \n statistic: ' + str(resultado[0]) + ' \n pvalue: '+ str(resultado[1])
        + "_--------------------------------------------------------------" 
        + "\n Tiempo de procesamiento de la muestra: " + str(tiempo) + " segundos" )

# Función para cerrar el aplicativo
# Function for close the app
    def fn_closeEvent(self, event):
        reply = QMessageBox.question(self, "Cerrar aplicativo", "¿Desea cerrar el aplicativo?", QMessageBox.Yes,
                                            QMessageBox.No, )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

# Función adicional para cerrar el aplicativo
# Function additional for close the app
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

# Bloque de código para el inicio de la aplicación
# Block of code for the start the app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = ejemplo_GUI()
    GUI.show()
    sys.exit(app.exec_())
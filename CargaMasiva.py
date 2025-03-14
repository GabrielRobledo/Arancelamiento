import MySQLdb
import pandas as pd
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename


# Crear la conexión con MySQL
db = MySQLdb.connect(host='localhost', user='root', db='arancelamiento')
cursor = db.cursor()
print('CONEXION EXITOSA')

# Leo la base de datos en Excel y guardo en un DataFrame

# Crear una ventana oculta para que no se muestre la interfaz de tkinter
Tk().withdraw()

# Abrir el explorador de archivos
file_path = askopenfilename(title="Selecciona un archivo Excel", filetypes=[("Archivos Excel", "*.xlsx;*.xlsm")])

# Verificar que el usuario seleccionó un archivo
if file_path:
    # Leer el archivo Excel en un DataFrame
    df = pd.read_excel(file_path, sheet_name='HyS')

else:
    print("No se seleccionó ningún archivo.")

# Crear tablas si no existen
cursor.execute("""
CREATE TABLE IF NOT EXISTS Agente (
    idAgente int AUTO_INCREMENT primary key,
    dni int not null,            
    apeYnom varchar(100) not null,
    puestolaboral int not null,
    establecimiento varchar(100) not null,           
    concepto varchar(50) null);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Efector (
    idEfector int AUTO_INCREMENT primary key,
    codPrestador varchar(10) not null,
    RazonSocial varchar(100) not null,
    localidad varchar(50) not null);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS obrasocial(
    idObra int AUTO_INCREMENT primary key,
    descripcion varchar(50) not null);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS arancelamiento(
    idArancel int AUTO_INCREMENT primary key,
    idAgente int not null,
    idObra int not null,
    mes varchar(20) not null,
    anio int not null,
    importe double(20, 2),
    idEfector int not null,
    periodo varchar(20),
    control varchar(20),
    FOREIGN KEY(idAgente) REFERENCES agente(idAgente),
    FOREIGN KEY(idObra) REFERENCES obrasocial(idObra),
    FOREIGN KEY(idEfector) REFERENCES efector(idEfector));
""")

# Inserción de agentes
for index, row in df.iloc[0:].iterrows():
    dni = df.iloc[index, 0]
    puesto = df.iloc[index, 3]
    if puesto == 'ERROR':
        puesto = 0

    cursor.execute(f"""SELECT idAgente FROM Agente WHERE dni = {dni}""")
    result = cursor.fetchone()
    if result is None:
        cursor.execute("""
        INSERT INTO Agente (dni, apeYnom, puestolaboral, establecimiento, concepto) 
        VALUES (%s, %s, %s, %s, %s)""", (dni, df.iloc[index, 2], puesto, df.iloc[index, 4], df.iloc[index, 5]))
db.commit()

# Inserción de efectores
for index, row in df.iloc[0:].iterrows():
    cursor.execute(f"""SELECT idEfector FROM Efector WHERE codPrestador = '{df.iloc[index, 10]}'""")
    result = cursor.fetchone()
    if result is None:
        cursor.execute("""
        INSERT INTO Efector (codPrestador, RazonSocial, localidad) 
        VALUES (%s, %s, %s)""", (df.iloc[index, 10], df.iloc[index, 11], df.iloc[index, 12]))
db.commit()

#insercion de obras sociales
dfunicos = df['OBRA SOCIAL'].unique()
for valor in dfunicos:
    cursor.execute(f"""SELECT idObra FROM obrasocial WHERE descripcion ='{valor}'""")  
    result = cursor.fetchone()
    if result is None:  
        sql=f"""
        INSERT INTO obrasocial (descripcion) 
        VALUES ('{valor}')"""
        cursor.execute(sql)
db.commit()

#insercion de arancelamientos
for index, row in df.iloc[0:].iterrows():
    cursor.execute(f"""SELECT idAgente FROM agente WHERE dni={df.iloc[index, 0]}""")
    idAgente = cursor.fetchone()
    cursor.execute(f"""SELECT idObra FROM obrasocial WHERE descripcion='{df.iloc[index, 6]}'""")
    idobra = cursor.fetchone()
    cursor.execute(f"""SELECT idEfector FROM efector WHERE codPrestador='{df.iloc[index, 10]}'""")
    idhosp = cursor.fetchone()
    importe = df.iloc[index, 9]
    estado = df.iloc[index, 15]
    if isinstance(estado, int):
        estado = "si cobró"   

    if (importe == '-' or importe == ""):
        importe = 0
        cursor.execute("""
        INSERT INTO arancelamiento (idAgente, idObra, mes, anio, importe, idEfector, periodo, control) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (idAgente, idobra, df.iloc[index, 7], df.iloc[index, 8], importe, idhosp, df.iloc[index, 14], estado))
    else:
        cursor.execute("""
        INSERT INTO arancelamiento (idAgente, idObra, mes, anio, importe, idEfector, periodo, control) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (idAgente, idobra, df.iloc[index, 7], df.iloc[index, 8], importe, idhosp, df.iloc[index, 14], estado))    

db.commit()        
    

print('REGISTROS CARGADOS CON EXITO!!!')
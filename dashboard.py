import MySQLdb
import pandas as pd
import numpy as np
import streamlit as st

# Crear la conexión con MySQL
try:
    db = MySQLdb.connect(host='localhost', user='root', db='arancelamiento')
    cursor = db.cursor()
    print('CONEXION EXITOSA')

except MySQLdb.Error as e:
    # Capturar y mostrar detalles completos del error
    print("Error de conexión:", e)
    print("Detalles del error:", e.args)

# Establecer configuración de la página y Titulo del Reporte
st.set_page_config(page_title="Dashboard UEP-UGP-MSP", layout="wide", initial_sidebar_state="expanded")

with st.sidebar:
    st.text(body='Ingrese los filtros a aplicar: ')
    fechaDesde = st.date_input(label='Desde:', format='DD/MM/YYYY')
    DesdeFormat =fechaDesde.strftime("%d-%m-%Y")
    fechaHasta = st.date_input(label='Hasta:', format='DD/MM/YYYY')
    HastaFormat = fechaHasta.strftime("%d-%m-%Y")
    check =st.button(label='CONSULTAR')


sql1 = f"""SELECT idArancel, a.dni, a.apeYnom, a.puestolaboral, a.establecimiento, a.concepto, o.descripcion, ar.mes, ar.anio, ar.importe, e.RazonSocial, e.localidad, ar.periodo, ar.control FROM `arancelamiento` as ar inner join agente as a on ar.idAgente = a.idAgente inner join obrasocial as o on ar.idObra = o.idObra inner join efector as e on ar.idEfector = e.idEfector ORDER BY `ar`.`idArancel` ASC"""
cursor = db.cursor()
cursor.execute(sql1)
resultados = cursor.fetchall()

df = pd.DataFrame(resultados)
df.columns = ['ID','DNI', 'AGENTE', 'PUESTO LABORAL', 'ESTABLECIMIENTO', 'CONCEPTO', 'OBRA SOCIAL', 'MES', 'AÑO', 'IMPORTE', 'PRESTADOR', 'LOCALIDAD', 'PERIODO', 'ESTADO']
df['IMPORTE'] = df['IMPORTE'].map(lambda x: f"${x:.2f}")
df['PUESTO LABORAL'] = df['PUESTO LABORAL'].map(lambda x: f"{x:}")
df['AÑO'] = df['AÑO'].map(lambda x: f"{x:}")
df['DNI'] = df['DNI'].map(lambda x: f"{x:}")
st.write("Listado de Arancelados de la busqueda realizada")
st.dataframe(df.drop(columns=['ID']))
import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_option_menu import option_menu
from sql import *

st.set_page_config(page_icon="logo1.png", page_title="Dashboard UEP", layout='wide', initial_sidebar_state="expanded")

st.markdown("""
    <style>
            .st-emotion-cache-1xf0csu > img{
                border-radius: 100%;
            }
    </style>
""", unsafe_allow_html=True)

resultados = listaArancel()

df = pd.DataFrame(resultados, columns=["IdArancel","Dni","Agente","Concepto","Obra Social","Mes","Año","Importe","Efector","Localidad","Periodo","Control Cobro"])


with st.sidebar:
    st.image('logo1.png', caption="")
    st.text(body='Ingrese los filtros a aplicar: ')
    concepto = st.sidebar.multiselect(
        "Concepto", 
        options=df['Concepto'].unique()        
    )
    obrasocial = st.sidebar.multiselect(
        "Obra Social", 
        options=df['Obra Social'].unique(),
    )
    efector = st.sidebar.multiselect(
        "Hospital/Caps", 
        options=df['Efector'].unique(),
    )

    control = st.sidebar.multiselect(
        "Estado Cobró", 
        options=df['Control Cobro'].unique(),
    )

    check =st.button(label='CONSULTAR')
    if check:
        # Filtrar los datos según las opciones seleccionadas en el sidebar
        if concepto:
            df = df[df['Concepto'].isin(concepto)]
        if obrasocial:
            df = df[df['Obra Social'].isin(obrasocial)]
        if efector:
            df = df[df['Efector'].isin(efector)]
        if control:
            df = df[df['Control Cobro'].isin(control)]    
   
st.dataframe(df)
st.write("-----")

col3, col4, col5, col6 = st.columns(4)
with col3:
    st.info("Total IOSCor")
    lista = ['IOSCOR']
    total_ioscor = df.loc[df['Obra Social'].isin(lista), 'Importe'].sum()
    total_ioscor_formateado = f"${total_ioscor:,.2f}"
    st.metric(label='',value=total_ioscor_formateado)

with col4:
    st.info("Total PAMI")
    lista = ['PAMI']
    total_PAMI = df.loc[df['Obra Social'].isin(lista), 'Importe'].sum()
    total_PAMI_formateado = f"${total_PAMI:,.2f}"
    st.metric(label='',value=total_PAMI_formateado)

with col5:
    st.info("Total RGA")
    lista = ['RGA']
    total_RGA = df.loc[df['Obra Social'].isin(lista), 'Importe'].sum()
    total_RGA_formateado = f"${total_RGA:,.2f}"
    st.metric(label='',value=total_RGA_formateado)

with col6:
    st.info("Total Obras Sociales Varias")
    varios = ['IOSCOR', 'RGA', 'PAMI']
    df_no_excluidos = df[~df['Obra Social'].isin(varios)]
    suma_no_excluidos = df_no_excluidos.groupby('Obra Social')['Importe'].sum().reset_index()
    total_VARIOS_formateado = f"${suma_no_excluidos['Importe'].sum():,.2f}"
    st.metric(label='',value=total_VARIOS_formateado)

st.write("-----")
dfsumobras = totalXObraSocial()

fig1 = px.bar(dfsumobras, x='Obras Sociales', y='Total', color='Obras Sociales')
st.subheader("Total por Obra Social")
st.plotly_chart(fig1)

dfConceptosSum = totalXConcepto()

fig2 = px.pie(dfConceptosSum, names='Concepto', values='Total', hole=.5)

dfCantestado = pd.DataFrame(totalXestado())

df_pivot1 = dfCantestado.pivot_table(
            index="Efector",                   # Filas: fechas
            columns="Control",              # Columnas: tipos de expediente
            margins=True,
            aggfunc= len,                         # Función de agregación: contar las filas
            fill_value=0, 
            margins_name='TOTAL',                                                    # Rellenar con 0 donde no haya datos
)

# Elimina la columna 'TOTAL' si está presente
pivot1_reset = df_pivot1.drop(columns=['TOTAL'], errors='ignore')


fig4 = px.line(pivot1_reset, 
              x=pivot1_reset.index,  
              y=pivot1_reset.columns,  
              labels={'Efector':'Hospital/Caps','value': 'Cantidad', 'Control': 'Control'},
              markers=True)  # Usamos markers=True para agregar puntos sobre las líneas

col1, col2 = st.columns(2)
with col1:
    st.subheader("Total por Concepto")
    st.plotly_chart(fig2)

with col2:
    st.subheader("Distribución estado de cobro por Nosocomio")
    st.plotly_chart(fig4)
    #st.dataframe(pivot1_reset)








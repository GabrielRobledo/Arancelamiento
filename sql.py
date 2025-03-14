import MySQLdb 

# Crear la conexión con MySQL
try:
    db = MySQLdb.connect(host='localhost', user='root', db='arancelamiento')
    cursor = db.cursor()
    print('CONEXION EXITOSA')

except MySQLdb.Error as e:
    # Capturar y mostrar detalles completos del error
    print("Error de conexión:", e)
    print("Detalles del error:", e.args)

c = db.cursor()

def listaArancel ():
    c.execute("""SELECT idArancel, ag.dni, ag.apeYnom, ag.concepto, o.descripcion, a.mes, a.anio, a.importe, e.RazonSocial, e.localidad, a.periodo, a.control FROM `arancelamiento` as a inner join agente as ag on a.idAgente = ag.idAgente inner join obrasocial as o on a.idObra = o.idObra inner join efector as e on a.idEfector = e.idEfector ORDER BY a.idArancel ASC;""")
    datos = c.fetchall()

    return datos

def totalXObraSocial():
    c.execute("""SELECT o.descripcion, SUM(a.importe) as 'Total' FROM arancelamiento as a inner join obrasocial as o on a.idObra = o.idObra GROUP BY o.descripcion""")
    datos = c.fetchall()
    data = []
    for i in datos:
        data.append({"Obras Sociales": i[0], "Total": i[1]})        

    return data

def totalXConcepto():
    c.execute("""SELECT ag.concepto, sum(a.importe) as 'Total' FROM arancelamiento as a inner join agente as ag on a.idAgente = ag.idAgente GROUP BY ag.concepto""")
    datos = c.fetchall()
    data = []
    for i in datos:
        data.append({"Concepto": i[0], "Total": i[1]})
    
    return data

def totalXestado():
    c.execute("""SELECT e.razonsocial, a.control FROM arancelamiento as a inner join efector as e on a.idEfector = e.idEfector;""")
    datos = c.fetchall()
    data = []
    for i in datos:
        data.append({"Efector":i[0], "Control": i[1]})
    
    return data



from flask import Flask, request,jsonify
from constants import FASES
from errors import ERRORS
from db import execute


from datetime import datetime #no se instala nada
def validar_formato_fecha(fecha):
    try:
        datetime.strptime(fecha, '%Y-%m-%d')
        return True
    except ValueError:
        return False


app = Flask(__name__)

@app.route('/partidos/', methods=['GET'] )
def listar_partidos():
    equipo=request.args.get("equipo") or None
    fecha=request.args.get("fecha") or None
    fase=request.args.get("fase") or None
    print("equipo->",equipo)
    print("fecha->",fecha)
    print("fase->",fase)

    filtro_query='' #concatenacion de cada filtro para obtene la query definitiva
    if fase:
        if fase in FASES:
            filtro_query=f"p.fase='{fase}'"
        else:
            return ERRORS["INVALID_FORMAT"]("Fase no existente")
    if fecha:
        if validar_formato_fecha(fecha):
            if filtro_query != '':
                filtro_query=f"{filtro_query} AND "
            filtro_query=f"{filtro_query}p.fecha='{fecha}'"
        else:
            return ERRORS["INVALID_FORMAT"]("Formato o fecha no valida")
    if equipo:
        if filtro_query != '':
            filtro_query=f"{filtro_query} AND "
        filtro_query=f"{filtro_query}('{equipo}' IN (p.equipo_local,p.equipo_visitante))"
    
    if filtro_query == '': resultado=execute("SELECT * FROM prode.partidos WHERE (goles_local IS NULL AND goles_visitante IS NULL)")
    else: resultado=execute(f"SELECT * FROM prode.partidos p WHERE (goles_local IS NULL AND goles_visitante IS NULL) AND {filtro_query}")
    
    if resultado == []: return ERRORS["NOT_FOUND"]("Inexistencia de registros pedidos")
    else: return jsonify(resultado), 200

@app.route('/partidos/<int:id>', methods=['GET'] )
def obtener_partido(id): #asumo por el  <int: id>  recibo siempre id tipo int
    #if id<0: return ERRORS["INVALID_FORMAT"]("Solo se permiten id sin signo")

    resultado=execute(f"SELECT * FROM prode.partidos p WHERE  p.id='{id}'") #devuelve una lista de diccionarios, cada dicc es una fila de la tabla 
    if resultado == []:
        return ERRORS["NOT_FOUND"]("id inexistente")
    else:
        if resultado[0]['goles_local'] is None or resultado[0]['goles_visitante'] is None:
            resultado=execute(f"SELECT id, equipo_local, equipo_visitante, fecha, fase FROM prode.partidos p WHERE  p.id='{id}'")
            return jsonify( resultado ),200
        else:
            resultado=execute(f"SELECT * FROM prode.partidos p WHERE  p.id='{id}'")
            return jsonify( resultado ),200


@app.route('/partidos/<int:id>', methods=['DELETE'] )
def eliminar_partido(id):
    resultado=execute(f"SELECT * FROM prode.partidos p WHERE  p.id='{id}'") #devuelve una lista de diccionarios, cada dicc es una fila de la tabla 
    if resultado == []:
        return ERRORS["NOT_FOUND"]("id inexistente")
    else:
        execute(f"DELETE FROM prode.partidos p WHERE  p.id='{id}'")
        return jsonify({"message": "Eliminado"}),200


if __name__ == '__main__':
    app.run(host="127.0.0.1", port="5000", debug=True)
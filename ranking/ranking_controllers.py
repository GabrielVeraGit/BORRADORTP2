from flask import Flask, request,jsonify
from errors import ERRORS
import querysGet

def paginacion(query_cant_registros,query):
    cant_registros_listdicc=execute(query_cant_registros)
    cant_registros=cant_registros_listdicc[0].get('cant_registros') #nombre_columna q pusieron
    if cant_registros==0: 
        return jsonify({"message": "Sin registros guardados"}),200

    all_args = request.args.to_dict()
    limit=all_args.pop("_limit", 10)
    offset=all_args.pop("_offset",0)
    url_extra=''
    for clave in list( all_args.keys() ):
        var=all_args.get(clave) or None
        if not(var is None):
            url_extra=f"{url_extra}&{clave}={all_args.get(clave)}"

    try:
        limit=int(limit)
        offset=int(offset)
        if limit<=0 or offset<0:
            return ERRORS["INVALID_FORMAT"]("Tipos de datos invalidos")
    except (ValueError, TypeError):
        return ERRORS["INVALID_FORMAT"]("Tipos de datos invalidos")
    
    url_base=request.base_url # ej "http://127.0.0.1:5000/algo"
    url_hateoas={}

    url_hateoas["_first"] = f"{url_base}?_limit={limit}&_offset=0{url_extra}" #firts
    
    if offset > 0: #previ
        pre_offset = offset - limit
        if pre_offset < 0:
            pre_offset = 0  
        url_hateoas["_prev"] = f"{url_base}?_limit={limit}&_offset={pre_offset}{url_extra}"

    if offset + limit < cant_registros: #next
        next_offset = offset + limit
        url_hateoas["_next"] = f"{url_base}?_limit={limit}&_offset={next_offset}{url_extra}"
    
    ultimo_offset = (math.ceil(cant_registros / limit) - 1) * limit #last
    if ultimo_offset < 0:
        ultimo_offset = 0
    url_hateoas["_last"] = f"{url_base}?_limit={limit}&_offset={ultimo_offset}{url_extra}"

    resultado=execute(f"{query} LIMIT %s OFFSET %s",(limit,offset))

    return resultado, url_hateoas

def obtener_ranking():
    resultado, links_hateoas=paginacion(querysGet.ranking['query_cant_registros'],querysGet.ranking['query'])

    if resultado == []: return ERRORS["NOT_FOUND"]("Inexistencia de registros pedidos")
    else: return jsonify(resultado,{"HATEOAS":links_hateoas}), 200
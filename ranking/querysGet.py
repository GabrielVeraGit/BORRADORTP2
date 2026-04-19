#GET RANKING

ranking={
    'query' : 
    '''
SELECT pre.usuario_id AS id_usuario,
    SUM(CASE
        	WHEN (pre.goles_local=par.goles_local) AND (pre.goles_visitante=par.goles_visitante) 
        		AND (par.goles_local!=par.goles_visitante)
        	THEN 3
        	WHEN ( (par.goles_local=par.goles_visitante) AND (pre.goles_local=pre.goles_visitante) )
        		OR ( (par.goles_local>par.goles_visitante) AND (pre.goles_local>pre.goles_visitante) )
        		OR( (par.goles_local<par.goles_visitante) AND (pre.goles_local<pre.goles_visitante) )
      		THEN 1
        	ELSE 0
    	END) 
AS puntos
FROM prode.predicciones pre
INNER JOIN prode.partidos par ON pre.partido_id = par.id 
WHERE (par.goles_local IS NOT NULL) AND (par.goles_visitante IS NOT NULL)
GROUP BY pre.usuario_id
ORDER BY puntos DESC''',

    'query_cant_registros' :
    '''
    SELECT COUNT(*) AS cant_registros
    FROM (
	SELECT pre.usuario_id 
	FROM prode.predicciones pre
	GROUP BY pre.usuario_id) AS cant_registros'''
}


para el ENDPOINT RANKING,
1. ranking_controllers.py MODIFICADO para el codigo necesario
2. db.py !! MODIFICADO ligeramente, por temas de las QUERY-PARAMS, agregue un como nuevo parametro "params=None", y un condicional para ejecutar el "cursor.execute()",no influye en el resto de codigo del repositorio
3. nuevo archivo querysGet.py, contiene las query para el funcionamiento del endpoint Ranking, esta junto a db.py , errors.py .....

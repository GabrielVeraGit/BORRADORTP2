CREATE DATABASE IF NOT EXISTS prode;

USE prode;

-- 1. Tabla de Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

INSERT INTO prode.usuarios(nombre,email)
VALUES('persona0','p0@gmail.com');

-- 2. Tabla de Partidos
CREATE TABLE IF NOT EXISTS partidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipo_local VARCHAR(50) NOT NULL,
    equipo_visitante VARCHAR(50) NOT NULL,
    fecha TIMESTAMP NOT NULL,
    goles_local INT DEFAULT NULL,
    goles_visitante INT DEFAULT NULL,
    fase VARCHAR(50) NOT NULL -- ["FASE_GRUPOS", "OCTAVOS", "CUARTOS", "SEMIFINALES", "FINALES"]
);

INSERT INTO prode.partidos(equipo_local,equipo_visitante,fecha,fase)
VALUES ('eq1','eq2','2026-01-01','SEMIFINALES');


-- 3. Tabla de Predicciones
CREATE TABLE IF NOT EXISTS predicciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    partido_id INT NOT NULL,
    goles_local INT NOT NULL,
    goles_visitante INT NOT NULL,
    
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (partido_id) REFERENCES partidos(id) ON DELETE CASCADE,
    -- RESTRICCIÓN: Un usuario solo puede tener una predicción por cada partido
    UNIQUE(usuario_id, partido_id)
);

INSERT INTO prode.predicciones(usuario_id,partido_id,goles_local,goles_visitante)
VALUES(4,4,7,2)
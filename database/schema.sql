CREATE DATABASE indicadores;

CREATE TABLE dimensiones(
    nombre VARCHAR(40),
    peso INTEGER,
    PRIMARY KEY (nombre)
);

CREATE TABLE subdimensiones(
    nombre VARCHAR(100),
    nombre_dimension VARCHAR(40),
    peso INTEGER,
    PRIMARY KEY (nombre),
    FOREIGN KEY (nombre_dimension) REFERENCES dimensiones (nombre)
);

CREATE TABLE definicion_indicadores(
    nombre VARCHAR(100),
    nombre_subdimension VARCHAR(40),
    importancia VARCHAR(30),
    formula VARCHAR(50),
    fuente VARCHAR(50),
    origen_indicador VARCHAR(30),
    PRIMARY KEY (nombre),
    FOREIGN KEY (nombre_subdimension) REFERENCES subdimensiones (nombre)
);

CREATE TABLE componentes_indicador(
    id INTEGER AUTO_INCREMENT,
    nombre_indicador VARCHAR(100),
    descripcion_dato VARCHAR(100),
    fuente_tabla VARCHAR(100),
    PRIMARY KEY (id),
    FOREIGN KEY (nombre_indicador) REFERENCES definicion_indicadores (nombre)
);

CREATE TABLE resultado_indicadores(
    id INTEGER AUTO_INCREMENT,
    nombre_indicador VARCHAR(100),
    valor_calculado DECIMAL(5,2),
    pais VARCHAR(30),
    provincia VARCHAR(30),
    periodo INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (nombre_indicador) REFERENCES definicion_indicadores (nombre)
);

CREATE TABLE datos_crudos(
    id INTEGER AUTO_INCREMENT,
    nombre_indicador VARCHAR(100),
    valor DECIMAL,
    unidad VARCHAR(30),
    pais VARCHAR(30),
    provincia VARCHAR(30),
    periodo INTEGER,
    descripcion_dato VARCHAR(50),
    PRIMARY KEY (id),
    FOREIGN KEY (nombre_indicador) REFERENCES definicion_indicadores (nombre)
);


CREATE TABLE datos_macro(
    id INTEGER AUTO_INCREMENT,
    valor DECIMAL,
    unidad VARCHAR(30),
    pais VARCHAR(30),
    provincia VARCHAR(30),
    periodo INTEGER,
    descripcion_dato VARCHAR(50),
    PRIMARY KEY (id)
);
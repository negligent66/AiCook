CREATE DATABASE AI_COOK;

USE AI_COOK;

CREATE TABLE IF NOT EXISTS CATEGORIA (
    idCategoria INT AUTO_INCREMENT NOT NULL,
    nome VARCHAR(25),
    PRIMARY KEY (idCategoria)
);

INSERT INTO CATEGORIA(nome) VALUES ("Primo"), ("Secondo"), ("Contorno"), ("Dessert");

CREATE TABLE IF NOT EXISTS RICETTA (
    idRicetta INT AUTO_INCREMENT NOT NULL,
    idCategoria INT,
    nome VARCHAR(255) NOT NULL,
    descrizione VARCHAR(255),
    tempo INT,
    difficolta enum("Non presente", "Bassa", "Media", "Alta"),
    PRIMARY KEY (idRicetta),
    FOREIGN KEY (idCategoria) REFERENCES CATEGORIA(idCategoria)
);

CREATE TABLE IF NOT EXISTS INGREDIENTI (
    idIngrediente INT AUTO_INCREMENT NOT NULL,
    nome VARCHAR(255),
    PRIMARY KEY (idIngrediente)
);

CREATE TABLE IF NOT EXISTS RICETTEINGREDIENTI (
    idIngrediente INT NOT NULL,
    idRicetta INT NOT NULL,
    quantita INT,
    unita_di_misura VARCHAR(10),    /* Se non ha un unita di misura, scrivere "unita'" */
    FOREIGN KEY (idIngrediente) REFERENCES INGREDIENTI(idIngrediente),
    FOREIGN KEY (idRicetta) REFERENCES RICETTA(idRicetta)
);

CREATE TABLE IF NOT EXISTS PREPARAZIONE (
    idPreparazione INT AUTO_INCREMENT NOT NULL,
    idRicetta INT NOT NULL,
    progressivo INT,
    descrizione VARCHAR(255),
    PRIMARY KEY (idPreparazione),
    FOREIGN KEY (idRicetta) REFERENCES RICETTA(idRicetta)
);

CREATE USER 'Cuoco'@'%' IDENTIFIED BY 'Password';
GRANT SELECT, INSERT ON AI_COOK.* TO 'Cuoco'@'%';
FLUSH PRIVILEGES;


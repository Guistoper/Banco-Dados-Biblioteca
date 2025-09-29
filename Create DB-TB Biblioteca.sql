--- DATABASE CREATE ---

DROP DATABASE IF EXISTS biblioteca;
CREATE DATABASE biblioteca;
USE biblioteca;

--- TABLE AUTORES CREATE ---

CREATE TABLE tb_autores (
	id_autor INT PRIMARY KEY AUTO_INCREMENT,
	nome VARCHAR(100) NOT NULL
);

--- TABLE LIVROS CREATE ---

CREATE TABLE tb_livros (
	id_livro INT PRIMARY KEY AUTO_INCREMENT,
	codigo INT,
	id_autor INT NOT NULL,
	quantidade INT NOT NULL,
	nome VARCHAR(255) NOT NULL,
	sinopse TEXT,
	FOREIGN KEY (id_autor) REFERENCES tb_autores(id_autor)
);

--- TABLE USUARIOS CREATE ---

CREATE TABLE tb_usuarios (
	id_ra INT PRIMARY KEY NOT NULL,
	nome VARCHAR(100) NOT NULL,
	telefone VARCHAR(20)
);

--- TABLE GENEROS CREATE ---

CREATE TABLE tb_generos (
	id_genero INT PRIMARY KEY AUTO_INCREMENT,
	genero VARCHAR(100) NOT NULL
);

--- TABLE LIVROS-GENEROS CREATE ---

CREATE TABLE tb_livros_generos (
	id_livro INT NOT NULL,
	id_genero INT NOT NULL,
	FOREIGN KEY (id_livro) REFERENCES tb_livros(id_livro),
	FOREIGN KEY (id_genero) REFERENCES tb_generos(id_genero)
);

--- TABLE EMPRESTIMOS CREATE ---

CREATE TABLE tb_emprestimos (
	id_emp INT PRIMARY KEY AUTO_INCREMENT,
	id_ra INT NOT NULL,
	id_livro INT NOT NULL,
	quantidade INT NOT NULL,
	data DATE NOT NULL,
	prazo DATE NOT NULL,
	atraso BOOLEAN,
	FOREIGN KEY (id_ra) REFERENCES tb_usuarios(id_ra),
	FOREIGN KEY (id_livro) REFERENCES tb_livros(id_livro)
);
	
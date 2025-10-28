DROP DATABASE IF EXISTS biblioteca;
CREATE DATABASE biblioteca;
USE biblioteca;

CREATE TABLE tb_autores (
	id_autor INT PRIMARY KEY AUTO_INCREMENT,
	autor VARCHAR(100) NOT NULL
);

CREATE TABLE tb_generos (
	id_genero INT PRIMARY KEY AUTO_INCREMENT,
	genero VARCHAR(100) NOT NULL
);

CREATE TABLE tb_livros (
	id_livro INT PRIMARY KEY AUTO_INCREMENT,
	codigo INT,
	id_autor INT,
	id_genero INT,
	quantidade INT NOT NULL,
	livro VARCHAR(255) NOT NULL,
	sinopse TEXT,
	FOREIGN KEY (id_autor) REFERENCES tb_autores(id_autor),
	FOREIGN KEY (id_genero) REFERENCES tb_generos(id_genero)
);

CREATE TABLE tb_usuarios (
	id_ra BIGINT PRIMARY KEY NOT NULL,
	nome VARCHAR(100) NOT NULL,
	telefone VARCHAR(20)
);

CREATE TABLE tb_emprestimos (
	id_emp INT PRIMARY KEY AUTO_INCREMENT,
	id_ra BIGINT NOT NULL,
	id_livro INT NOT NULL,
	quantidade INT NOT NULL,
	data DATE NOT NULL,
	prazo DATE NOT NULL,
	atraso BOOLEAN,
	FOREIGN KEY (id_ra) REFERENCES tb_usuarios(id_ra),
	FOREIGN KEY (id_livro) REFERENCES tb_livros(id_livro)
)
	
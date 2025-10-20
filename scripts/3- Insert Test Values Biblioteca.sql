INSERT INTO tb_autores (autor) VALUES
	('Miguel de Cervantes'),
	('Antoine de Saint-Exupéry'),
	('Charles Dickens'),
	('J. R. R. Tolkien'),
	('J. K. Rowling');

INSERT INTO tb_generos (genero) VALUES
	('Romance'),
	('Fantasia'),
	('Fábula'),
	('Paródia'),
	('Ficção');

INSERT INTO tb_livros (id_autor, id_genero, quantidade, livro) VALUES
	(1, 1, 4, 'Dom Quixote'),
	(2, 2, 7, 'O Pequeno Príncipe'),
	(3, 3, 1, 'Um Conto de Duas Cidades'),
	(4, 4, 9, 'O Senhor dos Anéis'),
	(5, 5, 15, 'Harry Potter e a Pedra Filosofal');

INSERT INTO tb_usuarios (id_ra, nome) VALUES
	(1125762433, 'Guilherme Menezes'),
	(1093592837, 'Stephanie Rodrigues'),
	(1116835101, 'Marcela de Lima'),
	(1094326823, 'Nycole Alves'),
	(1093592680, 'Jhennifer Rodrigues');

INSERT INTO tb_emprestimos (id_ra, id_livro, quantidade, data, prazo) VALUES
	(1125762433, 2, 5, '2025-09-29', '2025-10-09'),
	(1094326823, 5, 3, '2025-08-30', '2025-09-06'),
	(1116835101, 3, 1, '2025-10-15', '2025-10-29'),
	(1093592837, 4, 2, '2025-09-03', '2025-09-17'),
	(1093592837, 1, 1, '2025-09-24', '2025-10-15')
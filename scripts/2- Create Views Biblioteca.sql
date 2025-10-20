CREATE VIEW livros AS
SELECT t1.id_livro, t1.codigo, t1.livro, t2.autor, t3.genero, t1.quantidade, t1.sinopse
FROM tb_livros AS t1
INNER JOIN tb_autores AS t2 ON t2.id_autor = t1.id_autor
INNER JOIN tb_generos AS t3 ON t3.id_genero = t1.id_genero;

CREATE VIEW emprestimos AS
SELECT t1.id_emp, t1.id_ra, t2.nome, t3.livro, t4.autor, t5.genero, t1.quantidade, t1.data, t1.prazo, t1.atraso
FROM tb_emprestimos AS t1
INNER JOIN tb_usuarios AS t2 ON t2.id_ra = t1.id_ra
INNER JOIN tb_livros AS t3 ON t3.id_livro = t1.id_livro
INNER JOIN tb_autores AS t4 ON t4.id_autor = t3.id_autor
INNER JOIN tb_generos AS t5 ON t5.id_genero = t3.id_genero
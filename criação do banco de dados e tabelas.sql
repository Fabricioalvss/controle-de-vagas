-- Cria o banco
CREATE DATABASE controle_academico;
USE controle_academico;

-- Tabela de alunos
CREATE TABLE alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100)
);

-- Tabela de cursos
CREATE TABLE cursos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    carga_horaria INT
);

-- Tabela de matrícula (relacionamento entre aluno e curso)
CREATE TABLE matriculas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT,
    id_curso INT,
    nota DECIMAL(5,2),
    FOREIGN KEY (id_aluno) REFERENCES alunos(id),
    FOREIGN KEY (id_curso) REFERENCES cursos(id)
);
ALTER TABLE alunos ADD COLUMN curso_id INT;
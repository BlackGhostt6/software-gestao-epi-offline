PRAGMA foreign_keys = ON;

-- =========================
-- TABELA EPI
-- =========================
DROP TABLE IF EXISTS epi;

CREATE TABLE epi (
  nome_epi TEXT NOT NULL,
  tipo_epi TEXT NOT NULL,
  certificado_aprovacao_epi TEXT NOT NULL,
  validade_certificado_aprovacao TEXT NOT NULL,
  PRIMARY KEY (certificado_aprovacao_epi)
);

INSERT INTO epi VALUES
('Capacete','Proteção Cabeça','CA 000001','2026-06-25'),
('Óculos de proteção','Proteção','CA 000002','2026-07-18'),
('Luvas de couro','Proteção Mãos','CA 000003','2026-08-05'),
('Botina de segurança','Proteção Pés','CA 000004','2026-09-12'),
('Protetor auricular','Proteção Auditiva','CA 000005','2026-06-21'),
('Máscara PFF2','Proteção Respiratória','CA 000006','2026-10-08'),
('Cinto de segurança','Altura','CA 000007','2027-01-15'),
('Capacete com viseira','Proteção Completa','CA 000008','2026-11-03'),
('Luvas nitrílicas','Químico','CA 000009','2026-07-02'),
('Avental de couro','Proteção Corpo','CA 000010','2027-03-18'),
('Máscara solda','Soldagem','CA 000011','2026-12-10'),
('Respirador semi facial','Respiratório','CA 000012','2026-06-28'),
('Luva térmica','Alta temperatura','CA 000013','2027-05-20'),
('Bota PVC','Impermeável','CA 000014','2026-08-27'),
('Óculos ampla visão','Olhos','CA 000015','2026-07-09'),
('Protetor facial','Face shield','CA 000016','2027-02-14'),
('Macacão químico','Químico','CA 000017','2026-11-22'),
('Capacete industrial','Cabeça','CA 000018','2028-01-11'),
('Luva látex','Geral','CA 000019','2026-06-23'),
('Protetor solar EPI','UV','CA 000020','2026-09-30');

-- =========================
-- TABELA FUNCIONARIOS
-- =========================
DROP TABLE IF EXISTS funcionarios;

CREATE TABLE funcionarios (
  matricula_funcionario TEXT PRIMARY KEY,
  nome_funcionario TEXT NOT NULL,
  cpf_funcionario TEXT NOT NULL UNIQUE,
  setor_funcionario TEXT NOT NULL,
  funcao_funcionario TEXT NOT NULL,
  data_admissao_funcionario TEXT NOT NULL,
  telefone TEXT NOT NULL,
  email TEXT NOT NULL,
  whatsapp TEXT
);

INSERT INTO funcionarios VALUES
('FUNC0001','Ana Silva','111.111.111-01','Produção','Operador','2022-01-10','31999990001','ana@empresa.com','31999990001'),
('FUNC0002','Bruno Lima','111.111.111-02','Manutenção','Técnico','2021-03-15','31999990002','bruno@empresa.com','31999990002'),
('FUNC0003','Carla Mendes','111.111.111-03','RH','Analista','2020-07-20','31999990003','carla@empresa.com','31999990003'),
('FUNC0004','Diego Alves','111.111.111-04','Produção','Operador','2019-11-11','31999990004','diego@empresa.com','31999990004'),
('FUNC0005','Elisa Rocha','111.111.111-05','Segurança','Vigilante','2023-02-01','31999990005','elisa@empresa.com','31999990005'),
('FUNC0006','Felipe Santos','111.111.111-06','Logística','Auxiliar','2021-08-08','31999990006','felipe@empresa.com','31999990006'),
('FUNC0007','Gabriela Costa','111.111.111-07','TI','Suporte','2022-05-05','31999990007','gabriela@empresa.com','31999990007'),
('FUNC0008','Henrique Silva','111.111.111-08','Produção','Operador','2020-09-09','31999990008','henrique@empresa.com','31999990008'),
('FUNC0009','Isabela Pereira','111.111.111-09','Manutenção','Eletricista','2018-12-12','31999990009','isa@empresa.com','31999990009'),
('FUNC0010','João Ferreira','111.111.111-10','RH','Assistente','2023-06-06','31999990010','joao@empresa.com','31999990010'),
('FUNC0011','Karen Oliveira','111.111.111-11','Produção','Operador','2022-10-10','31999990011','karen@empresa.com','31999990011'),
('FUNC0012','Lucas Gomes','111.111.111-12','Logística','Motorista','2021-01-01','31999990012','lucas@empresa.com','31999990012'),
('FUNC0013','Mariana Souza','111.111.111-13','TI','Dev','2020-04-04','31999990013','mari@empresa.com','31999990013'),
('FUNC0014','Nicolas Martins','111.111.111-14','Produção','Operador','2019-05-05','31999990014','nicolas@empresa.com','31999990014'),
('FUNC0015','Olivia Barros','111.111.111-15','Segurança','Vigilante','2023-07-07','31999990015','olivia@empresa.com','31999990015'),
('FUNC0016','Paulo Teixeira','111.111.111-16','RH','Analista','2022-02-02','31999990016','paulo@empresa.com','31999990016'),
('FUNC0017','Rafaela Nunes','111.111.111-17','Produção','Operador','2021-09-09','31999990017','rafa@empresa.com','31999990017'),
('FUNC0018','Samuel Vieira','111.111.111-18','Manutenção','Técnico','2020-06-06','31999990018','samuel@empresa.com','31999990018'),
('FUNC0019','Tatiane Souza','111.111.111-19','TI','Suporte','2019-03-03','31999990019','tatiane@empresa.com','31999990019'),
('FUNC0020','Ulisses Dias','111.111.111-20','Logística','Auxiliar','2023-11-11','31999990020','ulisses@empresa.com','31999990020');

-- =========================
-- TABELA REGISTROS
-- =========================
DROP TABLE IF EXISTS registros;

CREATE TABLE registros (
  matricula_funcionario TEXT NOT NULL,
  ca_EPI TEXT NOT NULL,
  data_entrega TEXT NOT NULL,
  data_devolucao TEXT,
  data_troca TEXT,
  motivo_devolucao TEXT
);

INSERT INTO registros VALUES
('FUNC0001','CA 000001','2026-01-10','2026-02-10',NULL,'Desgaste'),
('FUNC0002','CA 000002','2026-01-11','2026-03-11',NULL,NULL),
('FUNC0003','CA 000003','2026-01-12','2026-04-12',NULL,'Perda'),
('FUNC0004','CA 000004','2026-01-13','2026-05-13',NULL,NULL),
('FUNC0005','CA 000005','2026-01-14','2026-06-14',NULL,'Troca'),
('FUNC0006','CA 000006','2026-01-15','2026-07-15',NULL,NULL),
('FUNC0007','CA 000007','2026-01-16','2026-08-16',NULL,'Dano'),
('FUNC0008','CA 000008','2026-01-17','2026-09-17',NULL,NULL),
('FUNC0009','CA 000009','2026-01-18','2026-10-18',NULL,'Desgaste'),
('FUNC0010','CA 000010','2026-01-19','2026-11-19',NULL,NULL),
('FUNC0011','CA 000011','2026-01-20','2026-12-20',NULL,NULL),
('FUNC0012','CA 000012','2026-01-21','2026-01-21',NULL,'Troca'),
('FUNC0013','CA 000013','2026-01-22','2026-02-22',NULL,NULL),
('FUNC0014','CA 000014','2026-01-23','2026-03-23',NULL,'Perda'),
('FUNC0015','CA 000015','2026-01-24','2026-04-24',NULL,NULL),
('FUNC0016','CA 000016','2026-01-25','2026-05-25',NULL,'Dano'),
('FUNC0017','CA 000017','2026-01-26','2026-06-26',NULL,NULL),
('FUNC0018','CA 000018','2026-01-27','2026-07-27',NULL,NULL),
('FUNC0019','CA 000019','2026-01-28','2026-08-28',NULL,'Troca'),
('FUNC0020','CA 000020','2026-01-29','2026-09-29',NULL,NULL);
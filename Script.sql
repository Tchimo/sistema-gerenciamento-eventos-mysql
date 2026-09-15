-- Gera��o de Modelo f�sico
-- Sql ANSI 2003 - brModelo.



CREATE TABLE Sessao (
Hora_fim timestamp,
Hora_inicio timestamp,
Nome_sessao varchar(100),
Id_sessao integer PRIMARY KEY,
Data timestamp,
Id_agenda integer
)

CREATE TABLE Evento (
Tipo_evento varchar(100),
Nome_evento varchar(100),
Id_evento integer PRIMARY KEY,
Id_local integer,
Id_org integer
)

CREATE TABLE Patroci_evento (
data_D timestamp,
Id_Patro_evento integer PRIMARY KEY,
Cod_patrocina integer,
Id_evento integer
)

CREATE TABLE Local (
Nome_local varchar(100),
Endereco varchar(120),
Id_local integer PRIMARY KEY,
Capacidade integer
)

CREATE TABLE Ator_evento (
Id_evento integer,
ID_ator integer,
FOREIGN KEY(Id_evento) REFERENCES Evento (Id_evento)
)

CREATE TABLE Ator (
Nome_ator varchar(100),
Contato_email varchar(50),
Papel_Ator varchar(100),
Descricao varchar(100),
ID_ator integer PRIMARY KEY
)

CREATE TABLE Ingresso (
Preco numeric,
Id_ingresso integer PRIMARY KEY,
Tipo_ingresso varchar(10),
Id_participante integer,
Id_evento integer,
FOREIGN KEY(Id_evento) REFERENCES Evento (Id_evento)
)

CREATE TABLE Colaboradore (
Funcao varchar(50),
Contato integer,
CPF integer,
Nome_colabo varchar(100),
Id_colaborador integer PRIMARY KEY
)

CREATE TABLE Vinculado (
Id_colaborador integer,
Id_evento integer,
FOREIGN KEY(Id_colaborador) REFERENCES Colaboradore (Id_colaborador),
FOREIGN KEY(Id_evento) REFERENCES Evento (Id_evento)
)

CREATE TABLE Agenda (
Id_agenda integer PRIMARY KEY,
Data_inicio timestamp,
Data_fim timestamp,
Id_evento integer,
FOREIGN KEY(Id_evento) REFERENCES Evento (Id_evento)
)

CREATE TABLE Pessoa_Fisica (
Tipo_organizacao varchar(150),
CPF varchar(11),
Cod_patrocina integer PRIMARY KEY
)

CREATE TABLE Pessoa_Juridica (
CNPJ varchar(15),
Sexo varchar(10),
Cod_patrocina integer PRIMARY KEY
)

CREATE TABLE Participante (
CPF integer,
Contato varchar(50),
Endereco_partici varchar(100),
Nome_participante varchar(100),
Id_participante integer PRIMARY KEY
)

CREATE TABLE Avaliacao (
Data_avaliacao timestamp,
Comentario varchar(400),
Id_Avaliacao integer PRIMARY KEY,
Nota integer,
Id_participante integer,
Id_evento integer,
FOREIGN KEY(Id_evento) REFERENCES Evento (Id_evento)
)

CREATE TABLE Organizacao (
Tipo_Organizacao varchar(100),
Contato_org varchar(50),
Nome_org varchar(100),
Id_org integer PRIMARY KEY
)

CREATE TABLE Patrocininador (
Cod_patrocina integer PRIMARY KEY,
Nome varchar(100),
Email varchar(50),
Valor_do_Patro numeric
)

ALTER TABLE Sessao ADD FOREIGN KEY(Id_agenda) REFERENCES Agenda (Id_agenda)
ALTER TABLE Evento ADD FOREIGN KEY(Id_local) REFERENCES Local (Id_local)
ALTER TABLE Evento ADD FOREIGN KEY(Id_org) REFERENCES Organizacao (Id_org)
ALTER TABLE Patroci_evento ADD FOREIGN KEY(Cod_patrocina) REFERENCES Patrocininador (Cod_patrocina)
ALTER TABLE Patroci_evento ADD FOREIGN KEY(Id_evento) REFERENCES Evento (Id_evento)
ALTER TABLE Ator_evento ADD FOREIGN KEY(ID_ator) REFERENCES Ator (ID_ator)
ALTER TABLE Ingresso ADD FOREIGN KEY(Id_participante) REFERENCES Participante (Id_participante)
ALTER TABLE Pessoa_Fisica ADD FOREIGN KEY(Cod_patrocina) REFERENCES Patrocininador (Cod_patrocina)
ALTER TABLE Pessoa_Juridica ADD FOREIGN KEY(Cod_patrocina) REFERENCES Patrocininador (Cod_patrocina)
ALTER TABLE Avaliacao ADD FOREIGN KEY(Id_participante) REFERENCES Participante (Id_participante)
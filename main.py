import os
import re
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

load_dotenv()  

"""Variáveis"""
"""Valores para criação de tabelas do banco de dados"""
tables = {'LOCAL': (
    """CREATE TABLE `LOCAL` (
        `Id_local` integer PRIMARY KEY NOT NULL,
        `Nome_local` varchar(100) NOT NULL,
        `Endereco` varchar(120) NOT NULL,
        `Capacidade` integer NOT NULL  
    ) ENGINE=InnoDB"""),
    'ATOR': (
        """CREATE TABLE `ATOR` (
            `Id_ator` integer PRIMARY KEY NOT NULL,
            `Nome_ator` varchar(100) NOT NULL,
            `Contato_email` varchar(100) NOT NULL,
            `Papel_ator` varchar(100) NOT NULL,
            `Descricao` varchar(100) NOT NULL
            
        ) ENGINE=InnoDB"""),
    'COLABORADOR': (
        """CREATE TABLE `COLABORADOR` (
            `Id_colaborador` integer PRIMARY KEY NOT NULL,
            `Funcao` varchar(50) NOT NULL,
            `Contato` varchar(11) NOT NULL,
            `CPF` varchar(11) NOT NULL,
            `Nome_colabo` varchar(100) NOT NULL
        ) ENGINE=InnoDB"""),
    'PARTICIPANTE': (
        """CREATE TABLE `PARTICIPANTE` (
            `Id_participante` integer PRIMARY KEY NOT NULL,
            `CPF` varchar(11) NOT NULL,
            `Contato` varchar(50) NOT NULL,
            `Endereco_partici` varchar(100) NOT NULL,
            `Nome_participante` varchar(100) NOT NULL
        ) ENGINE=InnoDB"""),
    'ORGANIZACAO': (
        """CREATE TABLE `ORGANIZACAO` (
            `Id_org` integer PRIMARY KEY NOT NULL,
            `Tipo_Organizacao` varchar(100) NOT NULL,
            `Contato_org` varchar(50) NOT NULL,
            `Nome_org` varchar(100) NOT NULL
        ) ENGINE=InnoDB"""),
    'PATROCINADOR': (
        """CREATE TABLE `PATROCINADOR` (
            `Cod_patrocina` integer PRIMARY KEY NOT NULL,
            `Nome` varchar(100) NOT NULL,
            `Email` varchar(50) NOT NULL,
            `Valor_do_Patro` numeric (6,2) NOT NULL
        ) ENGINE=InnoDB"""),
    'PESSOA_FISICA': (
        """CREATE TABLE `PESSOA_FISICA` (
            `Sexo` varchar(11) NOT NULL,
            `CPF` varchar(11) NOT NULL,
            `Cod_patrocina` integer PRIMARY KEY NOT NULL,
             FOREIGN KEY(Cod_patrocina) REFERENCES PATROCINADOR (Cod_patrocina)
        ) ENGINE=InnoDB"""),
    'PESSOA_JURIDICA': (
        """CREATE TABLE `PESSOA_JURIDICA` (
            `Tipo_organizacao` varchar(150),
            `CNPJ` varchar(15),
            `Cod_patrocina` integer PRIMARY KEY,
             FOREIGN KEY(Cod_patrocina) REFERENCES PATROCINADOR (Cod_patrocina)
        ) ENGINE=InnoDB"""),
    'EVENTO': (
        """CREATE TABLE `EVENTO` (
            `Id_evento` integer PRIMARY KEY NOT NULL,
            `Tipo_evento` varchar(8) NOT NULL,
            `Nome_evento` varchar(100) NOT NULL,  	
            `Id_local` integer NOT NULL,
            `Id_org` integer NOT NULL,
             FOREIGN KEY(Id_local) REFERENCES Local (Id_local),
             FOREIGN KEY(Id_org) REFERENCES Organizacao (Id_org)
        ) ENGINE=InnoDB"""),
    'ATOR_EVENTO': (
        """CREATE TABLE `ATOR_EVENTO` (
            `Id_evento` integer NOT NULL,
            `ID_ator` integer NOT NULL,
             FOREIGN KEY(Id_evento) REFERENCES Evento (Id_evento),
             FOREIGN KEY(ID_ator) REFERENCES Ator (ID_ator)
        ) ENGINE=InnoDB"""),
    'PATROCI_EVENTO': (
        """CREATE TABLE `PATROCI_EVENTO` (
            `Id_Patro_evento` integer PRIMARY KEY NOT NULL,
            `data_D` timestamp NOT NULL,
            `Cod_patrocina` integer NOT NULL,
            `Id_evento` integer NOT NULL,
             FOREIGN KEY(Cod_patrocina) REFERENCES Patrocinador (Cod_patrocina),
             FOREIGN KEY(Id_evento) REFERENCES Evento (Id_evento)
        ) ENGINE=InnoDB"""),
    'INGRESSO': (
        """CREATE TABLE `INGRESSO` (
            `Id_ingresso` integer PRIMARY KEY NOT NULL,
            `Preco` numeric (6,2) NOT NULL,
            `Tipo_ingresso` varchar(5) NOT NULL,
            `Id_participante` integer NOT NULL,
            `Id_evento` integer NOT NULL,
             FOREIGN KEY(Id_evento) REFERENCES Evento (Id_evento),
             FOREIGN KEY(Id_participante) REFERENCES Participante (Id_participante),
            CHECK (`Tipo_ingresso` in ('Vip', 'Geral'))
        ) ENGINE=InnoDB"""),
    'AVALIACAO': (
        """CREATE TABLE `AVALIACAO` (
            `Id_Avaliacao` integer PRIMARY KEY NOT NULL,
            `Data_avaliacao` timestamp,
            `Comentario` varchar(400),
            `Nota` integer,
            `Id_participante` integer,
            `Id_evento` integer,
             FOREIGN KEY(Id_evento) REFERENCES Evento (Id_evento),
             FOREIGN KEY(Id_participante) REFERENCES Participante (Id_participante)
        ) ENGINE=InnoDB"""),
    'VINCULADO': (
        """CREATE TABLE `VINCULADO` (
            `Id_colaborador` integer NOT NULL,
            `Id_evento` integer NOT NULL,
             FOREIGN KEY(Id_colaborador) REFERENCES Colaborador (Id_colaborador),
             FOREIGN KEY(Id_evento) REFERENCES Evento (Id_evento)
        ) ENGINE=InnoDB"""),
    'AGENDA': (
        """CREATE TABLE `AGENDA` (
            `Id_agenda` integer PRIMARY KEY NOT NULL,
            `Data_inicio` timestamp NOT NULL,
            `Data_fim` timestamp NOT NULL,
            `Id_evento` integer NOT NULL,
             FOREIGN KEY(Id_evento) REFERENCES Evento (Id_evento)
        ) ENGINE=InnoDB"""),
    'SESSAO': (
        """CREATE TABLE `SESSAO` (
            `Id_sessao` integer PRIMARY KEY NOT NULL,
            `Hora_inicio` timestamp NOT NULL,
            `Hora_fim` timestamp NOT NULL,
            `Nome_sessao` varchar(100) NOT NULL,
            `Data` timestamp NOT NULL,
            `Id_agenda` integer NOT NULL,
            FOREIGN KEY(Id_agenda) REFERENCES Agenda (Id_agenda)
        ) ENGINE=InnoDB"""),
}

# Valores para serem inseridos no Banco de Dados
inserts = {'LOCAL': (
    """insert into LOCAL (Id_local, Nome_local, Endereco, Capacidade) values
        (1, 'Centro de Convenções', 'Av. Principal, 123', 1000),
        (2, 'Auditório Municipal', 'Rua das Flores, 456', 500),
        (3, 'Teatro Municipal', 'Praça Central, 789', 700),
        (4, 'Centro de Eventos', 'Av. Comercial, 234', 1200),
        (5, 'Salão de Festas', 'Rua das Estrelas, 567', 300),
        (6, 'Ginásio Esportivo', 'Av. Esportiva, 890', 1500),
        (7, 'Casa de Shows', 'Rua das Bandas, 1234', 800),
        (8, 'Centro Cultural', 'Av. Cultural, 5678', 600),
        (9, 'Pavilhão de Exposições', 'Rua das Exposições, 901', 2000)"""),
    'ATOR': (
    """insert into ATOR (Id_ator, Nome_ator, Contato_email, Papel_ator, Descricao) values
        (1, 'Wizkid', 'joao.silva@gmail.com', 'Musico', 'Afrobeat'),
        (2, 'Maria Santos', 'maria.santos@hotmail.com', 'Palestrante', 'Especialista em Marketing Digital'),
        (3, 'Carlos Oliveira', 'carlos.oliveira@outlook.com', 'Musico', 'Guitarrista profissional'),
        (4, 'Ana Souza', 'ana.souza@yahoo.com', 'Palestrante', 'Consultora Financeira'),
        (5, 'Chris Brown', 'pedro.pereira@gmail.com', 'Musico', 'R&B'),
        (6, 'Juliana Costa', 'juliana.costa@hotmail.com', 'Palestrante', 'Coach de Carreira'),
        (7, 'Marcos Lima', 'marcos.lima@outlook.com', 'Musico', 'Baterista experiente'),
        (8, 'Fernanda Alves', 'fernanda.alves@yahoo.com', 'Palestrante', 'Psicóloga Clínica'),
        (9, 'Rafael Santos', 'rafael.santos@gmail.com', 'Musico', 'Violoncelista talentoso'),
        (10, 'Larissa Oliveira', 'larissa.oliveira@hotmail.com', 'Palestrante', 'Advogada especializada em direitos humanos'),
        (11, 'Burna Boy', 'rafael.santos@outlook.com', 'Musico', 'Afrobeat'),
        (12, 'Camila Alves', 'camila.alves@gmail.com', 'Palestrante', 'Especialista em marketing digital'),
        (13, 'Davido', 'bruno.ferreira@yahoo.com', 'Musico', 'Afrobeat'),
        (14, 'Isabela Lima', 'isabela.lima@outlook.com', 'Palestra', 'Violencia contra mulheres'),
        (15, 'Asake', 'thiago.martins@gmail.com', 'Musico', 'Afrobeat'),
        (16, 'Fernanda Silva', 'fernanda.silva@hotmail.com', 'Palestra', 'Aquecimento Global'),
        (17, 'Focalist', 'guilherme.costa@yahoo.com', 'Musico', 'Amapiano'),
        (18, 'Patrícia Oliveira', 'patricia.oliveira@gmail.com', 'Palestrante', 'Advogada especializada'),
        (19, 'Major Keys', 'lucas.goncalves@outlook.com', 'Musica', 'Amapiano'),
        (20, 'Amanda Ferreira', 'amanda.ferreira@hotmail.com', 'Palestrante', 'Consultora de RH')"""
),
    'COLABORADOR': (
        """insert into COLABORADOR (Id_colaborador, Funcao, Contato, CPF, Nome_colabo) VALUES
            (1, 'Técnico de Som', '1234567890', '11122233344', 'Lucas Alves'),
            (2, 'Coordenador de Eventos', '2345678901', '22233344455', 'Mariana Costa'),
            (3, 'Segurança', '3456789012', '33344455566', 'Carlos Lima'),
            (4, 'Recepcionista', '4567890123', '44455566677', 'Ana Beatriz'),
            (5, 'Assistente Administrativo', '5678901234', '55566677788', 'Pedro Henrique'),
            (6, 'Limpeza', '6789012345', '66677788899', 'Júlia Fernandes'),
            (7, 'Motorista', '7890123456', '77788899900', 'Roberto Silva'),
            (8, 'Catering', '8901234567', '88899900011', 'Fernanda Souza'),
            (9, 'Técnico de Iluminação', '9012345678', '99900011122', 'Ricardo Santos'),
            (10, 'Produtor', '0123456789', '00011122233', 'Carolina Oliveira')"""),
    'PARTICIPANTE': (
        """insert into PARTICIPANTE (Id_participante, CPF, Contato, Endereco_partici, Nome_participante) VALUES
            (1, '11122233344', 'joao.silva@example.com', 'Rua das Flores, 123', 'João Silva'),
            (2, '22233344455', 'maria.santos@example.com', 'Av. Principal, 456', 'Maria Santos'),
            (3, '33344455566', 'carlos.oliveira@example.com', 'Praça Central, 789', 'Carlos Oliveira'),
            (4, '44455566677', 'ana.souza@example.com', 'Rua da Paz, 101', 'Ana Souza'),
            (5, '55566677788', 'pedro.pereira@example.com', 'Av. Brasil, 202', 'Pedro Pereira'),
            (6, '66677788899', 'juliana.costa@example.com', 'Rua das Palmeiras, 303', 'Juliana Costa'),
            (7, '77788899900', 'marcos.lima@example.com', 'Av. Rio Branco, 404', 'Marcos Lima'),
            (8, '88899900011', 'fernanda.alves@example.com', 'Rua da Alegria, 505', 'Fernanda Alves'),
            (9, '99900011122', 'rafael.santos@example.com', 'Av. Liberdade, 606', 'Rafael Santos'),
            (10, '00011122233', 'larissa.oliveira@example.com', 'Rua dos Girassóis, 707', 'Larissa Oliveira'),
            (11, '11133355566', 'lucas.fernandes@example.com', 'Rua da Esperança, 808', 'Lucas Fernandes'),
            (12, '22244466677', 'amanda.martins@example.com', 'Av. Independência, 909', 'Amanda Martins'),
            (13, '33355577788', 'roberto.silva@example.com', 'Rua das Orquídeas, 111', 'Roberto Silva'),
            (14, '44466688899', 'camila.rodrigues@example.com', 'Av. das Nações, 222', 'Camila Rodrigues'),
            (15, '55577799900', 'vinicius.gomes@example.com', 'Rua das Hortênsias, 333', 'Vinicius Gomes'),
            (16, '66688800011', 'daniela.souza@example.com', 'Av. Paulista, 444', 'Daniela Souza'),
            (17, '77799911122', 'leonardo.almeida@example.com', 'Rua dos Cravos, 555', 'Leonardo Almeida'),
            (18, '88800022233', 'patricia.santos@example.com', 'Av. Amazonas, 666', 'Patricia Santos'),
            (19, '99911133344', 'gabriel.silva@example.com', 'Rua das Rosas, 777', 'Gabriel Silva'),
            (20, '00022244455', 'beatriz.lima@example.com', 'Av. Atlântica, 888', 'Beatriz Lima'),
            (21, '11133377788', 'ricardo.oliveira@example.com', 'Rua das Acácias, 999', 'Ricardo Oliveira'),
            (22, '22244488899', 'carla.moraes@example.com', 'Av. do Contorno, 101', 'Carla Moraes'),
            (23, '33355599900', 'antonio.fernandes@example.com', 'Rua dos Lírios, 202', 'Antonio Fernandes'),
            (24, '44466600011', 'leticia.costa@example.com', 'Av. Central, 303', 'Leticia Costa'),
            (25, '55577711122', 'renato.silva@example.com', 'Rua dos Jacarandás, 404', 'Renato Silva'),
            (26, '66688822233', 'mariana.souza@example.com', 'Av. das Flores, 505', 'Mariana Souza'),
            (27, '77799933344', 'thiago.alves@example.com', 'Rua dos Jasmins, 606', 'Thiago Alves'),
            (28, '88800044455', 'sara.lima@example.com', 'Av. Beira Mar, 707', 'Sara Lima'),
            (29, '99911155566', 'julio.gomes@example.com', 'Rua dos Pinheiros, 808', 'Julio Gomes'),
            (30, '00022266677', 'aline.santos@example.com', 'Av. das Araucárias, 909', 'Aline Santos')"""),

    'ORGANIZACAO': (
        """insert into ORGANIZACAO (Id_org, Tipo_Organizacao, Contato_org, Nome_org) VALUES
            (1, 'Empresa Privada', 'contato@empresa1.com', 'Empresa Alpha'),
            (2, 'ONG', 'contato@ong2.org', 'ONG Beta'),
            (3, 'Instituição Governamental', 'contato@instituicao3.gov', 'Instituição Gamma'),
            (4, 'Empresa Privada', 'contato@empresa4.com', 'Empresa Delta'),
            (5, 'ONG', 'contato@ong5.org', 'ONG Épsilon'),
            (6, 'Empresa Privada', 'contato@empresa10.com', 'Empresa Kappa')"""),
    'PATROCINADOR': (
        """insert into PATROCINADOR (Cod_patrocina, Nome, Email, Valor_do_Patro) VALUES
            (1, 'Empresa Alpha', 'contato@empresa1.com', 1500.00),
            (2, 'ONG Beta', 'contato@ong2.org', 2500.50),
            (3, 'Instituição Gamma', 'contato@instituicao3.gov', 1800.75),
            (4, 'Empresa Delta', 'contato@empresa4.com', 3200.00),
            (5, 'ONG Épsilon', 'contato@ong5.org', 2100.40),
            (6, 'Instituição Zeta', 'contato@instituicao6.gov', 1750.30),
            (7, 'Empresa Eta', 'contato@empresa7.com', 2800.00),
            (8, 'ONG Theta', 'contato@ong8.org', 3300.90),
            (9, 'Instituição Iota', 'contato@instituicao9.gov', 2900.25),
            (10, 'Empresa Kappa', 'contato@empresa10.com', 3100.80),
            (11, 'ONG Lambda', 'contato@ong11.org', 2300.70),
            (12, 'Instituição Mu', 'contato@instituicao12.gov', 2600.60),
            (13, 'Empresa Nu', 'contato@empresa13.com', 3400.20),
            (14, 'ONG Xi', 'contato@ong14.org', 2750.45),
            (15, 'Instituição Omicron', 'contato@instituicao15.gov', 3600.10)"""),

    'PESSOA_FISICA': (
        """insert into PESSOA_FISICA (Sexo, CPF, Cod_patrocina) VALUES
            ('Feminino', '11122233344', 2),
            ('Masculino', '22233344455', 4),
            ('Feminino', '33344455566', 6),
            ('Masculino', '44455566677', 8),
            ('Feminino', '55566677788', 10),
            ('Feminino', '55590677748', 13),
            ('Masculino', '66677788899', 12)"""),
    'PESSOA_JURIDICA': (
        """insert into PESSOA_JURIDICA (Tipo_organizacao, CNPJ, Cod_patrocina) VALUES
            ('Empresa Privada', '11122233344455', 1),
            ('ONG', '22233344455566', 3),
            ('Instituição Governamental', '33344455566677', 7),
            ('Empresa Privada', '44455566677788', 9),
            ('ONG', '55566677788899', 5),
            ('ONG', '55566675409899', 14),
            ('ONG', '55569670783899', 15),
            ('Instituição Governamental', '66677788899900', 11)"""),
    'EVENTO': (
        """insert into EVENTO (Id_evento, Tipo_evento, Nome_evento, Id_local, Id_org) VALUES
            (1, 'Show', 'Concerto de Rock', 1, 1),
            (2, 'Palestra', 'Tecnologias Futuras', 2, 2),
            (3, 'Show', 'Festival de Jazz', 3, 3),
            (4, 'Palestra', 'Inovações em Saúde', 4, 4),
            (5, 'Show', 'Música Clássica', 5, 5),
            (6, 'Palestra', 'Sustentabilidade Ambiental', 6, 6),
            (7, 'Show', 'Evento de Hip Hop', 7, 4),
            (8, 'Palestra', 'Desenvolvimento Pessoal', 8, 1),
            (9, 'Show', 'Festival de Reggae', 9, 6),
            (10, 'Palestra', 'Negócios e Empreendedorismo', 8, 6)"""),
    'ATOR_EVENTO': (
        """insert into ATOR_EVENTO (Id_evento, ID_ator) VALUES
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10),
            (1, 11),
            (2, 12),
            (3, 13),
            (4, 14),
            (5, 15),
            (6, 16),
            (7, 17),
            (8, 18),
            (9, 19),
            (10, 20)"""),
    'PATROCI_EVENTO': (
            """insert into PATROCI_EVENTO (Id_Patro_evento, data_D, Cod_patrocina, Id_evento) VALUES
            (1, '2024-06-01 12:00:00', 1, 1),
            (2, '2024-06-02 15:00:00', 2, 2),
            (3, '2024-06-03 11:00:00', 3, 3),
            (4, '2024-06-04 10:00:00', 4, 4),
            (5, '2024-06-05 14:00:00', 5, 5),
            (6, '2024-06-06 13:00:00', 6, 6),
            (7, '2024-06-07 16:00:00', 7, 7),
            (8, '2024-06-08 09:00:00', 8, 8),
            (9, '2024-06-09 17:00:00', 9, 9),
            (10, '2024-06-10 08:00:00', 10, 10),
            (11, '2024-06-10 08:00:00', 11, 4),
            (12, '2024-06-10 08:00:00', 12, 7),
            (13, '2024-06-10 08:00:00', 13, 6),
            (14, '2024-06-10 08:00:00', 14, 10),
            (15, '2024-06-10 08:00:00', 15, 2),
            (16, '2024-06-10 08:00:00', 10, 1),
            (17, '2024-06-10 08:00:00', 15, 9),
            (18, '2024-06-10 08:00:00', 9, 3),
            (19, '2024-06-10 08:00:00', 1, 2),
            (20, '2024-06-10 08:00:00', 2, 8)"""),
    'INGRESSO': (
        """insert into INGRESSO (Id_ingresso, Preco, Tipo_ingresso, Id_participante, Id_evento) VALUES
            (1, 50.00, 'Vip', 1, 1),
            (2, 30.00, 'Geral', 2, 1),
            (3, 50.00, 'Vip', 3, 1),
            (4, 30.00, 'Geral', 4, 1),
            (5, 50.00, 'Vip', 5, 1),
            (6, 30.00, 'Geral', 6, 1),
            (7, 40.00, 'Vip', 7, 2),
            (8, 25.00, 'Geral', 8, 2),
            (9, 40.00, 'Vip', 9, 2),
            (10, 25.00, 'Geral', 10, 2),
            (11, 60.00, 'Vip', 11, 3),
            (12, 35.00, 'Geral', 12, 3),
            (13, 60.00, 'Vip', 13, 3),
            (14, 35.00, 'Geral', 14, 3),
            (15, 45.00, 'Vip', 15, 4),
            (16, 20.00, 'Geral', 16, 4),
            (17, 45.00, 'Vip', 17, 4),
            (18, 20.00, 'Geral', 18, 4),
            (19, 70.00, 'Vip', 19, 5),
            (20, 40.00, 'Geral', 20, 5),
            (21, 70.00, 'Vip', 21, 5),
            (22, 40.00, 'Geral', 22, 5),
            (23, 55.00, 'Vip', 23, 6),
            (24, 30.00, 'Geral', 24, 6),
            (25, 55.00, 'Vip', 25, 6),
            (26, 30.00, 'Geral', 26, 6),
            (27, 55.00, 'Vip', 27, 7),
            (28, 30.00, 'Geral', 28, 7),
            (29, 55.00, 'Vip', 29, 7),
            (30, 30.00, 'Geral', 30, 7),
            (31, 75.00, 'Vip', 1, 8),
            (32, 40.00, 'Geral', 2, 8),
            (33, 75.00, 'Vip', 3, 8),
            (34, 40.00, 'Geral', 4, 8),
            (35, 55.00, 'Vip', 5, 9),
            (36, 30.00, 'Geral', 6, 9),
            (37, 55.00, 'Vip', 7, 9),
            (38, 30.00, 'Geral', 8, 9),
            (39, 65.00, 'Vip', 9, 10),
            (40, 35.00, 'Geral', 10, 10),
            (41, 65.00, 'Vip', 11, 10),
            (42, 35.00, 'Geral', 12, 10),
            (43, 65.00, 'Vip', 20, 10),
            (44, 35.00, 'Geral', 30, 10),
            (45, 65.00, 'Vip', 10, 10),
            (46, 35.00, 'Geral', 12, 10),
            (47, 65.00, 'Vip', 9, 3),
            (48, 35.00, 'Geral', 29, 7),
            (49, 65.00, 'Vip', 18, 4),
            (50, 35.00, 'Geral', 19, 8),
            (51, 65.00, 'Vip', 12, 3)"""),
    'AVALIACAO': (
        """insert into AVALIACAO (Id_Avaliacao, Data_avaliacao, Comentario, Nota, Id_participante, Id_evento) VALUES
            (1, '2024-06-01 10:00:00', 'Ótimo evento! Muito organizado.', 5, 1, 1),
            (2, '2024-06-01 11:00:00', 'Excelentes palestras. Aprendi muito.', 4, 2, 1),
            (3, '2024-06-01 12:00:00', 'Localização excelente.', 5, 3, 1),
            (4, '2024-06-01 13:00:00', 'Boa infraestrutura.', 4, 18, 4),
            (5, '2024-06-01 14:00:00', 'Achei os ingressos um pouco caros.', 3, 19, 8),
            (6, '2024-06-02 10:00:00', 'Show incrível! Adorei.', 5, 6, 1),
            (7, '2024-06-02 11:00:00', 'Evento muito bem organizado.', 4, 12, 10),
            (8, '2024-06-02 12:00:00', 'Poderia ter mais opções de alimentação.', 3, 4, 8),
            (9, '2024-06-02 13:00:00', 'Palestrantes muito qualificados.', 5, 10, 10),
            (10, '2024-06-02 14:00:00', 'Boa variedade de temas abordados.', 4, 7, 9)"""),
    'VINCULADO': (
        """insert into VINCULADO (Id_colaborador, Id_evento) VALUES
            (1, 1),
            (1, 2),
            (1, 3),
            (2, 2),
            (2, 3),
            (2, 4),
            (3, 4),
            (3, 5),
            (3, 6),
            (4, 5),
            (4, 6),
            (4, 7),
            (5, 7),
            (5, 8),
            (5, 9),
            (6, 8),
            (6, 9),
            (6, 10),
            (7, 9),
            (7, 10),
            (8, 10),
            (9, 1),
            (9, 2),
            (10,3),
            (10, 10)"""),
    'AGENDA': (
        """insert into AGENDA (Id_agenda, Data_inicio, Data_fim, Id_evento) VALUES
            (1, '2024-06-01 09:00:00', '2024-06-01 18:00:00', 1),
            (2, '2024-06-02 10:00:00', '2024-06-02 20:00:00', 2),
            (3, '2024-06-03 11:00:00', '2024-06-03 22:00:00', 3),
            (4, '2024-06-04 12:00:00', '2024-06-04 21:00:00', 4),
            (5, '2024-06-05 13:00:00', '2024-06-05 19:00:00', 5),
            (6, '2024-06-06 09:00:00', '2024-06-06 18:00:00', 6),
            (7, '2024-06-07 10:00:00', '2024-06-07 20:00:00', 7),
            (8, '2024-06-08 11:00:00', '2024-06-08 22:00:00', 8),
            (9, '2024-06-09 12:00:00', '2024-06-09 21:00:00', 9),
            (10, '2024-06-10 13:00:00', '2024-06-10 19:00:00', 10) """),
    'SESSAO': (
        """insert into SESSAO (Id_sessao, Hora_inicio, Hora_fim, Nome_sessao, Data, Id_agenda) VALUES
            (1, '2024-06-01 10:00:00', '2024-06-01 12:00:00', 'Show Matinal', '2024-06-01', 1),
            (2, '2024-06-01 14:00:00', '2024-06-01 16:00:00', 'Show Vespertino', '2024-06-01', 1),
            (3, '2024-06-02 11:00:00', '2024-06-02 13:00:00', 'Show de Abertura', '2024-06-02', 3),
            (4, '2024-06-02 15:00:00', '2024-06-02 17:00:00', 'Show Principal', '2024-06-02', 3),
            (5, '2024-06-03 12:00:00', '2024-06-03 14:00:00', 'Show da Tarde', '2024-06-03', 5),
            (6, '2024-06-03 16:00:00', '2024-06-03 18:00:00', 'Show Noturno', '2024-06-03', 5),
            (7, '2024-06-04 13:00:00', '2024-06-04 15:00:00', 'Show de Encerramento', '2024-06-04', 7),
            (8, '2024-06-04 17:00:00', '2024-06-04 19:00:00', 'Show Especial', '2024-06-04', 7),
            (9, '2024-06-05 14:00:00', '2024-06-05 16:00:00', 'Show Final', '2024-06-05', 9),
            (10, '2024-06-05 18:00:00', '2024-06-05 20:00:00', 'Show de Despedida', '2024-06-05', 9),
            (11, '2024-06-06 10:00:00', '2024-06-06 12:00:00', 'Palestra Matinal', '2024-06-06', 2),
            (12, '2024-06-06 14:00:00', '2024-06-06 16:00:00', 'Palestra Vespertina', '2024-06-06', 2),
            (13, '2024-06-07 11:00:00', '2024-06-07 13:00:00', 'Palestra de Abertura', '2024-06-07', 4),
            (14, '2024-06-07 15:00:00', '2024-06-07 17:00:00', 'Palestra Principal', '2024-06-07', 4),
            (15, '2024-06-08 12:00:00', '2024-06-08 14:00:00', 'Palestra da Tarde', '2024-06-08', 6),
            (16, '2024-06-08 16:00:00', '2024-06-08 18:00:00', 'Palestra Noturna', '2024-06-08', 6),
            (17, '2024-06-09 13:00:00', '2024-06-09 15:00:00', 'Palestra de Encerramento', '2024-06-09', 8),
            (18, '2024-06-09 17:00:00', '2024-06-09 19:00:00', 'Palestra Especial', '2024-06-09', 8),
            (19, '2024-06-10 14:00:00', '2024-06-10 16:00:00', 'Palestra Final', '2024-06-10', 10),
            (20, '2024-06-10 18:00:00', '2024-06-10 20:00:00', 'Palestra de Despedida', '2024-06-10', 10)"""),
}
# Valores para deletar as tabelas
drop = { 'SESSAO': (
    "drop table SESSAO"),
    'AGENDA': (
        "drop table AGENDA"),
    'VINCULADO': (
        "drop table VINCULADO"),
    'AVALIACAO': (
            "drop table AVALIACAO"),
    'INGRESSO': (
            "drop table INGRESSO"),
    'PATROCI_EVENTO': (
            "drop table PATROCI_EVENTO"),
    'ATOR_EVENTO': (
            "drop table  ATOR_EVENTO"),
    'EVENTO': (
            "drop table EVENTO"),
    'PESSOA_FISICA': (
            "drop table PESSOA_FISICA"),
    'PESSOA_JURIDICA': (
            "drop table PESSOA_JURIDICA"),
    'PATROCINADOR': (
            "drop table PATROCINADOR"),
    'ORGANIZACAO': (
            "drop table ORGANIZACAO"),
    'PARTICIPANTE': (
            "drop table PARTICIPANTE"),
    'COLABORADOR': (
            "drop table COLABORADOR"),
    'ATOR': (
            "drop table ATOR"),
    'LOCAL': (
            "drop table LOCAL"),
}
# Valores para teste de update
update = {'ATOR': (
    """update ATOR
        SET Nome_ator = 'Sarkodie',
            Contato_email = 'sarkodie@gmail.com',
            Descricao = 'RAP' 
        WHERE Id_ator = 3 """),
    'PARTICIPANTE': (
        """update PARTICIPANTE
            SET CPF = '287087564',
                Contato = 'imelda@gmail.com',
                Nome_participante = 'Imelda Da Costa' 
            WHERE Id_participante = 7 """),
    'LOCAL': (
        """update LOCAL
            SET Capacidade = '80',
                Nome_local = 'Teatro UFSC'
            WHERE Id_local = 3 """),
    'AVALIACAO': (
        """update AVALIACAO
            SET Comentario = 'Waaawwwww',
                Nota = '5' 
            WHERE Id_Avaliacao = 2 """),
}

# Valores para teste de delete
delete = { 'VINCULO': (
    """delete from VINCULADO
        where Id_colaborador in ('1' , '3') """),
    'SESSAO': (
        """delete from SESSAO
        where Id_sessao = 2 or Id_sessao = 3 """),
    'PATROCI_EVENTO': (
        """delete from PATROCI_EVENTO
        where Id_evento = 7 """),
}

path_env = '.env'
load_dotenv(path_env)


# Beginin of funtions 
def connect_resgatocao():
    cnx = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "bd_evento"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=(3306),
    )

    if cnx.is_connected():
        db_info = cnx.get_server_info()
        print("Conectado ao servidor MySQL versão ", db_info)
        cursor = cnx.cursor()
        cursor.execute("select database();")
        linha = cursor.fetchone()
        print("Conectado ao banco de dados ", linha)
        cursor.close()
    return cnx

def drop_all_tables(connect):
    print("\n---DROP DB---")
    # Esvazia o Banco de Dados
    cursor = connect.cursor()
    for drop_name in drop:
        drop_description = drop[drop_name]
        try:
            print("Deletando {}: ".format(drop_name), end='')
            cursor.execute(drop_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()

def create_all_tables(connect):
    print("\n---CREATE ALL TABLES---")
    # Criação das tabelas 
    cursor = connect.cursor()
    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Criando tabela {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Tabela já existe.")
            else:
                print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()

def show_table(connect):
    print("\n---SELECIONAR TABELA---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        print("Nome: {}".format(table_name))
    try:
        name = input(str("\nDigite o nome da tabela que deseja consultar. ")).upper()
        # SEGURANÇA: valida o nome contra a whitelist de tabelas conhecidas
        # (identificadores de tabela/coluna não podem ser parametrizados via
        # placeholders do driver, então a validação por whitelist é a defesa correta aqui)
        if name not in tables:
            print("Tabela inválida.")
            cursor.close()
            return
        select = "select * from `" + name + "`"
        cursor.execute(select)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("TABELA {}".format(name))
        myresult = cursor.fetchall()
        for x in myresult:
            print(x)
    cursor.close()

def update_value(connect):
    print("\n---SELECIONAR TABELA PARA ATUALIZAÇÃO---")
    # Criação das tabelas
    cursor = connect.cursor()
    for table_name in tables:
        print("Nome: {}".format(table_name))
    try:
        name = input(str("\nDigite o nome da tabela que deseja consultar. ")).upper()
        # SEGURANÇA: valida o nome da tabela contra a whitelist de tabelas conhecidas
        if name not in tables:
            print("Tabela inválida.")
            cursor.close()
            return
        for table_name in tables:
            table_description = tables[table_name]
            if table_name == name:
                print("Para criar a tabela: {}, foi utilizado o seguinte código {}".format(table_name,
                                                                                           table_description))
        atributo = input("Digite o atributo a ser alterado: ")
        valor = input("Digite o valor a ser atribuido: ")
        codigo_f = input("Digite a variavel primaria: ")
        codigo = input("Digite o codigo numerico: ")

        # SEGURANÇA: nomes de coluna não podem ser parametrizados pelo driver
        # (placeholders só valem para valores), então validamos com uma whitelist
        # de caracteres (somente letras, números e underscore) antes de montar a query.
        identifier_pattern = re.compile(r'^[A-Za-z0-9_]+$')
        if not identifier_pattern.match(atributo) or not identifier_pattern.match(codigo_f):
            print("Nome de atributo/coluna inválido.")
            cursor.close()
            return

        # Os VALORES (valor, codigo), esses sim, são parametrizados via %s —
        # isso é o que efetivamente elimina o risco de SQL Injection nos dados.
        sql = "UPDATE `{}` SET `{}` = %s WHERE `{}` = %s".format(name, atributo, codigo_f)
        cursor.execute(sql, (valor, codigo))
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("Atributo atualizado")
    connect.commit()
    cursor.close()

def insert_test(connect):
    print("\n---INSERT TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for insert_name in inserts:
        insert_description = inserts[insert_name]
        try:
            print("Inserindo valores para {}: ".format(insert_name), end='')
            cursor.execute(insert_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()

def update_test(connect):
    print("\n---UPDATE TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for update_name in update:
        update_description = update[update_name]
        try:
            print("Teste de atualização de valores para {}: ".format(update_name), end='')
            cursor.execute(update_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()

def delete_test(connect):
    print("\n---DELETE TEST---")
    # Inesrsão dos valores nas tabelas
    cursor = connect.cursor()
    for delete_name in delete:
        delete_description = delete[delete_name]
        try:
            print("Teste de atualização de valores para {}: ".format(delete_name), end='')
            cursor.execute(delete_description)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print("OK")
    connect.commit()
    cursor.close()

def consulta1(connect):
    select_query = """
    SELECT o.nome_org, e.Nome_evento,e.tipo_evento,  SUM(i.Preco) AS Receita_Total
        FROM EVENTO as e join organizacao as o on o.id_org = e.id_org
                 JOIN INGRESSO as i ON e.Id_evento = i.Id_evento
                 where e.tipo_evento = 'show'
        GROUP BY e.Nome_evento, o.nome_org, e.tipo_evento
    """
    print("\nPrimeira Consulta: Mostra o faturamento total das organizações que organizaram eventos do tipo 'show'..")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)

def consulta2(connect):
    select_query = """
    select o.nome_org, sum(pa.valor_do_patro)
    from organizacao as o join evento as e on o.id_org = e.id_org
            join patroci_evento as pe on e.id_evento = pe.id_evento
            join patrocinador as pa on pe.cod_patrocina = pa.cod_patrocina
            group by o.nome_org 
    """
    print("\nSegunda Consulta: O resultado dessa consulta será uma lista de "
          "organizações com o total de patrocínios recebidos para todos os eventos que organizaram. ")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)

def consulta3(connect):
    select_query = """
    select e.nome_evento, count(i.id_ingresso) as Total_ingrgresso_evento_com_comnetario
        from ingresso as i join evento as e on i.id_evento = e.id_evento
         inner join  avaliacao as a on a.id_evento = e.id_evento 
            group by e.nome_evento
    """
    print("\nTerceira Consulta:  apresenta o número total de ingressos vendidos para eventos"
          " que receberam pelo menos uma avaliação.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)

def consulta_extra(connect):
    select_query = """
        SELECT 
            e.Nome_evento, at.nome_ator,
            SUM(pa.Valor_do_Patro) AS Total_valor_patrocinio, 
            SUM(i.Preco) AS Total_valor_ingressos
        FROM EVENTO as e JOIN PATROCI_EVENTO as pe ON e.Id_evento = pe.Id_evento
            JOIN INGRESSO as i ON e.Id_evento = i.Id_evento
            inner join patrocinador as pa on  pe.cod_patrocina = pa.cod_patrocina
            join ator_evento as ae on e.id_evento = ae.id_evento
            join ator as at on ae.ID_ator = at.id_ator
        WHERE 
            at.Nome_ator in ('Wizkid', 'Burna boy', 'Asake')
        GROUP BY e.Nome_evento, at.nome_ator
    """
    print("\nConsulta Extra: A consulta vai apresentar nome do evento, total do valor recebido"
          "do patrocinio, total de vendas de ingresso e ambas esses resultados vai ser no"
          "critério de 3 artistas Wizkid, Burna Boy e Asake.")
    cursor = connect.cursor()
    cursor.execute(select_query)
    myresult = cursor.fetchall()
    for x in myresult:
        print(x)

def exit_db(connect):
    print("\n---EXIT DB---")
    connect.close()
    print("Conexão ao MySQL foi encerrada")

def crud_resgatocao(connect):
    drop_all_tables(connect)
    create_all_tables(connect)
    insert_test(connect)

    print("\n---CONSULTAS BEFORE---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)
    consulta_extra(connect)

    update_test(connect)
    delete_test(connect)

    print("\n---CONSULTAS AFTER---")
    consulta1(connect)
    consulta2(connect)
    consulta3(connect)
    consulta_extra(connect)

# Main
try:
    # Estabelece Conexão com o DB
    con = connect_resgatocao()

    power_up = 1
    while power_up == 1:
        interface = """\n       ---MENU---
        1.  CRUD RESGATOCAO
        2.  TEST - Create all tables
        3.  TEST - Insert all values
        4.  TEST - Update
        5.  TEST - Delete
        6.  CONSULTA 01
        7.  CONSULTA 02
        8.  CONSULTA 03
        9.  CONSULTA EXTRA
        10. Show Table
        11. Update Value
        12. CLEAR ALL TABLES BD_EVENTO
        0.  Disconnect DB\n """
        print(interface)

        choice = int(input("Opção: "))
        if choice < 0 or choice > 12:
            print("Erro tente novamente")
            choice = int(input())

        if choice == 0:
            if con.is_connected():
                exit_db(con)
                print("Muito obrigado.")
                break
            else:
                break

        if choice == 1:
            crud_resgatocao(con)

        if choice == 2:
            create_all_tables(con)

        if choice == 3:
            insert_test(con)

        if choice == 4:
            update_test(con)

        if choice == 5:
            delete_test(con)

        if choice == 6:
            consulta1(con)

        if choice == 7:
            consulta2(con)

        if choice == 8:
            consulta3(con)

        if choice == 9:
            consulta_extra(con)

        if choice == 10:
            show_table(con)

        if choice == 11:
            update_value(con)

        if choice == 12:
            drop_all_tables(con)

except mysql.connector.Error as err:
    print("Erro na conexão com o sqlite", err.msg)
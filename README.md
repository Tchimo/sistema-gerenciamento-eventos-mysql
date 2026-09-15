# Sistema de Gerenciamento de Eventos — Banco de Dados

Projeto de modelagem e implementação de banco de dados relacional para um sistema de gerenciamento de eventos (shows, palestras, conferências), desenvolvido para a disciplina de Banco de Dados I (UFSC — Campus Araranguá).

O sistema cobre o ciclo completo: modelagem conceitual → modelo lógico → script físico SQL → implementação em Python (CRUD + consultas de negócio) → visualização dos resultados.

## O problema

Organizações que promovem eventos com múltiplas sessões, patrocinadores, ingressos e avaliações precisam de uma estrutura de dados que suporte relacionamentos complexos (um evento pode ter vários patrocinadores, vários colaboradores, uma agenda com múltiplas sessões) sem duplicar ou perder informação.

## Modelo Conceitual

![Modelo Conceitual](visuals/modelo_conceitual.png)

Principais entidades: Evento, Organização, Local, Agenda/Sessão, Participante, Ingresso, Colaborador, Ator (palestrante/artista), Patrocinador (com especialização em Pessoa Física / Pessoa Jurídica) e Avaliação.

## Modelo Lógico

![Modelo Lógico](visuals/modelo_logico.png)

Conversão do modelo conceitual para o modelo relacional, com chaves primárias, estrangeiras e cardinalidades definidas — desenvolvido com a ferramenta [brModelo](https://sourceforge.net/projects/brmodeloii/).

## Estrutura do projeto

```
├── Script.sql          # Script físico do modelo (DDL)
├── main.py             # Implementação em Python: CRUD, testes e consultas
├── requirements.txt    # Dependências Python
├── .env.example         # Modelo de variáveis de ambiente (copie para .env)
└── visuals/
    ├── modelo_conceitual.png
    └── modelo_logico.png
```

## Como rodar

1. Clone este repositório
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Copie `.env.example` para `.env` e preencha com suas credenciais do MySQL:
   ```
   cp .env.example .env
   ```
4. Crie o banco `bd_evento` no MySQL (vazio — as tabelas são criadas pelo próprio script)
5. Execute:
   ```
   python main.py
   ```
6. Use o menu interativo para criar as tabelas, popular com dados de teste e rodar as consultas

## Consultas de negócio implementadas

| # | Consulta |
|---|---|
| 1 | Faturamento total das organizações que promoveram eventos do tipo "show" |
| 2 | Total de patrocínio recebido por organização, somando todos os eventos que organizou |
| 3 | Total de ingressos vendidos para eventos que receberam pelo menos uma avaliação |
| Extra | Valor de patrocínio e vendas de ingresso para eventos com artistas específicos (Wizkid, Burna Boy, Asake) |

Cada consulta usa `JOIN`/`GROUP BY`/funções de agregação sobre o modelo relacional completo. Os resultados foram visualizados em gráficos no Excel (ver relatório completo).

## Nota sobre segurança — correções aplicadas

Na primeira versão do projeto, duas funções do `main.py` (`show_table` e `update_value`) construíam queries SQL concatenando diretamente o input do usuário na string, o que é uma vulnerabilidade clássica de **SQL Injection**. Corrigi isso em duas frentes:

- **Nomes de tabela**: validados contra a whitelist de tabelas conhecidas (`tables.keys()`) antes de entrar na query
- **Nomes de coluna** (que, como identificadores, não podem ser parametrizados pelo driver): validados com uma regex restrita a `[A-Za-z0-9_]`
- **Valores** (o dado em si, que pode e deve ser parametrizado): passados via placeholders (`%s`) do `mysql-connector-python`, não mais concatenados como string

Também movi as credenciais do banco (antes hardcoded como `user='root', password='master'`) para variáveis de ambiente via `python-dotenv`, seguindo o arquivo `.env.example` incluído no repositório.

## Correção de modelagem

O diagrama do modelo lógico (brModelo) já definia `Cod_patrocina` como chave primária nas tabelas de especialização `Pessoa_Física` e `Pessoa_Jurídica` (padrão table-per-subclass para a generalização "Patrocinador"), mas essa PK não tinha sido replicada nos scripts SQL da primeira versão. Corrigido tanto no `Script.sql` quanto no `main.py`, junto com o tipo de `CPF`/`CNPJ` (de `integer` para `varchar`, evitando perda de zeros à esquerda).

## Ferramentas utilizadas

- **MySQL** — banco de dados relacional
- **Python** — `mysql-connector-python`, `python-dotenv`
- **brModelo** — modelagem conceitual e lógica
- **Excel** — visualização dos resultados das consultas

---

📎 Trabalho final da disciplina de Banco de Dados I — UFSC, Campus Araranguá (2024)
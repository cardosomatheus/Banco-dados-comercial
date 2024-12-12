﻿
                                -- AINDA EM DESENVOLVIMENTO

/*
cliente: id, nome, documento
produto: id, nome, nome_amigavel,  preco_usd, id_marca_produto
catergoria_produto: id, nome
marca_produto: id, nome
cambio_moeda:  id, moeda, pais, cambio_para_usd

COMPRA_CLIENTE: id, id_cliente, timestamp, total_compra
compra_produto: id,id_compra_cliente, id_produto, quantidade, preco_unitario_atual, id_cammbio_moeda

regiao: latitude, longitude, bairro, id_cidade
cidade: id, nome, sigla, id_estado
estado: id, nome, sigla, id_pais
pais: id, nome, sigla, continente

feriado : id, nome, id_pais

OBS: Criar tabelas de historico.
OBS: Criar trigger para calcular o total da compra sempre que houver alterações na SQ_COMPRA_PRODUTO
*/

-- modelo logico da fonte.
/******************************************************************************************************************************/

-- Tabela: TB_CLIENTE
CREATE SEQUENCE SQ_CLIENTE INCREMENT 1 START 1 NOCYCLE;

CREATE TABLE IF NOT EXISTS TB_CLIENTE (
    ID BIGINT NOT NULL NEXTVAL('SQ_CLIENTE'),
    NOME VARCHAR(255) NOT NULL,
    DOCUMENTO VARCHAR(100),
    CONSTRAINT PKEY_CLIENTE PRIMARY KEY(ID)
);


-- TABELA: TB_PRODUTO
CREATE SEQUENCE SQ_PRODUTO INCREMENT 1 START 1 NOCYCLE;

CREATE TABLE IF NOT EXISTS TB_PRODUTO (
    ID BIGINT NOT NULL DEFAULT NEXTVAL('SQ_PRODUTO'),
    NOME VARCHAR(4000) NOT NULL,
    NOME_COMERCIAL VARCHAR(250),
    ID_MARCA_PRODUTO BIGINT NOT NULL,
    ID_CATEGORIA_PRODUTO BIGINT NOT NULL,
    CONSTRAINT PKEY_PRODUTO PRIMARY KEY (ID),
    CONSTRAINT FKEY_MARCA_PRODUTO_PRODUTO FOREIGN KEY(ID_MARCA_PRODUTO) REFERENCES TB_MARCA_PRODUTO(ID),
    CONSTRAINT FKEY_CATEGORIA_PRODUTO_PRODUTO FOREIGN KEY(ID_CATEGORIA_PRODUTO) REFERENCES TB_CATEGORIA_PRODUTO(ID)
);


-- TABELA: TB_MARCA_PRODUTO
CREATE SEQUENCE SQ_MARCA_PRODUTO INCREMENT 1 START 1 NOCYCLE;

CREATE TABLE IF NOT EXISTS TB_MARCA_PRODUTO (
    ID BIGINT NOT NULL DEFAULT NEXTVAL('SQ_MARCA_PRODUTO'),
    NOME VARCHAR(4000) NOT NULL,
    CONSTRAINT PKEY_MARCA_PRODUTO PRIMARY KEY (ID)
);


-- TABELA: TB_CATEGORIA_PRODUTO
CREATE SEQUENCE SQ_CATEGORIA_PRODUTO INCREMENT 1 START 1 NOCYCLE;

CREATE TABLE IF NOT EXISTS TB_CATEGORIA_PRODUTO (
    ID BIGINT NOT NULL DEFAULT NEXTVAL('SQ_CATEGORIA_PRODUTO'),
    NOME VARCHAR(4000) NOT NULL,
    CONSTRAINT PKEY_CATEGORIA_PRODUTO PRIMARY KEY (ID)
);


-- TABELA: TB_PEDIDO
CREATE SEQUENCE SQ_PEDIDO INCREMENT 1 START 1 NOCYCLE;

CREATE TABLE IF NOT EXISTS TB_PEDIDO (
    ID BIGINT NOT NULL DEFAULT NEXTVAL('SQ_PEDIDO'),
    ID_CLIENTE BIGINT NOT NULL,
    TOTAL_COMPRA BIGINT,
    DATA_COMPRA TIMESTAMP, 
    CONSTRAINT PKEY_PEDIDO PRIMARY KEY (ID),
    CONSTRAINT FKEY_PEDIDO_CLIENTE FOREIGN KEY(ID_CLIENTE) REFERENCES TB_CLIENTE(ID)        
);


-- TABELA: TB_ITEM_PEDIDO
CREATE SEQUENCE SQ_ITEM_PEDIDO  INCREMENT 1 START 1 NOCYCLE;

CREATE TABLE IF NOT EXISTS TB_ITEM_PEDIDO (
    ID BIGINT NOT NULL DEFAULT NEXTVAL('SQ_ITEM_PEDIDO'),
    ID_PEDIDO BIGINT NOT NULL,
    QUANTIDADE BIGINT,
    PRECO_ATUAL_USD NUMERIC(15, 2),
    CONSTRAINT PKEY_ITEM_PEDIDO PRIMARY KEY (ID),
    CONSTRAINT FKEY_ITEM_PEDIDO_PEDIDO FOREIGN KEY(ID_PEDIDO) REFERENCES TB_PEDIDO(ID)
);


-- TABELA: TB_PAIS
CREATE SEQUENCE SQ_PAIS INCREMENT 1 START 1 NOCYCLE;

CREATE TABLE IF NOT EXISTS TB_PAIS (
    ID BIGINT NOT NULL NEXTVAL('SQ_PAIS'),
    NOME VARCHAR(100),
    SIGLA VARCHAR(2),
    CONTINENTE VARCHAR(50),
    CONSTRAINT PKEY_PAIS PRIMARY KEY (ID)
);


-- TABELA: TB_ESTADO
CREATE SEQUENCE SQ_ESTADO INCREMENT 1 START 1 NOCYCLE;

CREATE TABLE IF NOT EXISTS TB_ESTADO (
    ID BIGINT NOT NULL DEFAULT NEXTVAL('SQ_ESTADO'),
    NOME VARCHAR(100),
    SIGLA VARCHAR(5), 
    ID_PAIS BIGINT,
    CONSTRAINT PKEY_ESTADO PRIMARY KEY (ID),
    CONSTRAINT FKEY_ESTADO_PAIS FOREIGN KEY(ID_PAIS) REFERENCES TB_PAIS(ID)  
);

-- TABELA: TB_CIDADE
CREATE SEQUENCE SQ_CIDADE INCREMENT 1 START 1 NOCYCLE;

CREATE TABLE IF NOT EXISTS TB_CIDADE (
    ID BIGINT NOT NULL NEXTVAL('SQ_CIDADE'),
    NOME VARCHAR(100),
    SIGLA VARCHAR(5),
    ID_ESTADO BIGINT,
    CONSTRAINT PKEY_CIDADE PRIMARY KEY (ID),
    CONSTRAINT FKEY_CIDADE_ESTADO FOREIGN KEY(ID_ESTADO) REFERENCES TB_ESTADO(ID)    
);


-- TABELA: TB_REGIAO
CREATE SEQUENCE SQ_REGIAO INCREMENT 1 START 1 NOCYCLE;

CREATE TABLE IF NOT EXISTS TB_REGIAO (
    ID BIGINT NOT NULL DEFAULT NEXTVAL('SQ_REGIAO'),
    GEOLOCALIZACAO GEOMETRY,
    BAIRRO VARCHAR(100),
    ID_CIDADE BIGINT,
    CONSTRAINT PKEY_REGIAO PRIMARY KEY (ID),
    CONSTRAINT FKEY_REGIAO_CIDADE FOREIGN KEY(ID_CIDADE) REFERENCES TB_CIDADE(ID)    
);
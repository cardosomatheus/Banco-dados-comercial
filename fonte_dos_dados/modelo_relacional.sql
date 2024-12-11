
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
*/

-- modelo logico da fonte.
CREATE TABLE IF NOT EXISTS TB_CLIENTE (
    ID BIGINT NOT NULL,
    NOME VARCHAR(4000) NOT NULL,
    DOCUMENTO VARCHAR(400)
);


CREATE TABLE IF NOT EXISTS TB_PRODUTO (
    ID BIGINT NOT NULL,
    NOME VARCHAR(4000) NOT NULL,
    NOME_COMERCIAL VARCHAR(250),
    ID_MARCA_PRODUTO  BIGINT NOT NULL,
    ID_CATEGORIA_PRODUTO BIGINT NOT NULL
);



CREATE TABLE IF NOT EXISTS TB_MARCA_PRODUTO (
    ID BIGINT NOT NULL,
    NOME VARCHAR(4000) NOT NULL
);

CREATE TABLE IF NOT EXISTS TB_CATEGORIA_PRODUTO (
    ID BIGINT NOT NULL,
    NOME VARCHAR(4000) NOT NULL
);

CREATE TABLE IF NOT EXISTS TB_COMPRA_CLIENTE (
    ID BIGINT NOT NULL,
    ID_CLIENTE BIGINT NOT NULL,
    TOTAL_COMPRA BIGINT,
    DATA_COMPRA DATETIME
);


CREATE TABLE IF NOT EXISTS TB_COMPRA_PRODUTO (
    ID BIGINT NOT NULL,
    ID_COMPRA_CLIENTE BIGINT NOT NULL,
    QUANTIDADE BIGINT,
    PRECO_ATUAL_USD BIGINT,
    ID_CAMMBIO_MOEDA BIGINT NOT NULL
);


CREATE TABLE IF NOT EXISTS TB_PAIS (
    ID BIGINT NOT NULL,
    NOME VARCHAR(100),
    SIGLA VARCHAR(2),
    CONTINENTE VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS TB_ESTADO (
    ID BIGINT NOT NULL,
    NOME VARCHAR(100),
    SIGLA VARCHAR(2),
    ID_PAIS BIGINT
);


CREATE TABLE IF NOT EXISTS TB_ESTADO (
    ID BIGINT NOT NULL,
    NOME VARCHAR(100),
    SIGLA VARCHAR(5),
    ID_ESTAD BIGINT
);


CREATE TABLE IF NOT EXISTS TB_REGIAO (
    ID BIGINT NOT NULL,
    GEOLOCALIZACAO GEOMETRY,
    BAIRRO VARCHAR(300),
    ID_CIDADE BIGINT
);


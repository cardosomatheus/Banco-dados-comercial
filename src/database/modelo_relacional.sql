
                                -- AINDA EM DESENVOLVIMENTO

-- modelo logico da fonte.
/******************************************************************************************************************************/

-- TABELA: TB_PAIS
CREATE SEQUENCE IF NOT EXISTS SQ_PAIS INCREMENT 1 START 1 ;

CREATE TABLE IF NOT EXISTS TB_PAIS (
    ID BIGINT NOT NULL default NEXTVAL('SQ_PAIS'),
    NOME VARCHAR(100),
    SIGLA VARCHAR(2),
    CAPITAL VARCHAR(50),
    CONTINENTE VARCHAR(50),
    CONSTRAINT PKEY_PAIS PRIMARY KEY (ID)
);

-- TABELA: TB_ESTADO
CREATE SEQUENCE IF NOT EXISTS SQ_ESTADO INCREMENT 1 START 1 ;

CREATE TABLE IF NOT EXISTS TB_ESTADO (
    ID BIGINT NOT NULL DEFAULT NEXTVAL('SQ_ESTADO'),
    NOME VARCHAR(100),
    SIGLA VARCHAR(5), 
    CAPITAL varchar(300),
    ID_PAIS BIGINT,
    CONSTRAINT PKEY_ESTADO PRIMARY KEY (ID),
    CONSTRAINT FKEY_ESTADO_PAIS FOREIGN KEY(ID_PAIS) REFERENCES TB_PAIS(ID)  
);

-- TABELA: TB_CIDADE
CREATE SEQUENCE IF NOT EXISTS SQ_CIDADE INCREMENT 1 START 1 ;

CREATE TABLE IF NOT EXISTS TB_CIDADE (
    ID BIGINT NOT null DEFAULT NEXTVAL('SQ_CIDADE'),
    NOME VARCHAR(100),
    SIGLA VARCHAR(5),
    ID_ESTADO BIGINT,
    ID_IBGE BIGINT,
    CONSTRAINT PKEY_CIDADE PRIMARY KEY (ID),
    CONSTRAINT FKEY_CIDADE_ESTADO FOREIGN KEY(ID_ESTADO) REFERENCES TB_ESTADO(ID)    
);

-- TABELA: TB_REGIAO
CREATE SEQUENCE IF NOT EXISTS SQ_REGIAO INCREMENT 1 START 1 ;

CREATE TABLE IF NOT EXISTS TB_REGIAO (
    ID BIGINT NOT NULL DEFAULT NEXTVAL('SQ_REGIAO'),
    LATITUDE VARCHAR(100),
    LONGITUDE VARCHAR(100),
    BAIRRO VARCHAR(100),
    ID_CIDADE BIGINT,
    CONSTRAINT PKEY_REGIAO PRIMARY KEY (ID),
    CONSTRAINT FKEY_REGIAO_CIDADE FOREIGN KEY(ID_CIDADE) REFERENCES TB_CIDADE(ID)    
);


-- Tabela: TB_CLIENTE
CREATE SEQUENCE IF NOT EXISTS SQ_CLIENTE INCREMENT 1 START 1;

CREATE TABLE IF NOT EXISTS TB_CLIENTE (
    ID BIGINT NOT null default NEXTVAL('SQ_CLIENTE'),
    NOME VARCHAR(255) NOT NULL,
    DOCUMENTO VARCHAR(100),
    ID_REGIAO BIGINT,
    CONSTRAINT PKEY_CLIENTE PRIMARY KEY(ID),
    CONSTRAINT FKEY_CLIENTE_REGIAO FOREIGN KEY(ID_REGIAO) REFERENCES TB_REGIAO(ID)  
);

-- TABELA: TB_MARCA_PRODUTO
CREATE SEQUENCE IF NOT EXISTS SQ_MARCA_PRODUTO INCREMENT 1 START 1 ;

CREATE TABLE IF NOT EXISTS TB_MARCA_PRODUTO (
    ID BIGINT NOT NULL DEFAULT NEXTVAL('SQ_MARCA_PRODUTO'),
    NOME VARCHAR(4000) NOT NULL,
    CONSTRAINT PKEY_MARCA_PRODUTO PRIMARY KEY (ID)
);

-- TABELA: TB_CATEGORIA_PRODUTO
CREATE SEQUENCE IF NOT EXISTS SQ_CATEGORIA_PRODUTO INCREMENT 1 START 1 ;

CREATE TABLE IF NOT EXISTS TB_CATEGORIA_PRODUTO (
    ID BIGINT NOT NULL DEFAULT NEXTVAL('SQ_CATEGORIA_PRODUTO'),
    NOME VARCHAR(4000) NOT NULL,
    CONSTRAINT PKEY_CATEGORIA_PRODUTO PRIMARY KEY (ID)
);

-- TABELA: TB_PRODUTO
CREATE SEQUENCE IF NOT EXISTS SQ_PRODUTO INCREMENT 1 START 1 ;

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


-- TABELA: TB_PEDIDO
CREATE SEQUENCE IF NOT EXISTS SQ_PEDIDO INCREMENT 1 START 1 ;

CREATE TABLE IF NOT EXISTS TB_PEDIDO (
    ID BIGINT NOT NULL DEFAULT NEXTVAL('SQ_PEDIDO'),
    ID_CLIENTE BIGINT NOT NULL,
    TOTAL_COMPRA BIGINT,
    DATA_COMPRA TIMESTAMP, 
    CONSTRAINT PKEY_PEDIDO PRIMARY KEY (ID),
    CONSTRAINT FKEY_PEDIDO_CLIENTE FOREIGN KEY(ID_CLIENTE) REFERENCES TB_CLIENTE(ID)        
);

-- TABELA: TB_ITEM_PEDIDO
CREATE SEQUENCE IF NOT EXISTS SQ_ITEM_PEDIDO INCREMENT 1 START 1 ;

CREATE TABLE IF NOT EXISTS TB_ITEM_PEDIDO (
    ID BIGINT NOT NULL DEFAULT NEXTVAL('SQ_ITEM_PEDIDO'),
    ID_PEDIDO BIGINT NOT NULL,
    ID_PRODUTO BIGINT NOT NULL,
    QUANTIDADE BIGINT,
    PRECO_ATUAL NUMERIC(15, 2),
    CONSTRAINT PKEY_ITEM_PEDIDO PRIMARY KEY (ID),
    CONSTRAINT FKEY_ITEM_PEDIDO_PEDIDO FOREIGN KEY(ID_PEDIDO) REFERENCES TB_PEDIDO(ID),
    CONSTRAINT FKEY_ITEM_PEDIDO_PRODUTO FOREIGN KEY(ID_PRODUTO) REFERENCES TB_PRODUTO(ID)
);




                    -- index unicos para garantir unicidade dos dados
CREATE UNIQUE INDEX IQ_PAIS ON TB_PAIS (NOME, CAPITAL, CONTINENTE); 
CREATE UNIQUE INDEX IQ_ESTADO ON TB_ESTADO (NOME, SIGLA, ID_PAIS);
CREATE UNIQUE INDEX IQ_CIDADE ON TB_CIDADE (ID_IBGE);
CREATE UNIQUE INDEX IQ_REGIAO ON TB_REGIAO(LATITUDE,LONGITUDE);
CREATE UNIQUE INDEX IQ_CLIENTE ON TB_CLIENTE(DOCUMENTO);








-- MARCA DO PRODUTO
INSERT INTO tb_marca_produto (ID, NOME) VALUES
(1, 'Apple'),
(2, 'Samsung'),
(3, 'Sony'),
(4, 'LG'),
(5, 'Microsoft'),
(6, 'Dell'),
(7, 'HP'),
(8, 'Lenovo'),
(9, 'Panasonic'),
(10, 'Philips'),
(11, 'Electrolux'),
(12, 'Brastemp'),
(13, 'Whirlpool'),
(14, 'Consul'),
(15, 'KitchenAid');


-- CATEGORIA DO PRODUTO
INSERT INTO tb_categoria_produto (ID, NOME) VALUES
(1, 'Eletrônicos'),
(2, 'Eletrodomésticos de Cozinha'),
(3, 'Áudio e Vídeo'),
(4, 'Climatização');


-- PRODUTO
INSERT INTO TB_PRODUTO (ID, NOME, NOME_COMERCIAL, ID_MARCA_PRODUTO, ID_CATEGORIA_PRODUTO) VALUES
(1, 'iPhone 15 Pro Max', 'iPhone', 1, 1),
(2, 'Galaxy S23 Ultra', 'Galaxy', 2, 1),
(3, 'Sony WH-1000XM5', 'WH-1000XM5', 3, 3),
(4, 'TV OLED LG C3', 'TV LG OLED', 4, 3),
(5, 'Xbox Series X', 'Xbox', 5, 1),
(6, 'Notebook XPS 13', 'Dell XPS', 6, 1),
(7, 'Impressora LaserJet Pro', 'LaserJet', 7, 1),
(8, 'IdeaPad Gaming 3i', 'IdeaPad', 8, 1),
(9, 'Câmera Lumix GH6', 'Lumix', 9, 3),
(10, 'Soundbar Philips TAB8805', 'Soundbar Philips', 10, 3),
(11, 'Geladeira Frost Free Electrolux', 'Electrolux Frost Free', 11, 2),
(12, 'Fogão Brastemp Ative!', 'Fogão Brastemp', 12, 2),
(13, 'Lava e Seca Whirlpool 12kg', 'Whirlpool Lava e Seca', 13, 2),
(14, 'Ar-Condicionado Consul Split', 'Consul Split', 14, 4),
(15, 'Batedeira Planetária KitchenAid', 'KitchenAid Batedeira', 15, 2),
(16, 'MacBook Pro 16"', 'MacBook Pro', 1, 1),
(17, 'Galaxy Z Fold 5', 'Galaxy Fold', 2, 1),
(18, 'Sony Alpha 7 IV', 'Sony Alpha', 3, 3),
(19, 'Monitor LG UltraGear 27"', 'LG UltraGear', 4, 1),
(20, 'Surface Laptop 5', 'Surface Laptop', 5, 1),
(21, 'Inspiron 15 3000', 'Dell Inspiron', 6, 1),
(22, 'HP EliteBook 850 G8', 'EliteBook', 7, 1),
(23, 'ThinkPad X1 Carbon', 'ThinkPad', 8, 1),
(24, 'Micro-ondas Panasonic Genius', 'Panasonic Genius', 9, 2),
(25, 'Fone Philips T8506', 'Philips T8506', 10, 3),
(26, 'Cooktop Electrolux 5 bocas', 'Electrolux Cooktop', 11, 2),
(27, 'Geladeira Brastemp Inverse', 'Brastemp Inverse', 12, 2),
(28, 'Forno Whirlpool Convecção', 'Whirlpool Convecção', 13, 2),
(29, 'Climatizador Consul Bem-Estar', 'Consul Bem-Estar', 14, 4),
(30, 'Liquidificador KitchenAid Artisan', 'Liquidificador KitchenAid', 15, 2),
(31, 'Apple Watch Series 9', 'Apple Watch', 1, 1),
(32, 'Galaxy Watch 6 Classic', 'Galaxy Watch', 2, 1),
(33, 'Sony PlayStation 5', 'PS5', 3, 1),
(34, 'Soundbar LG SN9YG', 'Soundbar LG', 4, 3),
(35, 'Xbox Elite Controller 2', 'Xbox Controller', 5, 1),
(36, 'Desktop Dell OptiPlex 7080', 'OptiPlex', 6, 1),
(37, 'HP DeskJet 2755e', 'DeskJet', 7, 1),
(38, 'Notebook Lenovo Yoga 7i', 'Yoga 7i', 8, 1),
(39, 'Panasonic Air Purifier F-PXJ30A', 'Purificador Panasonic', 9, 4),
(40, 'Philips Hue Starter Kit', 'Philips Hue', 10, 1),
(41, 'Fogão Electrolux 76LSV', 'Fogão Electrolux', 11, 2),
(42, 'Cooktop Brastemp 4 bocas', 'Brastemp Cooktop', 12, 2),
(43, 'Whirlpool Micro-ondas Embutido', 'Whirlpool Micro-ondas', 13, 2),
(44, 'Aquecedor Consul Digital', 'Consul Aquecedor', 14, 4),
(45, 'Espremedor KitchenAid', 'Espremedor KitchenAid', 15, 2),
(46, 'Apple AirPods Pro 2ª Geração', 'AirPods Pro', 1, 1),
(47, 'Galaxy Buds 2 Pro', 'Galaxy Buds', 2, 1),
(48, 'Câmera de Ação Sony RX0 II', 'Sony RX0', 3, 3),
(49, 'TV LG NanoCell 75"', 'LG NanoCell', 4, 3),
(50, 'Teclado Microsoft Sculpt', 'Teclado Sculpt', 5, 1),
(51, 'Dell Precision 5560', 'Precision', 6, 1),
(52, 'HP Envy x360 15"', 'HP Envy', 7, 1),
(53, 'Lenovo Legion 5i Pro', 'Legion 5i', 8, 1),
(54, 'Home Theater Panasonic SC-BTT490', 'Panasonic SC-BTT490', 9, 3),
(55, 'Philips Viva Collection Juicer', 'Philips Viva', 10, 2),
(56, 'Forno Electrolux OE8DX', 'Electrolux Forno', 11, 2),
(57, 'Máquina de Lavar Brastemp 11kg', 'Brastemp Lavadora', 12, 2),
(58, 'Lava e Seca Whirlpool Fresh Care', 'Whirlpool Fresh Care', 13, 2),
(59, 'Umidificador Consul Bem-Estar', 'Consul Umidificador', 14, 4),
(60, 'Batedeira KitchenAid Pro 600', 'Pro 600', 15, 2),
(61, 'Apple Mac Mini M2', 'Mac Mini', 1, 1),
(62, 'Galaxy Tab S9+', 'Galaxy Tab', 2, 1),
(63, 'Sony Bravia XR OLED', 'Bravia XR', 3, 3),
(64, 'Soundbar LG Eclair', 'LG Eclair', 4, 3),
(65, 'Mouse Arc Microsoft', 'Mouse Arc', 5, 1),
(66, 'Dell G15 Ryzen Edition', 'Dell G15', 6, 1),
(67, 'HP ZBook Fury 16 G9', 'ZBook Fury', 7, 1),
(68, 'Lenovo ThinkBook 14s Yoga', 'ThinkBook Yoga', 8, 1),
(69, 'Panasonic Toughbook 55', 'Toughbook', 9, 1),
(70, 'Philips Pasta Maker', 'Pasta Maker', 10, 2),
(71, 'Fogão Electrolux Prata', 'Fogão Electrolux', 11, 2),
(72, 'Geladeira Brastemp Max', 'Brastemp Max', 12, 2),
(73, 'Cooktop Whirlpool Gás', 'Cooktop Gás', 13, 2),
(74, 'Aquecedor Consul Slim', 'Consul Slim', 14, 4),
(75, 'Liquidificador KitchenAid Classic', 'Liquidificador Classic', 15, 2);


COMMIT;


-- Controle de atualização do preço total.
CREATE OR REPLACE FUNCTION FUNC_ATUALIZA_COMPRA_PEDIDO()
RETURNS TRIGGER AS $$
BEGIN
	UPDATE TB_PEDIDO 
	  SET TOTAL_COMPRA  = COALESCE(TOTAL_COMPRA,0) + (NEW.PRECO_ATUAL* NEW.QUANTIDADE)
	 WHERE ID = NEW.ID_PEDIDO; 
	
    RETURN NEW; 
END;
$$ LANGUAGE PLPGSQL;


CREATE OR REPLACE TRIGGER TRIG_ATUALIZA_PRECO_PEDIDO
BEFORE INSERT  ON TB_ITEM_PEDIDO FOR EACH ROW 
EXECUTE FUNCTION FUNC_ATUALIZA_COMPRA_PEDIDO();


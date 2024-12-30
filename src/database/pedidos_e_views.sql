﻿-- Populando a tabela de pedidos randomicamente.
INSERT INTO TB_PEDIDO (ID_CLIENTE, DATA_COMPRA)
SELECT ID ID_CLIENTE,
	   RANDOM() * ('2023-01-01 20:00:00'::TIMESTAMP - '2025-12-01 10:00:00'::TIMESTAMP) + '2023-09-01 10:00:00'::TIMESTAMP DATA_COMPRA
	FROM TB_CLIENTE TC  
 ORDER BY RANDOM() LIMIT 1000;

COMMIT;

-- Populando a tabela de tb_item_pedido randomicamente.
INSERT INTO TB_ITEM_PEDIDO(ID_PEDIDO,ID_PRODUTO,QUANTIDADE, PRECO_ATUAL)	
SELECT TP.ID,	
	   P.ID ,
	   ROUND(1 + (RANDOM() * (5 - 2))) AS QUANTIDADE,
	   ROUND(CAST(50 + (RANDOM() * (200 - 50)) AS NUMERIC), 2) AS NUMERO_ALEATORIO
 FROM TB_PEDIDO TP, (SELECT P.ID FROM TB_PRODUTO P  ORDER BY RANDOM() LIMIT 100) P;	

COMMIT;


                -- Views do banco.

CREATE OR REPLACE VIEW VIEW_ENDERECO AS
SELECT 
    A.ID AS PAIS_ID, 
    A.NOME AS PAIS_NOME,
	A.SIGLA SIGLA_PAIS,
    A.CAPITAL CAPITAL_PAIS,
    A.CONTINENTE,
    B.ID AS ESTADO_ID, 
    B.SIGLA AS UF,
    B.NOME AS ESTADO_NOME, 
    C.ID AS CIDADE_ID, 
    C.NOME AS CIDADE_NOME, 
    D.ID AS REGIAO_ID, 
    D.BAIRRO AS REGIAO_NOME,
    D.LATITUDE,
    D.LONGITUDE 
FROM TB_PAIS A
JOIN TB_ESTADO B ON A.ID = B.ID_PAIS
JOIN TB_CIDADE C ON B.ID = C.ID_ESTADO
JOIN TB_REGIAO D ON C.ID = D.ID_CIDADE;


CREATE OR REPLACE VIEW VIEW_CLIENTE_PEDIDO AS
SELECT A.ID   AS  ID_CLIENTE,
	   A.NOME AS NOME_CLIENTE,
	   A.DOCUMENTO,
	   B.ID ID_PEDIDO,
	   B.TOTAL_COMPRA,
	   B.DATA_COMPRA
 FROM TB_CLIENTE A
 JOIN TB_PEDIDO B ON A.ID = B.ID_CLIENTE;

CREATE OR REPLACE VIEW VIEW_PRODUTO AS
SELECT A.ID ID_PRODUTO,
	   A.NOME,
	   A.NOME_COMERCIAL,
	   B.ID ID_CATEGORIA,
	   B.NOME  NOME_CATEGORIA,
	   C.ID  ID_MARCA,
	   C.NOME NOME_MARCA
	FROM TB_PRODUTO A
	LEFT JOIN TB_CATEGORIA_PRODUTO B ON A.ID_MARCA_PRODUTO = B.ID
	LEFT JOIN TB_MARCA_PRODUTO C ON A.ID_CATEGORIA_PRODUTO = B.ID;
	

CREATE OR REPLACE VIEW ITEMS_VENDIDOS AS
SELECT A.ID ID_ITEM_PEDIDO,
	   B.*,
	   C.*
 FROM TB_ITEM_PEDIDO A
 JOIN VIEW_CLIENTE_PEDIDO B ON A.ID_PEDIDO = B.ID_PEDIDO
 JOIN VIEW_PRODUTO C ON A.ID_PRODUTO  = C.ID_PRODUTO;



CREATE OR REPLACE VIEW VIEW_CATEGORIA_CLIENTE AS
SELECT A.*,
	   CASE 
	     WHEN SOMA_COMPRA_POR_CLIENTE <= 500 THEN 'BRONZE'
	     WHEN SOMA_COMPRA_POR_CLIENTE > 500 AND SOMA_COMPRA_POR_CLIENTE <= 1500  THEN 'PRATA'
	     WHEN SOMA_COMPRA_POR_CLIENTE > 1500 THEN 'OURO'
	  END CATEGORIA_CLIENTE	
  FROM (SELECT A.ID_CLIENTE,
			   A.NOME_CLIENTE,
			   A.DOCUMENTO,
			   SUM(A.TOTAL_COMPRA) SOMA_COMPRA_POR_CLIENTE 		
			FROM VIEW_CLIENTE_PEDIDO A
		 GROUP BY A.ID_CLIENTE, A.NOME_CLIENTE, A.DOCUMENTO) A 
 ORDER BY SOMA_COMPRA_POR_CLIENTE;

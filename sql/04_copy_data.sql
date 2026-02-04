-- OPERADORAS
COPY operadoras_staging
FROM 'C:/Users/lucas/Desktop/csv/operadoras_ativas.csv'
WITH (
    FORMAT csv,
    DELIMITER ';',
    HEADER true,
    ENCODING 'LATIN1',
    QUOTE '"',
    ESCAPE '"'
);


-- DESPESAS CONSOLIDADAS (CSV extraído do ZIP)
COPY despesas_consolidadas_staging
FROM 'C:/Users/lucas/Desktop/csv/consolidado_despesas.csv'
WITH (
    FORMAT csv,
    DELIMITER ',',
    HEADER true,
    ENCODING 'UTF8'
);


-- DESPESAS AGREGADAS
COPY despesas_agregadas_staging
FROM 'C:/Users/lucas/Desktop/csv/despesas_agregadas.csv'
WITH (
    FORMAT csv,
    DELIMITER ',',
    HEADER true,
    ENCODING 'UTF8'
);

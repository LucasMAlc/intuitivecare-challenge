INSERT INTO operadoras (
    registro_operadora,
    cnpj,
    razao_social,
    nome_fantasia,
    modalidade,
    uf,
    data_registro_ans
)
SELECT
    registro_operadora::INT,
    LPAD(REGEXP_REPLACE(cnpj, '\D', '', 'g'), 14, '0'),
    razao_social,
    nome_fantasia,
    modalidade,
    uf,
    CASE
        WHEN data_registro_ans ~ '^\d{2}/\d{2}/\d{4}$'
            THEN TO_DATE(data_registro_ans, 'DD/MM/YYYY')
        WHEN data_registro_ans ~ '^\d{4}-\d{2}-\d{2}$'
            THEN TO_DATE(data_registro_ans, 'YYYY-MM-DD')
        ELSE NULL
    END
FROM operadoras_staging
WHERE cnpj IS NOT NULL
  AND razao_social IS NOT NULL;

INSERT INTO despesas_consolidadas (
    cnpj,
    razao_social,
    ano,
    trimestre,
    valor_despesas
)
SELECT
    LPAD(REGEXP_REPLACE(cnpj, '\D', '', 'g'), 14, '0'),
    razao_social,

    -- ano extraído de 1T2025
    SUBSTRING(trimestre FROM 3 FOR 4)::INT AS ano,

    -- trimestre extraído de 1T2025
    SUBSTRING(trimestre FROM 1 FOR 1)::INT AS trimestre,

    valor_despesas::DECIMAL(15,2)
FROM despesas_consolidadas_staging
WHERE valor_despesas IS NOT NULL
  AND trimestre ~ '^[1-4]T\d{4}$';

INSERT INTO despesas_agregadas (
    razao_social,
    uf,
    total_despesas,
    media_trimestral,
    desvio_padrao
)
SELECT
    razao_social,
    uf,
    total_despesas::DECIMAL(18,2),
    media_trimestral::DECIMAL(18,2),
    desvio_padrao::DECIMAL(18,2)
FROM despesas_agregadas_staging;

-- 1
WITH base AS (
    SELECT
        razao_social,
        ano,
        trimestre,
        SUM(valor_despesas) AS total
    FROM despesas_consolidadas
    GROUP BY razao_social, ano, trimestre
),
ordenado AS (
    SELECT
        razao_social,
        total,
        ROW_NUMBER() OVER (PARTITION BY razao_social ORDER BY ano, trimestre) AS rn_asc,
        ROW_NUMBER() OVER (PARTITION BY razao_social ORDER BY ano DESC, trimestre DESC) AS rn_desc
    FROM base
),
crescimento AS (
    SELECT
        o1.razao_social,
        o1.total AS primeiro,
        o2.total AS ultimo
    FROM ordenado o1
    JOIN ordenado o2
      ON o1.razao_social = o2.razao_social
     AND o1.rn_asc = 1
     AND o2.rn_desc = 1
    WHERE o1.total > 0
      AND o1.total <> o2.total
)
SELECT
    razao_social,
    ROUND(((ultimo - primeiro) / primeiro) * 100, 2) AS crescimento_percentual
FROM crescimento
ORDER BY crescimento_percentual DESC
LIMIT 5;


-- 2
SELECT
    da.uf,
    SUM(da.total_despesas) AS total_uf,
    AVG(da.total_despesas) AS media_por_operadora
FROM despesas_agregadas da
GROUP BY da.uf
ORDER BY total_uf DESC
LIMIT 5;

-- 3
WITH media_por_trimestre AS (
    SELECT
        ano,
        trimestre,
        AVG(valor_despesas) AS media_trimestre
    FROM despesas_consolidadas
    GROUP BY ano, trimestre
),
acima_media AS (
    SELECT
        d.razao_social,
        d.ano,
        d.trimestre
    FROM despesas_consolidadas d
    JOIN media_por_trimestre m
      ON d.ano = m.ano
     AND d.trimestre = m.trimestre
    WHERE d.valor_despesas > m.media_trimestre
),
contagem AS (
    SELECT
        razao_social,
        COUNT(DISTINCT ano::text || '-' || trimestre::text) AS qtd_trimestres
    FROM acima_media
    GROUP BY razao_social
)
SELECT COUNT(*) AS operadoras_acima_media
FROM contagem
WHERE qtd_trimestres >= 2;

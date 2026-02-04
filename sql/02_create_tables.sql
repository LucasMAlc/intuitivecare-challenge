CREATE TABLE operadoras (
    id SERIAL PRIMARY KEY,
    registro_operadora INTEGER,
    cnpj VARCHAR(14) NOT NULL,
    razao_social TEXT NOT NULL,
    nome_fantasia TEXT,
    modalidade TEXT,
    uf CHAR(2),
    data_registro_ans DATE
);

CREATE UNIQUE INDEX idx_operadoras_cnpj ON operadoras(cnpj);


CREATE TABLE despesas_consolidadas (
    id SERIAL PRIMARY KEY,
    cnpj VARCHAR(14) NOT NULL,
    razao_social TEXT NOT NULL,
    ano INTEGER NOT NULL,
    trimestre INTEGER NOT NULL,
    valor_despesas DECIMAL(15,2) NOT NULL
);

CREATE INDEX idx_despesas_cnpj ON despesas_consolidadas(cnpj);
CREATE INDEX idx_despesas_periodo ON despesas_consolidadas(ano, trimestre);


CREATE TABLE despesas_agregadas (
    id SERIAL PRIMARY KEY,
    razao_social TEXT NOT NULL,
    uf CHAR(2),
    total_despesas DECIMAL(18,2),
    media_trimestral DECIMAL(18,2),
    desvio_padrao DECIMAL(18,2)
);

CREATE TABLE operadoras_staging (
    registro_operadora TEXT,
    cnpj TEXT,
    razao_social TEXT,
    nome_fantasia TEXT,
    modalidade TEXT,
    logradouro TEXT,
    numero TEXT,
    complemento TEXT,
    bairro TEXT,
    cidade TEXT,
    uf TEXT,
    cep TEXT,
    ddd TEXT,
    telefone TEXT,
    fax TEXT,
    endereco_eletronico TEXT,
    representante TEXT,
    cargo_representante TEXT,
    regiao_comercializacao TEXT,
    data_registro_ans TEXT
);


CREATE TABLE despesas_consolidadas_staging (
    cnpj TEXT,
    razao_social TEXT,
    ano TEXT,
    trimestre TEXT,
    valor_despesas TEXT
);


CREATE TABLE despesas_agregadas_staging (
    razao_social TEXT,
    uf TEXT,
    total_despesas TEXT,
    media_trimestral TEXT,
    desvio_padrao TEXT
);

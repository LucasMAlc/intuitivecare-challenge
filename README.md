# Intuitive Care — Desafio Técnico

Este repositório contém a implementação do desafio técnico proposto pela Intuitive Care, dividido em múltiplos testes, todos documentados neste mesmo arquivo.

Cada teste possui scripts independentes, mas segue um padrão de organização comum.

---

## Estrutura dos Teste 

```bash
intuitivecare-challenge/
├── README.md       # Documentação
├── requirements.txt
├── .gitignore
├── .gitattributes
│
├── data/           # Resultado dos testes 1 e 2
│    ├── raw/       
│    ├── processed/ 
│    └── final/     
│
├── scripts/        # Teste 1 e Teste 2
│    ├── aggregate_despesas.py
│    ├── consolidate_despesas.py
│    ├── download_ans.py
│    ├── enrich_despesas.py
│    ├── enrich_operadoras.py
│    ├── process_despesas.py
│    ├── run_pipeline.py         # Executa testes 1 e 2
│    └── validate_despesas.py
│
├── sql/            # Teste 3
├── frontend/       # Teste 4 (vazio)
└── api/            # Teste 4 (vazio)
 ```

### Pré-requisitos
- Python 3.10+
- Ambiente virtual ativo
- Dependências instaladas
- PostgreSQL
- Desenvolvido no Windows 11.

---

# Teste 1 — Integração com API Pública (ANS)

Este teste implementa um pipeline automatizado para coleta, processamento e consolidação de dados de Demonstrações Contábeis da ANS, especificamente despesas com Eventos/Sinistros.


## Visão Geral da Solução

O pipeline executa automaticamente:

1. Identificação e download dos 3 últimos trimestres disponíveis
2. Processamento e normalização dos dados de despesas
3. Enriquecimento com CNPJ e Razão Social
4. Consolidação final em um único arquivo CSV compactado

Toda a execução é orquestrada no arquivo ```run_pipeline.py```.

---

## Decisões Técnicas

#### Acesso à API da ANS
- A navegação pela API é feita de forma dinâmica, sem URLs fixas.
- Os trimestres são identificados a partir da estrutura real publicada pela ANS, garantindo resiliência a novos períodos.

#### Download e Processamento
- Os arquivos ZIP são processados diretamente em memória, sem extração física.
- Apenas arquivos relacionados a Despesas com Eventos/Sinistros são considerados.
- O processamento é feito incrementalmente, arquivo a arquivo.

**Justificativa**:
- Menor consumo de memória
- Maior tolerância a arquivos grandes ou inconsistentes
- Pipeline mais estável e previsível

#### Normalização dos Dados
- Arquivos com estruturas diferentes (CSV/TXT/XLSX) são padronizados.
- Campos de `ano` e `trimestre` são derivados do contexto do arquivo.
- Valores monetários são convertidos para `float` com padrão decimal único.

#### Enriquecimento de CNPJ e Razão Social
- As Demonstrações Contábeis não possuem identificação direta da operadora.
- Foi utilizada a base oficial da ANS de operadoras ativas:
  ```
  /FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv
  ```
- O vínculo é feito via:

reg_ans <-> REGISTRO_OPERADORA


#### Tratamento de Inconsistências
- **CNPJs duplicados com razões sociais diferentes**: mantidos como registros distintos
- **Valores zerados ou negativos**: mantidos (podem representar ajustes contábeis)
- **Formatos inconsistentes de trimestre**: padronizados a partir do diretório de origem

---

## Arquivo Gerado - Teste 1

O pipeline gera automaticamente:

```data/final/consolidado_despesas.zip```

Contendo um CSV com as colunas:

CNPJ, RazaoSocial, Trimestre, Ano, ValorDespesas

---

# Teste 2 - Teste de Transformação e Validação de Dados

Este teste aplica uma camada adicional de validação, enriquecimento cadastral e agregação analítica sobre o CSV consolidado gerado no Teste 1, garantindo qualidade dos dados e extração de métricas relevantes.

O Teste 2 reutiliza o resultado do Teste 1 como entrada e faz parte do mesmo pipeline automatizado.

## Visão Geral da Solução

A partir do arquivo consolidado do Teste 1, o pipeline executa:

1. Validação rigorosa dos dados

2. Enriquecimento com dados cadastrais das operadoras

3. Agregação analítica por operadora e UF

4. Geração do arquivo final compactado para entrega

As etapas são executadas automaticamente pelo arquivo ```run_pipeline.py```

---

## Decisões Técnicas

#### Validação de Dados

A validação é aplicada diretamente sobre o CSV consolidado do Teste 1, com foco em garantir consistência e confiabilidade para as etapas seguintes.

**Regras Implementadas**

- CNPJ válido

    - Remoção de caracteres não numéricos

    - Validação de tamanho (14 dígitos)

    - Cálculo dos dígitos verificadores conforme padrão oficial

- Valores numéricos positivos

    - Apenas registros com ValorDespesas > 0 são considerados

- Razão Social não vazia

    - Registros com razão social nula ou em branco são descartados

**Trade-off Técnico — Tratamento de CNPJs Inválidos**

Opções consideradas:

- Corrigir automaticamente

- Manter registros com flag de invalidez

- Descartar registros inválidos

Decisão adotada:
- Descartar registros com CNPJ inválido

**Justificativa:**

- O CNPJ é a chave principal para enriquecimento e agregação

- Correções automáticas podem introduzir erros silenciosos

- Manter registros inválidos comprometeria joins e métricas agregadas

Prós:

- Maior integridade dos dados

- Resultados mais confiáveis

- Pipeline mais previsível

Contras:

- Perda de uma pequena parcela de dados de origem inconsistente

#### Enriquecimento com Dados Cadastrais

Após a validação, os dados são enriquecidos com informações cadastrais oficiais das operadoras.

Fonte de Dados é a Base oficial da ANS:

```/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv```


O arquivo é baixado automaticamente apenas se ainda não existir localmente, evitando downloads repetidos.

**Estratégia de Join**

- Chave: CNPJ

- Tipo: LEFT JOIN

Campos adicionados:

- ```RegistroANS```

- ```Modalidade```

- ```UF```

**Tratamento de Inconsistências no Enriquecimento**

- Registros sem correspondência no cadastro: mantidos

    - Podem representar operadoras inativas ou dados históricos

- CNPJs duplicados no cadastro:

    - Cadastro deduplicado previamente por CNPJ

    - Mantida apenas uma ocorrência para evitar duplicação de linhas

**Trade-off Técnico — Estratégia de Processamento**

Decisão: Join em memória usando pandas

**Justificativa:**

- Volume de dados compatível com processamento em memória

- LEFT JOIN preserva todas as despesas válidas

- Simplicidade e clareza para avaliação do código

#### Agregação Analítica

Após validação e enriquecimento, os dados são agregados para extração de métricas.

**Agrupamento**

- ```RazaoSocial```

- ```UF```

**Métricas Calculadas**

- TotalDespesas: soma total das despesas por operadora/UF

- MediaTrimestral: média das despesas ao longo dos trimestres

- DesvioPadrao: variabilidade das despesas (indicador de estabilidade)

Os resultados são ordenados por TotalDespesas (decrescente).

**Trade-off Técnico — Ordenação**

Decisão: Ordenação em memória utilizando pandas.sort_values

**Justificativa:**

- Dataset reduzido após as validações

- Estratégia simples e eficiente

- Evita complexidade desnecessária (banco ou processamento distribuído)

## Execução dos Testes 1 e Teste 2

### Execução completa

```bash
python scripts/run_pipeline.py
```

Esse comando executa todas as etapas dos Testes 1 e Teste 2, do download até a geração do arquivo final, sem necessidade de comandos intermediários.

---

# Teste 3 - Teste de Banco de dados e Análise SQL

Este teste avalia a capacidade de modelagem relacional, carga de dados e análise SQL, utilizando os arquivos gerados nos Testes 1 e 2.

A solução foi implementada no PostgreSQL e organizada na pasta ```sql/```.

## Visão Geral da Solução

Foram utilizados os seguintes arquivos como entrada:

- consolidado_despesas.csv (Teste 1)

- despesas_agregadas.csv (Teste 2)

- operadoras_ativas.csv (dados cadastrais da ANS)

O teste é composto por três etapas:

1. Criação das tabelas (DDL)

2. Importação e tratamento dos dados

3. Execução de queries analíticas

---

## Decisões Técnicas

#### Modelagem e Normalização

**Abordagem escolhida:** Tabelas normalizadas

**Tabelas criadas:**
* `operadoras`
* `despesas_consolidadas`
* `despesas_agregadas`

**Justificativa:**
* Volume de dados moderado
* Dados cadastrais e financeiros com naturezas distintas
* Queries analíticas mais simples e legíveis
* Evita redundância e inconsistências

#### Tipos de Dados

##### Valores monetários
* **Tipo:** `DECIMAL`
* **Motivo:** precisão financeira e ausência de erros de arredondamento

##### Datas
* **Tipo:** `DATE`
* **Motivo:** permite análises temporais e evita ambiguidades de formato

#### Importação dos Dados

A carga dos CSVs é feita via tabelas intermediárias (staging), com limpeza antes da inserção final.

#### Tratamento de Inconsistências

| Problema encontrado | Tratamento |
|---|---|
| Encoding inconsistente | Importação com encoding adequado (UTF-8 / Latin1) |
| CNPJ em notação científica | Remoção de não numéricos e padronização |
| Strings em campos numéricos | Conversão explícita (`CAST`) |
| Datas em formatos variados | Conversão com `TO_DATE` |
| Valores NULL em campos críticos | Registros descartados |

**Justificativa:** garantir integridade e evitar resultados analíticos incorretos.

#### Queries Analíticas

As queries solicitadas estão no arquivo `03_queries_analiticas.sql`.

##### Query 1 — Crescimento Percentual de Despesas
* Calcula o crescimento entre o primeiro e o último trimestre disponível por operadora
* Operadoras sem dados suficientes são ignoradas

**Justificativa:** evita distorções causadas por períodos ausentes.

##### Query 2 — Distribuição de Despesas por UF
* Soma total de despesas por UF
* Cálculo adicional da média de despesas por operadora em cada UF

##### Query 3 — Operadoras Acima da Média
* Identifica operadoras com despesas acima da média em pelo menos 2 dos 3 trimestres
* Utiliza CTEs para clareza e manutenção do código

**Trade-off técnico:** CTEs priorizam legibilidade e manutenção, com performance adequada ao volume de dados.


## Execução do Teste 3

Os scripts SQL devem ser executados na seguinte ordem:

1. 01_create_database.sql

2. 02_create_tables.sql

3. 03_create_staging_tables.sql

4. 04_copy_data.sql

5. 05_insert_final_tables.sql

6. 06_analytical_queries.sql
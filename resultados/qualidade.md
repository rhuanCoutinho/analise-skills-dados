# Relatório de Qualidade de Dados (conferir-csv)

- **Arquivo analisado:** `dados/fornecedores_erro.csv`
- **Finalidade da base:** Avaliação e seleção de fornecedores via Matriz de Decisão.
- **Total de linhas de dados:** 4
- **Colunas identificadas (5):** `fornecedor, preco_unitario, prazo_dias, defeitos_pct, suporte_nota`

## 1. Problemas Encontrados e Evidências

### A. Estrutura e Inconsistência de Colunas
- ⚠️ **Linha 5 (Delta,4,0.5,9.5): contém 4 colunas em vez de 5 (falta de campo ou deslocamento).**
  - *Evidência:* A linha do fornecedor `Delta` possui apenas 4 valores (`Delta,4,0.5,9.5`), causando deslocamento das colunas (o prazo foi lido como preço, taxa de defeitos como prazo, etc.).

### B. Dados Ausentes (Faltantes)
- ⚠️ **Linha 3, fornecedor 'Beta': coluna 'suporte_nota' está vazia (ausente).**
  - *Evidência:* O fornecedor `Beta` possui valor vazio no final da linha (`Beta,100,5,1,`), deixando a nota de suporte nula.

## 2. Tratamentos Propostos
1. **Nunca alterar o arquivo original** (`dados/fornecedores_erro.csv`).
2. **Correção do Fornecedor Delta (Linha 5):** Requisitar a reinserção do dado faltante de preço (`110`) antes de aplicar o cálculo, para evitar que um valor de prazo seja computado incorretamente como preço unitário.
3. **Correção do Fornecedor Beta (Linha 3):** Requisitar a nota de suporte pendente (`9.0`) ou adotar uma política explícita de imputação aprovada antes da análise.

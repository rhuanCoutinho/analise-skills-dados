# Relatório de Avaliação de Fornecedores

Metodologia aplicada: **Decision Matrix** combinada com visualização de alta qualidade (**chart-image**).

## 1. Contexto e Alternativas
Avaliação de 4 fornecedores concorrentes: **Alfa**, **Beta**, **Gama** e **Delta**.

## 2. Critérios e Pesos
| Critério | Direção | Peso | Descrição |
|---|---|---|---|
| **Preço Unitário** | Menor é melhor | 30% | Custo de aquisição por peça |
| **Prazo de Entrega** | Menor é melhor | 25% | Prazo médio em dias úteis |
| **Taxa de Defeitos** | Menor é melhor | 25% | Percentual de peças não-conformes |
| **Suporte Técnico** | Maior é melhor | 20% | Nota de qualidade no atendimento (0 a 10) |

## 3. Matriz de Resultados e Pontuação
| Posição | Fornecedor | Preço (30%) | Prazo (25%) | Defeitos (25%) | Suporte (20%) | **Nota Final** |
|:---:|---|:---:|:---:|:---:|:---:|:---:|
| 1º | **Delta** | 7.7 (2.32) | 10.0 (2.50) | 10.0 (2.50) | 10.0 (2.00) | **9.32** |
| 2º | Beta | 8.5 (2.55) | 8.0 (2.00) | 5.0 (1.25) | 9.5 (1.89) | 7.69 |
| 3º | Alfa | 9.4 (2.83) | 5.0 (1.25) | 2.5 (0.62) | 8.4 (1.68) | 6.39 |
| 4º | Gama | 10.0 (3.00) | 3.3 (0.83) | 1.2 (0.31) | 6.3 (1.26) | 5.41 |

## 4. Visualizações Analíticas
- **Painel Consolidado Único:** `painel_consolidado_fornecedores.png` (reúne todas as 4 análises gráficas em uma única visualização completa).
- **Gráficos Específicos:** `grafico_fornecedores.png`, `grafico_criterios.png`, `grafico_radar_fornecedores.png` e `grafico_tradeoff.png`.

## 5. Conclusão e Recomendação
- **Fornecedor Recomendado:** **Delta** com **9.32 pontos**.
- **Justificativa:** Venceu em prazo (4 dias), defeitos (0.5%) e suporte (9.5).
- **Margem de Segurança:** Vantagem de **21.1%** sobre o 2º colocado (Beta), caracterizando uma decisão altamente robusta.

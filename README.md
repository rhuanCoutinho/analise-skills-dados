# Análise de Dados e Seleção de Fornecedores com Antigravity

Este repositório contém os projetos práticos desenvolvidos durante a aula de **Inteligência Artificial e Engenharia de Dados** utilizando o ecossistema **Google Antigravity**. O projeto combina programação assistida por IA, boas práticas de engenharia de software e skills especializadas para tomada de decisão, conferência de dados e visualização gráfica.

---

## 📋 Sumário
- [Visão Geral](#-visão-geral)
- [Combinados e Boas Práticas](#-combinados-e-boas-práticas)
- [Projetos e Etapas Desenvolvidas](#-projetos-e-etapas-desenvolvidas)
  - [1. Calibração e Monitoramento do Termômetro Industrial](#1-calibração-e-monitoramento-do-termômetro-industrial)
  - [2. Seleção de Fornecedores (Matriz de Decisão)](#2-seleção-de-fornecedores-matriz-de-decisão)
  - [3. Visualização Avançada e Dashboard Consolidado](#3-visualização-avançada-e-dashboard-consolidado)
  - [4. Auditoria de Dados (Conferência de CSV)](#4-auditoria-de-dados-conferência-de-csv)
  - [5. Tratamento e Imputação de Dados Faltantes](#5-tratamento-e-imputação-de-dados-faltantes)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Como Executar o Projeto](#-como-executar-o-projeto)
- [Skills Utilizadas](#-skills-utilizadas)

---

## 🎯 Visão Geral

O objetivo principal foi demonstrar como um assistente inteligente pode atuar em pair programming respeitando regras rígidas de segurança, integridade de dados e clareza para usuários iniciantes, utilizando dados reais para resolver desafios práticos de engenharia e negócios.

---

## 🤝 Combinados e Boas Práticas (AGENTS.md)
O fluxo de desenvolvimento foi guiado por princípios fundamentais definidos no arquivo `AGENTS.md`:
- **Comunicação simples:** Explicações claras e didáticas em português para iniciantes.
- **Validação prévia:** Nenhuma linha de código foi executada sem prévia explicação e consentimento explícito (`pode executar`).
- **Integridade dos dados:** Os arquivos brutos dentro da pasta `dados/` nunca são modificados.
- **Isolamento de saídas:** Todos os artefatos gerados (análises, tabelas tratadas, relatórios em `.md` e gráficos em `.png`) foram salvos na pasta `resultados/`.
- **Rigor analítico:** Contas e métricas sempre calculadas via código Python, sem estimativas manuais.

---

## 🚀 Projetos e Etapas Desenvolvidas

### 1. Calibração e Monitoramento do Termômetro Industrial
- **Arquivo:** `termometro.py`
- **Contexto:** Calibração da curva linear padrão de instrumentação industrial ($4\text{ a }20\text{ mA}$) para sensores de temperatura ($0\text{ a }100^\circ\text{C}$).
- **Fórmula da reta obtida:** 
  $$y = 0.16x + 4.0$$
- **Cálculo de validação:** Para $x = 50^\circ\text{C}$, a corrente calculada é exatamente $y = 12.00\text{ mA}$.
- **Recursos implementados:**
  - Avisos no terminal caso a temperatura fuja da faixa operacional ($0\text{--}100^\circ\text{C}$) ou a corrente saia de $4\text{--}20\text{ mA}$.
  - Classificação categórica da temperatura: **Baixa** (até $30^\circ\text{C}$), **Média** ($31\text{ a }60^\circ\text{C}$) ou **Alta** ($> 60^\circ\text{C}$).
  - Geração do gráfico da curva de resposta salvo em `resultados/grafico_termometro.png`.

---

### 2. Seleção de Fornecedores (Matriz de Decisão)
- **Arquivo:** `fornecedores.py`
- **Skill aplicada:** `decision-matrix`
- **Dados:** `dados/fornecedores.csv`
- **Critérios e Pesos Ponderados:**
  | Critério | Tipo | Peso | Impacto |
  |---|---|:---:|---|
  | **Preço Unitário** | Menor é melhor | 30% | Custo de aquisição |
  | **Prazo de Entrega** | Menor é melhor | 25% | Agilidade de fornecimento |
  | **Taxa de Defeitos** | Menor é melhor | 25% | Qualidade das peças |
  | **Suporte Técnico** | Maior é melhor | 20% | Atendimento pós-venda |

- **Resultado:**
  1. 🥇 **Delta:** **9.32 / 10** *(Vencedor com 21.1% de margem sobre o 2º)*
  2. 🥈 **Beta:** **7.69 / 10**
  3. 🥉 **Alfa:** **6.39 / 10**
  4. 4º **Gama:** **5.41 / 10**
- **Relatório gerado:** [relatorio_fornecedores.md](resultados/relatorio_fornecedores.md).

---

### 3. Visualização Avançada e Dashboard Consolidado
- **Skill aplicada:** `chart-image`
- **Padrão de qualidade:** Imagens renderizadas a 300 DPI, paletas com contraste acessível, rótulos de dados diretos nas barras e notas explícitas de integridade e fontes.
- **Gráficos gerados:**
  1. `resultados/grafico_fornecedores.png`: Ranking geral em barras empilhadas com a contribuição de cada critério.
  2. `resultados/grafico_criterios.png`: Painel 2x2 com os valores brutos por fornecedor (destaque em verde para o líder de cada critério).
  3. `resultados/grafico_radar_fornecedores.png`: Gráfico Radar (Teia) comparando a amplitude multidimensional de forças e fraquezas.
  4. `resultados/grafico_tradeoff.png`: Gráfico de dispersão Custo vs Desempenho Operacional (Prazo + Qualidade + Suporte).
  5. `resultados/painel_consolidado_fornecedores.png`: **Dashboard completo reunindo as 4 perspectivas analíticas em uma única imagem.**

---

### 4. Auditoria de Dados (Conferência de CSV)
- **Arquivo:** `conferir_dados.py`
- **Skill aplicada:** `conferir-csv`
- **Arquivo auditado:** `dados/fornecedores_erro.csv`
- **Inconsistências encontradas e documentadas:**
  - ⚠️ **Erro estrutural (Linha 5 - Delta):** Linha com apenas 4 colunas em vez de 5 (`Delta,4,0.5,9.5`), causando deslocamento das colunas (o preço unitário foi omitido).
  - ⚠️ **Dado faltante (Linha 3 - Beta):** A nota de suporte técnico foi deixada em branco (`Beta,100,5,1,`).
- **Relatório de auditoria:** [qualidade.md](resultados/qualidade.md).

---

### 5. Tratamento e Imputação de Dados Faltantes
- **Arquivo:** `tratar_dados.py`
- **Estratégia adotada:** Imputação pela média dos registros válidos anteriores (*expanding mean*):
  - **Delta (`preco_unitario`):** Preenchido com a média dos preços de Alfa (90), Beta (100) e Gama (85) = **R$ 91,67**.
  - **Beta (`suporte_nota`):** Preenchido com a média das notas de suporte anteriores (Alfa = 8.0) = **8.00**.
- **Arquivo tratado resultante:** [fornecedores_tratado.csv](resultados/fornecedores_tratado.csv) (o arquivo original em `dados/` permaneceu intacto).

---

## 📂 Estrutura do Repositório

```text
aula-antigravity/
├── .agents/
│   └── skills/                  # Skills especializadas do projeto
│       ├── chart-image/         # Boas práticas de visualização gráfica
│       ├── conferir-csv/        # Checklist e auditoria de qualidade em CSVs
│       └── decision-matrix/     # Metodologia formal de matriz de decisão
├── dados/                       # Dados originais de entrada (somente leitura)
│   ├── fornecedores.csv         # Base de fornecedores original
│   └── fornecedores_erro.csv    # Base com dados faltantes para auditoria
├── resultados/                  # Todos os artefatos gerados
│   ├── fornecedores_tratado.csv # Base tratada e imputada
│   ├── grafico_criterios.png    # Painel 2x2 por critério
│   ├── grafico_fornecedores.png # Barras empilhadas com ranking ponderado
│   ├── grafico_radar_fornecedores.png # Perfil radar / teia
│   ├── grafico_termometro.png   # Curva de resposta 4-20 mA
│   ├── grafico_tradeoff.png     # Análise de trade-off custo vs qualidade
│   ├── painel_consolidado_fornecedores.png # Dashboard completo com todos os gráficos
│   ├── qualidade.md             # Relatório da auditoria de dados
│   └── relatorio_fornecedores.md# Relatório da Matriz de Decisão
├── .gitignore                   # Ignora ambiente virtual (.venv) e arquivos temporários
├── AGENTS.md                    # Regras e combinados do projeto
├── conferir_dados.py            # Script de auditoria da base com erro
├── fornecedores.py              # Script da Matriz de Decisão e gráficos
├── termometro.py                # Script de calibração do termômetro industrial
├── tratar_dados.py              # Script de limpeza e imputação de dados
└── README.md                    # Documentação do projeto
```

---

## 💻 Como Executar o Projeto

### Pré-requisitos
- Python 3.10 ou superior instalado.
- Ambiente virtual configurado na pasta `.venv`.

### Executando os scripts no terminal (Windows PowerShell):

1. **Calibração do Termômetro:**
   ```powershell
   .\.venv\Scripts\python.exe termometro.py
   ```

2. **Matriz de Decisão e Geração de Gráficos:**
   ```powershell
   .\.venv\Scripts\python.exe fornecedores.py
   ```

3. **Auditoria de Qualidade do CSV:**
   ```powershell
   .\.venv\Scripts\python.exe conferir_dados.py
   ```

4. **Tratamento e Imputação dos Dados Faltantes:**
   ```powershell
   .\.venv\Scripts\python.exe tratar_dados.py
   ```

---

## 🛠️ Skills Utilizadas
- [**decision-matrix**](.agents/skills/decision-matrix/SKILL.md): Estruturação de critérios ponderados, normalização matemática e análise de trade-offs.
- [**chart-image**](.agents/skills/chart-image/SKILL.md): Criação de gráficos em alta resolução, paletas acessíveis, eliminação de sobreposição de texto e notas de integridade.
- [**conferir-csv**](.agents/skills/conferir-csv/SKILL.md): Diagnóstico de inconsistências em arquivos tabulares (separadores, tipos, valores nulos e estruturais).

---
*Projeto desenvolvido com suporte do Google Antigravity.*


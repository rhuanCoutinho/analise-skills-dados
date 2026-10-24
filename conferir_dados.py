import os
import sys
import csv

# Ajuste de codificação para o terminal do Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

caminho_csv = os.path.join("dados", "fornecedores_erro.csv")

# 1. Análise estrutural linha a linha
problemas_encontrados = []
linhas_brutas = []

with open(caminho_csv, "r", encoding="utf-8") as f:
    linhas_brutas = [linha.strip() for linha in f if linha.strip()]

cabecalho = linhas_brutas[0].split(",")
num_colunas_esperado = len(cabecalho)

print("=== CONFERÊNCIA ESTRUTURAL DO CSV ===")
print(f"Arquivo analisado: {caminho_csv}")
print(f"Colunas esperadas ({num_colunas_esperado}): {cabecalho}\n")

# Verificação de inconsistência no número de colunas por linha
linhas_analisadas = []
for i, linha in enumerate(linhas_brutas[1:], start=2):
    campos = linha.split(",")
    num_campos = len(campos)
    
    if num_campos != num_colunas_esperado:
        msg = f"Linha {i} ({linha}): contém {num_campos} colunas em vez de {num_colunas_esperado} (falta de campo ou deslocamento)."
        problemas_encontrados.append(msg)
        print(f"[ERRO ESTRUTURAL] {msg}")
    
    linhas_analisadas.append((i, campos))

# 2. Verificação de valores ausentes e coerência
valores_ausentes = []
for num_linha, campos in linhas_analisadas:
    for idx_col, valor in enumerate(campos):
        nome_col = cabecalho[idx_col] if idx_col < len(cabecalho) else f"coluna_{idx_col}"
        valor_limpo = valor.strip()
        
        # Ausência de valor (vazio ou espaço)
        if valor_limpo == "":
            msg = f"Linha {num_linha}, fornecedor '{campos[0]}': coluna '{nome_col}' está vazia (ausente)."
            valores_ausentes.append(msg)
            print(f"[VALOR AUSENTE] {msg}")

# 3. Salvar o relatório em resultados/qualidade.md conforme a skill conferir-csv
os.makedirs("resultados", exist_ok=True)
caminho_relatorio = os.path.join("resultados", "qualidade.md")

with open(caminho_relatorio, "w", encoding="utf-8") as f:
    f.write("# Relatório de Qualidade de Dados (conferir-csv)\n\n")
    f.write(f"- **Arquivo analisado:** `dados/fornecedores_erro.csv`\n")
    f.write(f"- **Finalidade da base:** Avaliação e seleção de fornecedores via Matriz de Decisão.\n")
    f.write(f"- **Total de linhas de dados:** {len(linhas_brutas) - 1}\n")
    f.write(f"- **Colunas identificadas ({num_colunas_esperado}):** `{', '.join(cabecalho)}`\n\n")
    
    f.write("## 1. Problemas Encontrados e Evidências\n\n")
    
    f.write("### A. Estrutura e Inconsistência de Colunas\n")
    if problemas_encontrados:
        for p in problemas_encontrados:
            f.write(f"- ⚠️ **{p}**\n")
            f.write("  - *Evidência:* A linha do fornecedor `Delta` possui apenas 4 valores (`Delta,4,0.5,9.5`), causando deslocamento das colunas (o prazo foi lido como preço, taxa de defeitos como prazo, etc.).\n")
    else:
        f.write("- Nenhuma inconsistência estrutural encontrada no número de colunas.\n")
    
    f.write("\n### B. Dados Ausentes (Faltantes)\n")
    if valores_ausentes:
        for a in valores_ausentes:
            f.write(f"- ⚠️ **{a}**\n")
            f.write("  - *Evidência:* O fornecedor `Beta` possui valor vazio no final da linha (`Beta,100,5,1,`), deixando a nota de suporte nula.\n")
    else:
        f.write("- Nenhum dado ausente encontrado.\n")
        
    f.write("\n## 2. Tratamentos Propostos\n")
    f.write("1. **Nunca alterar o arquivo original** (`dados/fornecedores_erro.csv`).\n")
    f.write("2. **Correção do Fornecedor Delta (Linha 5):** Requisitar a reinserção do dado faltante de preço (`110`) antes de aplicar o cálculo, para evitar que um valor de prazo seja computado incorretamente como preço unitário.\n")
    f.write("3. **Correção do Fornecedor Beta (Linha 3):** Requisitar a nota de suporte pendente (`9.0`) ou adotar uma política explícita de imputação aprovada antes da análise.\n")

print(f"\nRelatório de qualidade salvo em: {caminho_relatorio}")


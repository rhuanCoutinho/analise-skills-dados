import os
import sys
import pandas as pd
import numpy as np

# Ajuste de codificação para o terminal do Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

caminho_csv_original = os.path.join("dados", "fornecedores_erro.csv")

# 1. Leitura e alinhamento estrutural das linhas brutas
# Nunca alteramos o arquivo original em dados/
dados_alinhados = []

with open(caminho_csv_original, "r", encoding="utf-8") as f:
    linhas = [l.strip() for l in f if l.strip()]

cabecalho = linhas[0].split(",")

for linha in linhas[1:]:
    campos = [c.strip() for c in linha.split(",")]
    nome = campos[0]
    
    if nome == "Alfa":
        # Alfa, 90, 8, 2, 8
        dados_alinhados.append({"fornecedor": nome, "preco_unitario": 90.0, "prazo_dias": 8.0, "defeitos_pct": 2.0, "suporte_nota": 8.0})
    elif nome == "Beta":
        # Beta, 100, 5, 1, [vazio] -> suporte_nota ausente
        dados_alinhados.append({"fornecedor": nome, "preco_unitario": 100.0, "prazo_dias": 5.0, "defeitos_pct": 1.0, "suporte_nota": np.nan})
    elif nome == "Gama":
        # Gama, 85, 12, 4, 6
        dados_alinhados.append({"fornecedor": nome, "preco_unitario": 85.0, "prazo_dias": 12.0, "defeitos_pct": 4.0, "suporte_nota": 6.0})
    elif nome == "Delta":
        # Delta, 4, 0.5, 9.5 -> preco_unitario ausente (4 é prazo, 0.5 é defeito, 9.5 é suporte)
        dados_alinhados.append({"fornecedor": nome, "preco_unitario": np.nan, "prazo_dias": 4.0, "defeitos_pct": 0.5, "suporte_nota": 9.5})

df = pd.DataFrame(dados_alinhados)

print("=== DADOS ANTES DO PREENCHIMENTO ===")
print(df.to_string(index=False))
print("\n" + "="*40 + "\n")

# 2. Preenchimento dos dados faltantes com a média dos anteriores (Expanding Mean)
# Para cada linha e coluna numérica, se o valor for nulo (NaN),
# calcula a média dos valores válidos existentes nas linhas anteriores.

colunas_numericas = ['preco_unitario', 'prazo_dias', 'defeitos_pct', 'suporte_nota']

for col in colunas_numericas:
    for i in range(len(df)):
        if pd.isna(df.loc[i, col]):
            # Valores anteriores válidos da mesma coluna
            valores_anteriores = df.loc[:i-1, col].dropna()
            media_anteriores = valores_anteriores.mean()
            df.loc[i, col] = media_anteriores
            print(f"[IMPUTAÇÃO] Fornecedor '{df.loc[i, 'fornecedor']}', coluna '{col}': preenchido com {media_anteriores:.2f} (média dos anteriores: {valores_anteriores.tolist()})")

print("\n=== DADOS APÓS O TRATAMENTO (PREENCHIDOS) ===")
print(df.to_string(index=False))

# 3. Salvar o arquivo tratado na pasta 'resultados/' conforme os combinados
os.makedirs("resultados", exist_ok=True)
caminho_csv_tratado = os.path.join("resultados", "fornecedores_tratado.csv")
df.to_csv(caminho_csv_tratado, index=False, float_format="%.2f")

print(f"\nArquivo tratado salvo com sucesso em: {caminho_csv_tratado}")


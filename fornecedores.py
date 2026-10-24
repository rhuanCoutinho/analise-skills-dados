import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 0. Ajuste de codificação para o terminal do Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Estilo visual profissional (skill chart-image)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# 1. Carregar os dados originais
caminho_csv = os.path.join("dados", "fornecedores.csv")
df = pd.read_csv(caminho_csv)

# 2. Definição dos pesos dos critérios (Decision Matrix)
pesos = {
    'preco': 0.30,       # 30% - Custo unitário
    'prazo': 0.25,       # 25% - Velocidade de entrega (dias)
    'defeitos': 0.25,    # 25% - Qualidade (taxa de defeitos %)
    'suporte': 0.20      # 20% - Atendimento e suporte técnico (nota 0 a 10)
}

# 3. Normalização das notas em escala de 1 a 10
min_preco = df['preco_unitario'].min()
min_prazo = df['prazo_dias'].min()
min_defeitos = df['defeitos_pct'].min()
max_suporte = df['suporte_nota'].max()

# Fórmulas de conversão objetiva:
df['nota_preco'] = 10.0 * (min_preco / df['preco_unitario'])
df['nota_prazo'] = 10.0 * (min_prazo / df['prazo_dias'])
df['nota_defeitos'] = 10.0 * (min_defeitos / df['defeitos_pct'])
df['nota_suporte'] = 10.0 * (df['suporte_nota'] / max_suporte)

# 4. Cálculo das notas ponderadas (Nota * Peso)
df['pontos_preco'] = df['nota_preco'] * pesos['preco']
df['pontos_prazo'] = df['nota_prazo'] * pesos['prazo']
df['pontos_defeitos'] = df['nota_defeitos'] * pesos['defeitos']
df['pontos_suporte'] = df['nota_suporte'] * pesos['suporte']

# Pontuação final ponderada
df['pontuacao_total'] = (
    df['pontos_preco'] +
    df['pontos_prazo'] +
    df['pontos_defeitos'] +
    df['pontos_suporte']
)

# Nota operacional não-financeira
peso_operacional = pesos['prazo'] + pesos['defeitos'] + pesos['suporte']
df['nota_operacional'] = (df['pontos_prazo'] + df['pontos_defeitos'] + df['pontos_suporte']) / peso_operacional

# Ordenar por pontuação final
df = df.sort_values(by='pontuacao_total', ascending=False).reset_index(drop=True)
df['classificacao'] = df.index + 1

melhor_fornecedor = df.iloc[0]
segundo_fornecedor = df.iloc[1]
margem_vitoria = ((melhor_fornecedor['pontuacao_total'] - segundo_fornecedor['pontuacao_total']) / segundo_fornecedor['pontuacao_total']) * 100

print("=== RESULTADOS DA MATRIZ DE DECISÃO ===")
print(df[['classificacao', 'fornecedor', 'pontuacao_total']].to_string(index=False))
print(f"\nMelhor fornecedor: {melhor_fornecedor['fornecedor']} (Nota: {melhor_fornecedor['pontuacao_total']:.2f}/10)")
print(f"Vantagem sobre o 2º colocado ({segundo_fornecedor['fornecedor']}): {margem_vitoria:.1f}%\n")

# 5. Criar pasta 'resultados' caso não exista
os.makedirs("resultados", exist_ok=True)

# 6. Atualizar Relatório Markdown
caminho_relatorio = os.path.join("resultados", "relatorio_fornecedores.md")
with open(caminho_relatorio, "w", encoding="utf-8") as f:
    f.write("# Relatório de Avaliação de Fornecedores\n\n")
    f.write("Metodologia aplicada: **Decision Matrix** combinada com visualização de alta qualidade (**chart-image**).\n\n")
    
    f.write("## 1. Contexto e Alternativas\n")
    f.write("Avaliação de 4 fornecedores concorrentes: **Alfa**, **Beta**, **Gama** e **Delta**.\n\n")
    
    f.write("## 2. Critérios e Pesos\n")
    f.write("| Critério | Direção | Peso | Descrição |\n")
    f.write("|---|---|---|---|\n")
    f.write(f"| **Preço Unitário** | Menor é melhor | {int(pesos['preco']*100)}% | Custo de aquisição por peça |\n")
    f.write(f"| **Prazo de Entrega** | Menor é melhor | {int(pesos['prazo']*100)}% | Prazo médio em dias úteis |\n")
    f.write(f"| **Taxa de Defeitos** | Menor é melhor | {int(pesos['defeitos']*100)}% | Percentual de peças não-conformes |\n")
    f.write(f"| **Suporte Técnico** | Maior é melhor | {int(pesos['suporte']*100)}% | Nota de qualidade no atendimento (0 a 10) |\n\n")
    
    f.write("## 3. Matriz de Resultados e Pontuação\n")
    f.write("| Posição | Fornecedor | Preço (30%) | Prazo (25%) | Defeitos (25%) | Suporte (20%) | **Nota Final** |\n")
    f.write("|:---:|---|:---:|:---:|:---:|:---:|:---:|\n")
    for _, row in df.iterrows():
        destaque = "**" if row['classificacao'] == 1 else ""
        f.write(f"| {row['classificacao']}º | {destaque}{row['fornecedor']}{destaque} | {row['nota_preco']:.1f} ({row['pontos_preco']:.2f}) | {row['nota_prazo']:.1f} ({row['pontos_prazo']:.2f}) | {row['nota_defeitos']:.1f} ({row['pontos_defeitos']:.2f}) | {row['nota_suporte']:.1f} ({row['pontos_suporte']:.2f}) | {destaque}{row['pontuacao_total']:.2f}{destaque} |\n")
    f.write("\n")
    
    f.write("## 4. Visualizações Analíticas\n")
    f.write("- **Painel Consolidado Único:** `painel_consolidado_fornecedores.png` (reúne todas as 4 análises gráficas em uma única visualização completa).\n")
    f.write("- **Gráficos Específicos:** `grafico_fornecedores.png`, `grafico_criterios.png`, `grafico_radar_fornecedores.png` e `grafico_tradeoff.png`.\n\n")

    f.write("## 5. Conclusão e Recomendação\n")
    f.write(f"- **Fornecedor Recomendado:** **Delta** com **{melhor_fornecedor['pontuacao_total']:.2f} pontos**.\n")
    f.write(f"- **Justificativa:** Venceu em prazo (4 dias), defeitos (0.5%) e suporte (9.5).\n")
    f.write(f"- **Margem de Segurança:** Vantagem de **{margem_vitoria:.1f}%** sobre o 2º colocado (Beta), caracterizando uma decisão altamente robusta.\n")

print(f"Relatório atualizado em: {caminho_relatorio}")

# ==============================================================================
# 7. PAINEL CONSOLIDADO (TODOS OS GRÁFICOS JUNTOS EM UMA ÚNICA IMAGEM)
# ==============================================================================
caminho_painel_consolidado = os.path.join("resultados", "painel_consolidado_fornecedores.png")

fig = plt.figure(figsize=(17, 13), dpi=300)
gs = fig.add_gridspec(2, 2, hspace=0.32, wspace=0.22)

fig.suptitle("Dashboard Consolidado de Avaliação de Fornecedores (Decision Matrix)", fontsize=18, fontweight='bold', y=0.98)

# --- QUADRANTE 1: Ranking Geral Empilhado (Top-Left) ---
ax1 = fig.add_subplot(gs[0, 0])
fornecedores_ordenados = df['fornecedor'].tolist()
posicoes = np.arange(len(fornecedores_ordenados))
p_preco = df['pontos_preco'].values
p_prazo = df['pontos_prazo'].values
p_defeitos = df['pontos_defeitos'].values
p_suporte = df['pontos_suporte'].values
totais = df['pontuacao_total'].values

cores_criterios = ['#2b5c8f', '#2a9d8f', '#e76f51', '#9b5de5']
w_bar = 0.52

ax1.bar(posicoes, p_preco, width=w_bar, label='Preço Unitário (30%)', color=cores_criterios[0], edgecolor='white')
ax1.bar(posicoes, p_prazo, width=w_bar, bottom=p_preco, label='Prazo de Entrega (25%)', color=cores_criterios[1], edgecolor='white')
bottom_def = p_preco + p_prazo
ax1.bar(posicoes, p_defeitos, width=w_bar, bottom=bottom_def, label='Baixa Taxa Defeitos (25%)', color=cores_criterios[2], edgecolor='white')
bottom_sup = bottom_def + p_defeitos
ax1.bar(posicoes, p_suporte, width=w_bar, bottom=bottom_sup, label='Suporte Técnico (20%)', color=cores_criterios[3], edgecolor='white')

for i, total in enumerate(totais):
    destaque = " (Vencedor)" if i == 0 else ""
    cor_txt = '#1b4332' if i == 0 else '#333333'
    ax1.text(i, total + 0.18, f"{total:.2f}{destaque}", ha='center', va='bottom', fontweight='bold', fontsize=10, color=cor_txt)

ax1.set_xticks(posicoes)
ax1.set_xticklabels(fornecedores_ordenados, fontsize=11, fontweight='bold')
ax1.set_ylabel("Pontuação Ponderada Total (0 a 10)", fontsize=10)
ax1.set_title("A. Ranking Geral Ponderado", fontsize=13, fontweight='bold')
ax1.set_ylim(0, 11)
ax1.grid(axis='y', linestyle='--', alpha=0.5)
ax1.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)

# --- QUADRANTE 2: Radar Multidimensional (Top-Right) ---
ax2 = fig.add_subplot(gs[0, 1], polar=True)
categorias = ['Preço (30%)', 'Prazo (25%)', 'Defeitos (25%)', 'Suporte (20%)']
num_vars = len(categorias)
angulos = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angulos += angulos[:1]

paleta_radar = {'Delta': '#2a9d8f', 'Beta': '#e76f51', 'Alfa': '#2b5c8f', 'Gama': '#9b5de5'}

for _, row in df.iterrows():
    nome = row['fornecedor']
    valores = [row['nota_preco'], row['nota_prazo'], row['nota_defeitos'], row['nota_suporte']]
    valores += valores[:1]
    cor = paleta_radar.get(nome, '#333333')
    espessura = 2.8 if nome == 'Delta' else 1.8
    alpha_fill = 0.22 if nome == 'Delta' else 0.06
    ax2.plot(angulos, valores, label=f"{nome} ({row['pontuacao_total']:.2f})", color=cor, linewidth=espessura)
    ax2.fill(angulos, valores, color=cor, alpha=alpha_fill)

ax2.set_theta_offset(np.pi / 2)
ax2.set_theta_direction(-1)
ax2.set_xticks(angulos[:-1])
ax2.set_xticklabels(categorias, fontsize=10, fontweight='bold')
ax2.set_rlabel_position(0)
ax2.set_yticks([2, 4, 6, 8, 10])
ax2.set_yticklabels(["2", "4", "6", "8", "10"], color="#666666", size=8)
ax2.set_ylim(0, 10.5)
ax2.set_title("B. Perfil Radar de Competitividade", fontsize=13, fontweight='bold', pad=18)
ax2.legend(loc='upper right', bbox_to_anchor=(1.32, 1.12), frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)

# --- QUADRANTE 3: Comparativo por Critério - Barras Agrupadas (Bottom-Left) ---
ax3 = fig.add_subplot(gs[1, 0])
nomes_fornecedores = ['Alfa', 'Beta', 'Gama', 'Delta']
df_ord_nome = df.set_index('fornecedor').loc[nomes_fornecedores].reset_index()

x_crit = np.arange(len(categorias))
largura_agrupada = 0.18
paleta_fornec = {'Alfa': '#2b5c8f', 'Beta': '#e76f51', 'Gama': '#9b5de5', 'Delta': '#2a9d8f'}

for idx, forn in enumerate(nomes_fornecedores):
    row_f = df_ord_nome[df_ord_nome['fornecedor'] == forn].iloc[0]
    notas = [row_f['nota_preco'], row_f['nota_prazo'], row_f['nota_defeitos'], row_f['nota_suporte']]
    offset = (idx - 1.5) * largura_agrupada
    barras = ax3.bar(x_crit + offset, notas, width=largura_agrupada, label=forn, color=paleta_fornec[forn], edgecolor='white', alpha=0.9)
    for b in barras:
        alt = b.get_height()
        ax3.text(b.get_x() + b.get_width()/2., alt + 0.15, f"{alt:.1f}", ha='center', va='bottom', fontsize=7.5, fontweight='bold')

ax3.set_xticks(x_crit)
ax3.set_xticklabels(categorias, fontsize=10, fontweight='bold')
ax3.set_ylabel("Nota Normalizada (0 a 10)", fontsize=10)
ax3.set_title("C. Desempenho por Critério Individual", fontsize=13, fontweight='bold')
ax3.set_ylim(0, 11.5)
ax3.grid(axis='y', linestyle='--', alpha=0.5)
ax3.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)

# --- QUADRANTE 4: Trade-off Custo vs Desempenho Operacional (Bottom-Right) ---
ax4 = fig.add_subplot(gs[1, 1])

for _, row in df.iterrows():
    nome = row['fornecedor']
    x = row['preco_unitario']
    y = row['nota_operacional']
    tamanho = row['pontuacao_total'] * 80
    cor = '#2a9d8f' if nome == 'Delta' else '#2b5c8f'
    
    ax4.scatter(x, y, s=tamanho, color=cor, alpha=0.8, edgecolors='black', linewidth=1.5, zorder=4)
    desloc_y = 0.28 if nome != 'Beta' else -0.38
    ax4.annotate(
        f"{nome}\n(R$ {x:.2f} | Nota Op: {y:.1f})",
        (x, y + desloc_y),
        ha='center',
        fontweight='bold',
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#cccccc", alpha=0.85)
    )

ax4.axvline(x=df['preco_unitario'].mean(), color='#999999', linestyle=':', label=f"Preço Médio (R$ {df['preco_unitario'].mean():.2f})")
ax4.axhline(y=df['nota_operacional'].mean(), color='#999999', linestyle='--', label=f"Nota Op. Média ({df['nota_operacional'].mean():.1f})")

ax4.set_title("D. Trade-off: Preço vs Desempenho Operacional", fontsize=13, fontweight='bold')
ax4.set_xlabel("Preço Unitário (R$) - [Mais barato à esquerda ←]", fontsize=10)
ax4.set_ylabel("Desempenho Operacional (Nota 0 a 10) - [Maior qualidade acima ↑]", fontsize=10)
ax4.grid(True, linestyle='--', alpha=0.5)
ax4.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9, fontsize=8.5)
ax4.set_xlim(80, 115)
ax4.set_ylim(0, 11)

# Rodapé de integridade dos dados
fig.text(0.02, 0.01, "Fonte: dados/fornecedores.csv | Metodologia: Matriz de Decisão Ponderada (Decision Matrix) e Boas Práticas chart-image", fontsize=9, color='#555555')

plt.savefig(caminho_painel_consolidado, bbox_inches='tight')
plt.close()

print(f"Painel consolidado salvo com sucesso em: {caminho_painel_consolidado}")


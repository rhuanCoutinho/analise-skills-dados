import os
import sys
import matplotlib.pyplot as plt

# Ajuste de codificação para o terminal do Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 1. Pontos de calibração fornecidos: (temperatura em °C, corrente em mA)
# Ponto 1: (0°C, 4 mA)
# Ponto 2: (100°C, 20 mA)
x1, y1 = 0, 4
x2, y2 = 100, 20

# 2. Cálculo dos coeficientes da reta: y = ax + b
# 'a' é a inclinação (taxa de variação de mA por °C)
a = (y2 - y1) / (x2 - x1)

# 'b' é o valor de y quando x = 0 (intercepto)
b = y1 - a * x1

print("=== PARÂMETROS DA EQUAÇÃO ===")
print(f"Coeficiente a: {a}")
print(f"Coeficiente b: {b}")
print(f"Equação: y = {a} * x + {b}\n")

# 3. Cálculo para x = 50 graus
x_teste = 50
y_resultado = a * x_teste + b

print(f"=== RESULTADO PARA {x_teste}°C ===")
print(f"Para x = {x_teste}°C, a corrente calculada é y = {y_resultado:.2f} mA\n")

# 4. Avisos de limites
print("=== VERIFICAÇÃO DE LIMITES ===")
# Alerta para temperatura fora de 0 a 100 °C
if x_teste < 0 or x_teste > 100:
    print(f"[AVISO] A temperatura ({x_teste}°C) está fora do limite permitido (0 a 100°C)!")
else:
    print(f"[OK] Temperatura ({x_teste}°C) dentro do limite (0 a 100°C).")

# Alerta para corrente fora de 4 a 20 mA
if y_resultado < 4 or y_resultado > 20:
    print(f"[AVISO] A corrente ({y_resultado:.2f} mA) está fora do limite permitido (4 a 20 mA)!")
else:
    print(f"[OK] Corrente ({y_resultado:.2f} mA) dentro do limite (4 a 20 mA).\n")

# 5. Classificação da temperatura
# - Baixa: até 30 graus
# - Média: de 31 a 60 graus
# - Alta: acima de 60 graus
print("=== CLASSIFICAÇÃO DA TEMPERATURA ===")
if x_teste <= 30:
    classificacao = "Baixa (até 30°C)"
elif x_teste <= 60:
    classificacao = "Média (de 31°C a 60°C)"
else:
    classificacao = "Alta (acima de 60°C)"

print(f"Classificação para {x_teste}°C: {classificacao}\n")

# 6. Gerando o gráfico com matplotlib
# Garante que a pasta resultados exista
os.makedirs("resultados", exist_ok=True)

# Pontos de temperatura para montar a linha no gráfico
temperaturas = [0, 20, 40, 60, 80, 100]
correntes = [a * temp + b for temp in temperaturas]

plt.figure(figsize=(8, 5))
plt.plot(temperaturas, correntes, label="Curva de Resposta (y = ax + b)", color="blue", marker="o")
plt.scatter([x_teste], [y_resultado], color="red", zorder=5, label=f"Ponto Atual ({x_teste}°C, {y_resultado:.1f} mA)")

plt.title("Relação entre Temperatura e Corrente Elétrica")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Corrente Elétrica (mA)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()

# Salva a imagem na pasta resultados/
caminho_grafico = os.path.join("resultados", "grafico_termometro.png")
plt.savefig(caminho_grafico, dpi=300, bbox_inches="tight")
print(f"Gráfico salvo com sucesso em: {caminho_grafico}")

# Fechamento do gráfico após salvar
plt.close()

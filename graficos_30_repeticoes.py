import matplotlib.pyplot as plt
import numpy as np
import os

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Criar pasta para salvar gráficos
os.makedirs('graficos_30rep', exist_ok=True)

# Dados das 30 repetições
cenarios = ['Leve\n(50 users)', 'Moderado\n(100 users)', 'Pico\n(200 users)']
usuarios = [50, 100, 200]
tempo_medio = [788.56, 337.41, 256.13]
tempo_max = [9407.83, 10105.49, 10113.20]
throughput = [17.90, 41.14, 81.18]
taxa_sucesso = [18.03, 1.47, 0.86]
total_requisicoes = [10384, 24619, 24269]
total_falhas = [8746, 24258, 24061]

print("Gerando gráficos das 30 repetições...")

# ====================================================================
# GRÁFICO 1: Tempos de Resposta (Médio e Máximo)
# ====================================================================
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(cenarios))
width = 0.35

bars1 = ax.bar(x - width/2, tempo_medio, width, label='Tempo Médio', 
               color='#2E86AB', alpha=0.8, edgecolor='black', linewidth=1.2)
bars2 = ax.bar(x + width/2, tempo_max, width, label='Tempo Máximo', 
               color='#A23B72', alpha=0.8, edgecolor='black', linewidth=1.2)

ax.set_xlabel('Cenário de Teste', fontweight='bold')
ax.set_ylabel('Tempo de Resposta (ms)', fontweight='bold')
ax.set_title('Tempos de Resposta - Média de 30 Repetições', fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(cenarios)
ax.legend(loc='upper right', fontsize=11)
ax.grid(axis='y', alpha=0.3)

# Adicionar valores nas barras
for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}',
            ha='center', va='bottom', fontweight='bold', fontsize=9)

for bar in bars2:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.0f}',
            ha='center', va='bottom', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('graficos_30rep/tempos_resposta_30rep.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico 1 salvo: tempos_resposta_30rep.png")
plt.close()

# ====================================================================
# GRÁFICO 2: Throughput (Requisições por Segundo)
# ====================================================================
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(cenarios, throughput, color=['#06A77D', '#F77F00', '#D62828'], 
              alpha=0.8, edgecolor='black', linewidth=1.2)

ax.set_xlabel('Cenário de Teste', fontweight='bold')
ax.set_ylabel('Requisições por Segundo (req/s)', fontweight='bold')
ax.set_title('Throughput do Sistema - Média de 30 Repetições', fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3)

# Adicionar valores nas barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f}',
            ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('graficos_30rep/throughput_30rep.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico 2 salvo: throughput_30rep.png")
plt.close()

# ====================================================================
# GRÁFICO 3: Taxa de Sucesso
# ====================================================================
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(cenarios, taxa_sucesso, color=['#E63946', '#F77F00', '#06A77D'], 
              alpha=0.8, edgecolor='black', linewidth=1.2)

ax.set_xlabel('Cenário de Teste', fontweight='bold')
ax.set_ylabel('Taxa de Sucesso (%)', fontweight='bold')
ax.set_title('Taxa de Sucesso das Requisições - Média de 30 Repetições', fontweight='bold', pad=20)
ax.set_ylim(0, 100)
ax.grid(axis='y', alpha=0.3)

# Linha de referência em 100%
ax.axhline(y=100, color='green', linestyle='--', linewidth=2, alpha=0.5, label='100% Sucesso')
ax.legend(loc='upper right')

# Adicionar valores nas barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.2f}%',
            ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('graficos_30rep/taxa_sucesso_30rep.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico 3 salvo: taxa_sucesso_30rep.png")
plt.close()

# ====================================================================
# GRÁFICO 4: Requisições vs Falhas
# ====================================================================
fig, ax = plt.subplots(figsize=(10, 6))

x = np.arange(len(cenarios))
width = 0.35

bars1 = ax.bar(x - width/2, total_requisicoes, width, label='Total de Requisições', 
               color='#4A90E2', alpha=0.8, edgecolor='black', linewidth=1.2)
bars2 = ax.bar(x + width/2, total_falhas, width, label='Total de Falhas', 
               color='#E74C3C', alpha=0.8, edgecolor='black', linewidth=1.2)

ax.set_xlabel('Cenário de Teste', fontweight='bold')
ax.set_ylabel('Quantidade', fontweight='bold')
ax.set_title('Total de Requisições vs Falhas - Média de 30 Repetições', fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(cenarios)
ax.legend(loc='upper left', fontsize=11)
ax.grid(axis='y', alpha=0.3)

# Adicionar valores nas barras
for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}',
            ha='center', va='bottom', fontweight='bold', fontsize=9)

for bar in bars2:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}',
            ha='center', va='bottom', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('graficos_30rep/requisicoes_falhas_30rep.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico 4 salvo: requisicoes_falhas_30rep.png")
plt.close()

# ====================================================================
# GRÁFICO 5: Eficiência (Throughput por Usuário)
# ====================================================================
fig, ax = plt.subplots(figsize=(10, 6))

eficiencia = [throughput[i]/usuarios[i] for i in range(len(usuarios))]

bars = ax.bar(cenarios, eficiencia, color=['#9B59B6', '#3498DB', '#E67E22'], 
              alpha=0.8, edgecolor='black', linewidth=1.2)

ax.set_xlabel('Cenário de Teste', fontweight='bold')
ax.set_ylabel('Requisições por Segundo por Usuário', fontweight='bold')
ax.set_title('Eficiência do Sistema - Média de 30 Repetições', fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3)

# Adicionar valores nas barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.3f}',
            ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('graficos_30rep/eficiencia_30rep.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico 5 salvo: eficiencia_30rep.png")
plt.close()

# ====================================================================
# GRÁFICO 6: Comparação de Escalabilidade (Usuários vs Throughput)
# ====================================================================
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(usuarios, throughput, marker='o', linewidth=3, markersize=12, 
        color='#E74C3C', label='Throughput Real', markeredgecolor='black', markeredgewidth=2)

# Linha de escalabilidade ideal (linear)
throughput_ideal = [throughput[0] * (u/usuarios[0]) for u in usuarios]
ax.plot(usuarios, throughput_ideal, linestyle='--', linewidth=2, 
        color='#2ECC71', alpha=0.7, label='Throughput Ideal (Linear)')

ax.set_xlabel('Número de Usuários', fontweight='bold')
ax.set_ylabel('Throughput (req/s)', fontweight='bold')
ax.set_title('Escalabilidade do Sistema - Média de 30 Repetições', fontweight='bold', pad=20)
ax.legend(loc='upper left', fontsize=11)
ax.grid(True, alpha=0.3)

# Adicionar valores nos pontos
for i, (u, t) in enumerate(zip(usuarios, throughput)):
    ax.annotate(f'{t:.2f} req/s', 
                xy=(u, t), 
                xytext=(10, 10), 
                textcoords='offset points',
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

plt.tight_layout()
plt.savefig('graficos_30rep/escalabilidade_30rep.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico 6 salvo: escalabilidade_30rep.png")
plt.close()

print("\n" + "="*60)
print("TODOS OS GRÁFICOS FORAM GERADOS COM SUCESSO!")
print("="*60)
print(f"Local: graficos_30rep/")
print("\nArquivos gerados:")
print("  1. tempos_resposta_30rep.png")
print("  2. throughput_30rep.png")
print("  3. taxa_sucesso_30rep.png")
print("  4. requisicoes_falhas_30rep.png")
print("  5. eficiencia_30rep.png")
print("  6. escalabilidade_30rep.png")

import pandas as pd
import glob
import os
from pathlib import Path

def processar_resultados_locust():
    """
    Processa os CSVs gerados pelo Locust e calcula as médias das 30 repetições.
    """
    
    print("="*60)
    print("PROCESSADOR DE RESULTADOS - LOCUST PETCLINIC")
    print("="*60)
    
    # Dicionário para armazenar resultados
    resultados = {
        'leve': [],
        'moderado': [],
        'pico': []
    }
    
    # Processar cada tipo de cenário
    for cenario in ['leve', 'moderado', 'pico']:
        print(f"\n📊 Processando cenário: {cenario.upper()}")
        
        # Buscar todos os arquivos CSV do cenário
        pattern = f"results/{cenario}_*_stats.csv"
        arquivos = glob.glob(pattern)
        
        if not arquivos:
            print(f"⚠ Nenhum arquivo encontrado para o padrão: {pattern}")
            continue
        
        print(f"✓ {len(arquivos)} execuções encontradas")
        
        # Processar cada arquivo
        for arquivo in arquivos:
            try:
                df = pd.read_csv(arquivo)
                
                # Filtrar apenas a linha "Aggregated" (resumo total)
                agregado = df[df['Name'] == 'Aggregated']
                
                if not agregado.empty:
                    resultado = {
                        'cenario': cenario,
                        'tempo_medio_ms': agregado['Average Response Time'].values[0],
                        'tempo_max_ms': agregado['Max Response Time'].values[0],
                        'req_por_segundo': agregado['Requests/s'].values[0],
                        'total_requisicoes': agregado['Request Count'].values[0],
                        'total_falhas': agregado['Failure Count'].values[0],
                        'percentual_sucesso': (1 - agregado['Failure Count'].values[0] / 
                                              agregado['Request Count'].values[0]) * 100
                    }
                    resultados[cenario].append(resultado)
                    
            except Exception as e:
                print(f"✗ Erro ao processar {arquivo}: {e}")
    
    # Calcular médias e gerar relatório
    print("\n" + "="*60)
    print("RESULTADOS MÉDIOS (30 REPETIÇÕES)")
    print("="*60)
    
    resumo_final = []
    
    for cenario in ['leve', 'moderado', 'pico']:
        if not resultados[cenario]:
            print(f"\n⚠ Sem dados para cenário {cenario}")
            continue
        
        df_cenario = pd.DataFrame(resultados[cenario])
        
        media = {
            'Cenário': cenario.upper(),
            'Usuários': {'leve': 50, 'moderado': 100, 'pico': 200}[cenario],
            'Tempo Médio (ms)': df_cenario['tempo_medio_ms'].mean(),
            'Tempo Máximo (ms)': df_cenario['tempo_max_ms'].mean(),
            'Req/s': df_cenario['req_por_segundo'].mean(),
            'Total Requisições': df_cenario['total_requisicoes'].mean(),
            'Total Falhas': df_cenario['total_falhas'].mean(),
            '% Sucesso': df_cenario['percentual_sucesso'].mean()
        }
        
        resumo_final.append(media)
        
        # Imprimir resultados do cenário
        print(f"\n{'─'*60}")
        print(f"CENÁRIO {cenario.upper()}")
        print(f"{'─'*60}")
        print(f"Usuários Virtuais: {media['Usuários']}")
        print(f"Tempo Médio de Resposta: {media['Tempo Médio (ms)']:.2f} ms")
        print(f"Tempo Máximo de Resposta: {media['Tempo Máximo (ms)']:.2f} ms")
        print(f"Requisições por Segundo: {media['Req/s']:.2f} req/s")
        print(f"Total de Requisições: {media['Total Requisições']:.0f}")
        print(f"Total de Falhas: {media['Total Falhas']:.0f}")
        print(f"Taxa de Sucesso: {media['% Sucesso']:.2f}%")
    
    # Salvar resumo em CSV
    if resumo_final:
        df_resumo = pd.DataFrame(resumo_final)
        arquivo_saida = "results/resumo_final.csv"
        df_resumo.to_csv(arquivo_saida, index=False)
        print(f"\n✓ Resumo salvo em: {arquivo_saida}")
        
        # Criar análise comparativa
        print("\n" + "="*60)
        print("ANÁLISE COMPARATIVA")
        print("="*60)
        
        if len(resumo_final) >= 2:
            # Comparar leve vs moderado
            if len(resumo_final) >= 2:
                leve = resumo_final[0]
                moderado = resumo_final[1]
                
                aumento_tempo = ((moderado['Tempo Médio (ms)'] - leve['Tempo Médio (ms)']) / 
                                leve['Tempo Médio (ms)'] * 100)
                aumento_req = ((moderado['Req/s'] - leve['Req/s']) / 
                              leve['Req/s'] * 100)
                
                print(f"\n📈 LEVE → MODERADO (50 → 100 usuários):")
                print(f"   • Tempo médio aumentou: {aumento_tempo:+.1f}%")
                print(f"   • Throughput aumentou: {aumento_req:+.1f}%")
            
            # Comparar moderado vs pico
            if len(resumo_final) >= 3:
                moderado = resumo_final[1]
                pico = resumo_final[2]
                
                aumento_tempo = ((pico['Tempo Médio (ms)'] - moderado['Tempo Médio (ms)']) / 
                                moderado['Tempo Médio (ms)'] * 100)
                queda_sucesso = moderado['% Sucesso'] - pico['% Sucesso']
                
                print(f"\n📈 MODERADO → PICO (100 → 200 usuários):")
                print(f"   • Tempo médio aumentou: {aumento_tempo:+.1f}%")
                print(f"   • Taxa de sucesso variou: {queda_sucesso:+.2f}%")
        
        # Gerar tabela formatada para o artigo
        print("\n" + "="*60)
        print("TABELA PARA O ARTIGO (copie para o LaTeX)")
        print("="*60)
        print("\n\\begin{table}[h]")
        print("\\centering")
        print("\\caption{Resultados Médios dos Testes de Carga}")
        print("\\begin{tabular}{|l|c|c|c|}")
        print("\\hline")
        print("\\textbf{Métrica} & \\textbf{Leve} & \\textbf{Moderado} & \\textbf{Pico} \\\\")
        print("\\hline")
        
        if len(resumo_final) >= 3:
            print(f"Usuários & {resumo_final[0]['Usuários']} & {resumo_final[1]['Usuários']} & {resumo_final[2]['Usuários']} \\\\")
            print(f"Tempo Médio (ms) & {resumo_final[0]['Tempo Médio (ms)']:.2f} & {resumo_final[1]['Tempo Médio (ms)']:.2f} & {resumo_final[2]['Tempo Médio (ms)']:.2f} \\\\")
            print(f"Req/s & {resumo_final[0]['Req/s']:.2f} & {resumo_final[1]['Req/s']:.2f} & {resumo_final[2]['Req/s']:.2f} \\\\")
            print(f"Taxa Sucesso (\\%) & {resumo_final[0]['% Sucesso']:.2f} & {resumo_final[1]['% Sucesso']:.2f} & {resumo_final[2]['% Sucesso']:.2f} \\\\")
        
        print("\\hline")
        print("\\end{tabular}")
        print("\\end{table}\n")
    
    print("\n" + "="*60)
    print("PROCESSAMENTO CONCLUÍDO!")
    print("="*60)

if __name__ == "__main__":
    # Verificar se o pandas está instalado
    try:
        import pandas as pd
    except ImportError:
        print("❌ ERRO: Pandas não está instalado!")
        print("Execute: pip install pandas")
        exit(1)
    
    # Verificar se a pasta results existe
    if not os.path.exists('results'):
        print("❌ ERRO: Pasta 'results' não encontrada!")
        print("Certifique-se de estar na pasta SD_07 e que a pasta results existe.")
        exit(1)
    
    # Processar resultados
    processar_resultados_locust()
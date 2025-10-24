# Avaliação de Desempenho do Spring PetClinic Microservices com Locust

Trabalho acadêmico de medição e análise de desempenho do Spring PetClinic (versão microservices) usando Apache Locust.

## 📋 Objetivo

Medir e relatar o desempenho básico do Spring PetClinic executando 3 cenários de carga (leve, moderado e pico) com 30 repetições cada, analisando tempo de resposta, throughput, taxa de sucesso e falhas.

## 🎯 Sistema Testado

**Spring PetClinic Microservices** - Arquitetura de microsserviços com:
- API Gateway
- Customers Service
- Vets Service  
- Visits Service

Repositório: https://github.com/spring-petclinic/spring-petclinic-microservices

## 📊 Plano de Teste (Mix de Requisições)

- **40%** - `GET /api/customer/owners` - Lista proprietários
- **30%** - `GET /api/customer/owners/{id}` - Busca proprietário específico
- **20%** - `GET /api/vet/vets` - Lista veterinários
- **10%** - `POST /api/customer/owners` - Cadastra novo proprietário

## 🔧 Pré-requisitos

- Docker Desktop 4.0+
- Python 3.9+
- Git

## 📦 Instalação Rápida

```powershell
# Clonar repositório
git clone https://github.com/simao-morais/SD_07.git
cd trabalho7

# Clonar Spring PetClinic
git clone https://github.com/spring-petclinic/spring-petclinic-microservices

# Instalar dependências Python
pip install locust pandas matplotlib numpy

```

## 🚀 Execução (Passo a Passo)

### 1. Subir o Sistema

```powershell
cd spring-petclinic-microservices
docker-compose up -d
```

Aguarde 3-5 minutos para inicialização completa. Verifique em: http://localhost:8080

### 2. Popular Banco de Dados

Via interface web (http://localhost:8080):
- Acesse "Owners" > "Register"  
- Cadastre 10-15 proprietários com pets

### 3. Executar Testes

```powershell
cd ..

# Executar cenário individual
.\run_leve.bat        # 50 usuários, 10 min
.\run_moderado.bat    # 100 usuários, 10 min  
.\run_pico.bat        # 200 usuários, 5 min

# OU executar todas as 30 repetições (12-15 horas)
.\executar_todos.bat
```

### 4. Processar Resultados

```powershell
python processar_resultados.py
```

Gera:
- `results/resumo_final.csv` - Dados consolidados
- Tabelas LaTeX para o artigo
- Relatório no terminal

## 📊 Cenários de Teste

| Cenário | Usuários | Duração | Warm-up | Repetições |
|---------|----------|---------|---------|------------|
| **Leve** | 50 | 10 min | 1 min | 30 |
| **Moderado** | 100 | 10 min | 1 min | 30 |
| **Pico** | 200 | 5 min | 30 s | 30 |

## 📈 Métricas Coletadas

1. **Tempo médio de resposta (ms)** - Latência média
2. **Tempo máximo de resposta (ms)** - Pior caso
3. **Requisições por segundo (req/s)** - Throughput
4. **Total de requisições** - Volume processado
5. **Total de falhas** - Erros 4xx e 5xx
6. **Taxa de sucesso (%)** - % de requisições bem-sucedidas

### Arquivos Gerados

Cada execução produz 3 CSVs na pasta `results/`:
- `{cenario}_{num}_stats.csv` - Estatísticas agregadas
- `{cenario}_{num}_stats_history.csv` - Histórico temporal  
- `{cenario}_{num}_failures.csv` - Detalhes de erros (se houver)
- `{cenario}_{num}_exceptions.csv` - Exceções (se houver)

## 📁 Estrutura do Repositório

```
_trabalho7/
├── locustfile.py              # Script Locust com mix de requisições
├── processar_resultados.py    # Processa e calcula médias das 30 repetições
├── graficos_30_repeticoes.py  # Gera gráficos de análise
├── run_leve.bat               # Executa cenário leve
├── run_moderado.bat           # Executa cenário moderado
├── run_pico.bat               # Executa cenário pico
├── executar_todos.bat         # Executa 90 testes (30×3)
├── results/                   # CSVs de resultados
├── graficos_30rep/            # Gráficos gerados
└── spring-petclinic-microservices/  # Sistema testado
```

## 🛠️ Troubleshooting

**Docker não inicia:**
```powershell
docker-compose down
docker-compose up -d --build
```

**Porta 8080 ocupada:**
```powershell
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

**Erros de conexão (5xx):**
- Aumente recursos do Docker (Settings > Resources > Memory: 6GB+)
- Verifique logs: `docker-compose logs -f`

**Monitorar recursos:**
```powershell
docker stats  # CPU e memória em tempo real
```

## 📝 Entregáveis

✅ **Repositório com:**
- `locustfile.py` com mix de requisições  
- Scripts de execução (`.bat`)
- Pasta `results/` com CSVs e tabela resumo
- README.md (este arquivo)

✅ **Vídeo** demonstrando:
- Sistema funcionando
- Execução de teste
- Monitoramento de recursos

✅ **Artigo IEEE (6 páginas)** contendo:
- Resumo e principais números
- Descrição do sistema e endpoints
- Metodologia (cenários A/B/C)
- Resultados (tabelas e gráficos)
- Conclusões e limitações

## 📚 Referências

- [Spring PetClinic Microservices](https://github.com/spring-petclinic/spring-petclinic-microservices)
- [Documentação Locust](https://docs.locust.io/)

## 👥 Autores

- **Pedro Tércio**
- **Robson Santos**
- **Simão Morais** 

**Disciplina:** Sistemas Distribuídos  
**Instituição:** UFPI  
**Período:** 2025.2

---

**Última atualização:** Outubro 2025
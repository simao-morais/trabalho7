# Avaliação de Desempenho do Spring PetClinic com Locust

Trabalho acadêmico de avaliação de desempenho do sistema Spring PetClinic (versão microservices) utilizando a ferramenta Locust para testes de carga.

## 📋 Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar](#como-executar)
- [Cenários de Teste](#cenários-de-teste)
- [Processamento dos Resultados](#processamento-dos-resultados)
- [Métricas Coletadas](#métricas-coletadas)
- [Troubleshooting](#troubleshooting)
- [Autores](#autores)

---

## 🎯 Sobre o Projeto

Este projeto realiza testes de carga automatizados no sistema **Spring PetClinic Microservices** para avaliar seu desempenho sob diferentes níveis de carga. São executados 3 cenários (leve, moderado e pico) com 30 repetições cada, totalizando 90 execuções.

### Endpoints Testados

O teste simula usuários reais acessando os seguintes endpoints com a distribuição especificada:

- **40%** - `GET /api/customer/owners` - Lista de donos
- **30%** - `GET /api/customer/owners/{id}` - Busca de dono específico
- **20%** - `GET /api/vet/vets` - Lista de veterinários
- **10%** - `POST /api/customer/owners` - Criação de novo dono

---

## 🔧 Pré-requisitos

### Software Necessário

- **Docker Desktop** (versão 4.0+)
  - Download: https://www.docker.com/products/docker-desktop
- **Python** (versão 3.9 ou superior)
  - Download: https://www.python.org/downloads/
- **Git**
  - Download: https://git-scm.com/downloads

### Verificar Instalações

Abra o PowerShell ou CMD e execute:

```powershell
docker --version
python --version
git --version
```

---

## 📦 Instalação

### 1. Clonar este Repositório

```powershell
git clone https://github.com/simao-morais/trabalho7.git
cd trabalho7
```

### 2. Clonar o Spring PetClinic Microservices

```powershell
git clone https://github.com/spring-petclinic/spring-petclinic-microservices
```

### 3. Instalar Dependências Python

```powershell
pip install locust pandas matplotlib
```

Ou usando o arquivo requirements.txt:

```powershell
pip install -r requirements.txt
```

### 4. Criar Pasta de Resultados

```powershell
mkdir results
```

---

## 📁 Estrutura do Projeto

```
trabalho7/
├── spring-petclinic-microservices/    # Sistema a ser testado
│   ├── docker-compose.yml
│   └── ...
│
├── locustfile.py                       # Script de teste Locust
├── processar_resultados.py             # Script de análise dos resultados
│
├── run_leve.bat                        # Executa cenário leve (50 usuários)
├── run_moderado.bat                    # Executa cenário moderado (100 usuários)
├── run_pico.bat                        # Executa cenário pico (200 usuários)
├── executar_todos.bat                  # Executa todas as 30 repetições
│
├── results/                            # Pasta para armazenar CSVs
│   ├── leve_1_stats.csv
│   ├── leve_1_stats_history.csv
│   ├── ...
│   └── resumo_final.csv               # Gerado após processamento
│
├── README.md                           # Este arquivo
└── requirements.txt                    # Dependências Python
```

---

## 🚀 Como Executar

### Passo 1: Subir o Spring PetClinic

Navegue até a pasta do PetClinic e inicie os containers:

```powershell
cd spring-petclinic-microservices
docker-compose up -d
```

**Aguarde 3-5 minutos** para todos os serviços iniciarem completamente.

### Passo 2: Verificar se Está Funcionando

Abra o navegador e acesse:
- http://localhost:8080 (Interface Web)
- http://localhost:8080/api/customer/owners (API de Owners)
- http://localhost:8080/api/vet/vets (API de Vets)

Você também pode verificar os logs:

```powershell
docker-compose logs -f
```

Para ver status dos containers:

```powershell
docker-compose ps
```

### Passo 3: Popular o Banco de Dados

**Opção A - Via Interface Web:**
1. Acesse http://localhost:8080
2. Vá em "Owners" > "Register"
3. Adicione pelo menos 10-15 donos manualmente

**Opção B - Via Script Python:**

```powershell
cd ..
python popular_banco.py
```

### Passo 4: Executar os Testes

Volte para a pasta raiz do projeto:

```powershell
cd trabalho7
```

#### Opção A: Executar Cenários Individualmente

```powershell
# Cenário Leve (50 usuários, 10 minutos)
run_leve.bat

# Cenário Moderado (100 usuários, 10 minutos)
run_moderado.bat

# Cenário Pico (200 usuários, 5 minutos)
run_pico.bat
```

#### Opção B: Executar Todas as 30 Repetições Automaticamente

```powershell
executar_todos.bat
```

**⚠️ ATENÇÃO:** As 30 repetições levam aproximadamente:
- Cenário Leve: 30 × 10 min = ~5 horas
- Cenário Moderado: 30 × 10 min = ~5 horas
- Cenário Pico: 30 × 5 min = ~2.5 horas
- **TOTAL: ~12-15 horas** (considerando intervalos entre execuções)

**Recomendação:** Execute durante a noite ou em dias separados.

### Passo 5: Processar os Resultados

Após todas as execuções terminarem:

```powershell
python processar_resultados.py
```

Este script irá:
- Ler todos os CSVs da pasta `results/`
- Calcular as médias das 30 repetições
- Gerar relatório completo no terminal
- Criar `results/resumo_final.csv` com os dados consolidados
- Gerar tabela formatada em LaTeX para o artigo

---

## 📊 Cenários de Teste

### Cenário A - Leve
- **Usuários:** 50 simultâneos
- **Duração:** 10 minutos
- **Warm-up:** 1 minuto (descartado)
- **Spawn Rate:** 5 usuários/segundo
- **Repetições:** 30

### Cenário B - Moderado
- **Usuários:** 100 simultâneos
- **Duração:** 10 minutos
- **Warm-up:** 1 minuto (descartado)
- **Spawn Rate:** 10 usuários/segundo
- **Repetições:** 30

### Cenário C - Pico
- **Usuários:** 200 simultâneos
- **Duração:** 5 minutos
- **Warm-up:** 30 segundos (descartado)
- **Spawn Rate:** 20 usuários/segundo
- **Repetições:** 30

---

## 📈 Métricas Coletadas

Para cada cenário, são coletadas as seguintes métricas:

1. **Tempo Médio de Resposta (ms)** - Latência média das requisições
2. **Tempo Máximo de Resposta (ms)** - Pior caso observado
3. **Requisições por Segundo (req/s)** - Throughput do sistema
4. **Total de Requisições** - Volume total processado
5. **Total de Falhas** - Quantidade de erros (4xx, 5xx)
6. **Taxa de Sucesso (%)** - Percentual de requisições bem-sucedidas

### Arquivos Gerados por Execução

Cada execução gera 3 arquivos CSV:

- `{cenario}_{numero}_stats.csv` - Estatísticas agregadas
- `{cenario}_{numero}_stats_history.csv` - Histórico temporal
- `{cenario}_{numero}_failures.csv` - Detalhes dos erros (se houver)

---

## 🔍 Monitoramento Durante os Testes

### Monitorar Uso de Recursos dos Containers

Em outro terminal, execute:

```powershell
docker stats
```

Isso mostrará CPU, memória e I/O em tempo real.

### Visualizar Interface do Locust (Opcional)

Para acompanhar graficamente (em vez de headless):

```powershell
locust -f locustfile.py --host=http://localhost:8080
```

Depois acesse: http://localhost:8089

---

## 🛠️ Troubleshooting

### Problema: Docker não inicia os containers

**Solução:**
```powershell
docker-compose down
docker-compose up -d --build
```

### Problema: Porta 8080 já está em uso

**Solução:**
```powershell
# Identifique o processo
netstat -ano | findstr :8080

# Mate o processo (substitua <PID> pelo número encontrado)
taskkill /PID <PID> /F
```

### Problema: Locust não encontra o host

**Solução:**
- Verifique se o PetClinic está rodando: `docker-compose ps`
- Teste manualmente: `curl http://localhost:8080/api/customer/owners`
- Verifique se há firewall bloqueando a porta 8080

### Problema: Erros 404 nos testes

**Solução:**
- Certifique-se de popular o banco de dados antes dos testes
- Verifique os endpoints no navegador manualmente

### Problema: Muitos erros de conexão (5xx)

**Causas possíveis:**
- Sistema sobrecarregado (esperado no cenário pico)
- Falta de recursos (RAM/CPU)
- Containers reiniciando

**Soluções:**
- Reduza o número de usuários temporariamente
- Aumente recursos do Docker Desktop (Settings > Resources)
- Verifique logs: `docker-compose logs -f`

### Problema: Script Python não encontra pandas

**Solução:**
```powershell
pip install pandas matplotlib
```

---

## 📝 Gerando o Artigo

### Dados para Incluir no Artigo

Após processar os resultados, você terá:

1. **Tabela Resumo** - Copie de `resumo_final.csv`
2. **Tabela LaTeX** - Gerada automaticamente pelo script de processamento
3. **Análise Comparativa** - Percentuais de variação entre cenários
4. **Gráficos** - Crie no Excel/Sheets ou com matplotlib

### Estrutura Sugerida (IEEE, 6 páginas)

1. **Abstract** - Resumo do trabalho e principais resultados
2. **Introduction** - Contexto, objetivos, justificativa
3. **Methodology** - Sistema testado, ferramenta, cenários
4. **Results** - Tabelas e gráficos com as métricas
5. **Discussion** - Análise dos resultados, comparações
6. **Conclusion** - Principais achados e limitações

---

## 🎥 Gravando o Vídeo

### Conteúdo Sugerido

1. Mostrar a estrutura de pastas do projeto
2. Subir o PetClinic com `docker-compose up`
3. Acessar a interface web funcionando
4. Executar um cenário de teste (pode ser versão reduzida)
5. Mostrar o dashboard do Locust (se usar modo web)
6. Mostrar os CSVs gerados na pasta results/
7. Executar o script de processamento
8. Mostrar o relatório final

**Duração sugerida:** 5-10 minutos

---

## 📚 Referências

- [Spring PetClinic Microservices](https://github.com/spring-petclinic/spring-petclinic-microservices)
- [Documentação Locust](https://docs.locust.io/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

## 👥 Autores

- **Pedro Tércio** - [seu-email@exemplo.com]
- **Robson Santos** - [email@exemplo.com]
- **Simão Morais** - simao.morais@ufpi.edu.br

**Disciplina:** Sistemas Distribuídos  
**Instituição:** UFPI  
**Período:** 2025.2

---

## 📄 Licença

Este projeto é para fins acadêmicos. O Spring PetClinic é mantido pela Pivotal/VMware sob a licença Apache 2.0.

---
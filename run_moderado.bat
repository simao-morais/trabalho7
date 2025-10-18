@echo off
echo Executando cenário MODERADO (100 usuários, 10 min)
locust -f locustfile.py --host=http://localhost:8080 --users 100 --spawn-rate 10 --run-time 10m --csv=results/cenario_moderado --headless
pause
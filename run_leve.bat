@echo off
echo Executando cenário LEVE (50 usuários, 10 min)
locust -f locustfile.py --host=http://localhost:8080 --users 50 --spawn-rate 5 --run-time 10m --csv=results/cenario_leve --headless
pause
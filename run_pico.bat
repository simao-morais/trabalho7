@echo off
echo Executando cenário PICO (200 usuários, 5 min)
locust -f locustfile.py --host=http://localhost:8080 --users 200 --spawn-rate 20 --run-time 5m --csv=results/cenario_pico --headless
pause
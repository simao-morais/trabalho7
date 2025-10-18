@echo off
for /L %%i in (1,1,30) do (
    echo Execução %%i do cenário LEVE
    locust -f locustfile.py --host=http://localhost:8080 --users 50 --spawn-rate 5 --run-time 10m --csv=results/leve_%%i --headless
    timeout /t 60
)

for /L %%i in (1,1,30) do (
    echo Execução %%i do cenário MODERADO
    locust -f locustfile.py --host=http://localhost:8080 --users 100 --spawn-rate 10 --run-time 10m --csv=results/moderado_%%i --headless
    timeout /t 60
)

for /L %%i in (1,1,30) do (
    echo Execução %%i do cenário PICO
    locust -f locustfile.py --host=http://localhost:8080 --users 200 --spawn-rate 20 --run-time 5m --csv=results/pico_%%i --headless
    timeout /t 60
)
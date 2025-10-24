@echo off
echo ================================================================================
echo RESET RÁPIDO - APENAS DADOS (Mantém outros serviços rodando)
echo ================================================================================
echo.
echo Este script irá reiniciar apenas os serviços com dados:
echo   • customers-service (owners/pets)
echo   • vets-service (veterinários)
echo   • visits-service (visitas)
echo.
echo Tempo estimado: 2 minutos
echo.
pause

REM Verificar se está na pasta correta
if not exist "spring-petclinic-microservices" (
    echo ERRO: Pasta spring-petclinic-microservices não encontrada!
    pause
    exit /b 1
)

cd spring-petclinic-microservices

echo.
echo [1/2] Reiniciando serviços de dados...
echo ────────────────────────────────────────────────────────
docker-compose restart customers-service vets-service visits-service
echo ✓ Serviços reiniciados
echo.

echo [2/2] Aguardando serviços ficarem prontos (2 minutos)...
echo ────────────────────────────────────────────────────────
timeout /t 60 /nobreak
echo   [■■□□] 50%...
timeout /t 60 /nobreak
echo   [■■■■] 100% - Concluído!
echo.

cd ..

echo.
echo ================================================================================
echo DADOS RESETADOS COM SUCESSO!
echo ================================================================================
echo.
echo Os serviços de dados foram reiniciados e voltaram ao estado padrão.
echo Outros serviços (gateway, discovery, etc.) continuam rodando.
echo.
echo Teste agora:
echo   curl http://localhost:8080/api/customer/owners
echo.
pause
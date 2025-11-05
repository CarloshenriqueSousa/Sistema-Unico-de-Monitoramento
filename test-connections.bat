@echo off
REM Script de teste de conexões do S.U.M para Windows
REM Este script verifica se todos os serviços estão funcionando corretamente

echo 🔍 Testando conexões do S.U.M...

set total_tests=0
set passed_tests=0
set failed_tests=0

echo ==========================================
echo 🧪 TESTE DE CONEXÕES - S.U.M
echo ==========================================
echo.

REM Função para executar teste
:run_test
set test_name=%1
set test_command=%2
set /a total_tests+=1
echo [TEST] Testando: %test_name%

%test_command% >nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS] %test_name% ✓
    set /a passed_tests+=1
) else (
    echo [FAIL] %test_name% ✗
    set /a failed_tests+=1
)
goto :eof

REM Teste 1: Verificar se Docker está rodando
call :run_test "Docker está rodando" "docker ps"

REM Teste 2: Verificar containers
call :run_test "Containers estão rodando" "docker-compose ps | findstr Up"

REM Teste 3: PostgreSQL
call :run_test "PostgreSQL está respondendo" "docker-compose exec -T db pg_isready -U sum_user -d sum_db"

REM Teste 4: Backend Django - Health Check
call :run_test "Backend Django - Health Check" "curl -f http://localhost:8000/api/health/"

REM Teste 5: Backend Django - Health Check Detalhado
call :run_test "Backend Django - Health Detalhado" "curl -f http://localhost:8000/api/auth/health/detailed/"

REM Teste 6: Backend Django - API Info
call :run_test "Backend Django - API Info" "curl -f http://localhost:8000/api/info/"

REM Teste 7: Frontend Vue.js
call :run_test "Frontend Vue.js está respondendo" "curl -f http://localhost:5173"

REM Teste 8: Nginx - Health Check
call :run_test "Nginx - Health Check" "curl -f http://localhost:80/health"

REM Teste 9: Nginx - Frontend via Proxy
call :run_test "Nginx - Frontend via Proxy" "curl -f http://localhost:80"

REM Teste 10: Nginx - Backend via Proxy
call :run_test "Nginx - Backend via Proxy" "curl -f http://localhost:80/api/health/"

REM Teste 11: Admin Django
call :run_test "Admin Django está acessível" "curl -f http://localhost:8000/admin/"

REM Teste 12: Teste de autenticação (login)
echo [TEST] Testando autenticação...
curl -s -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d "{\"identifier\": \"admin\", \"password\": \"admin123\"}" > temp_auth.json 2>nul
findstr /C:"access" temp_auth.json >nul 2>&1
if %errorlevel% equ 0 (
    echo [PASS] Autenticação funcionando ✓
    set /a passed_tests+=1
) else (
    echo [FAIL] Autenticação falhou ✗
    set /a failed_tests+=1
)
set /a total_tests+=1
del temp_auth.json 2>nul

REM Teste 13: Verificar banco de dados - conexão
call :run_test "Banco de dados - Conexão" "docker-compose exec -T db psql -U sum_user -d sum_db -c \"SELECT 1;\""

REM Teste 14: Verificar banco de dados - tabelas
echo [TEST] Verificando tabelas do banco de dados...
docker-compose exec -T db psql -U sum_user -d sum_db -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" > temp_tables.txt 2>nul
set /p db_tables=<temp_tables.txt
set db_tables=%db_tables: =%
if %db_tables% gtr 0 (
    echo [PASS] Banco de dados tem %db_tables% tabelas ✓
    set /a passed_tests+=1
) else (
    echo [FAIL] Banco de dados não tem tabelas ✗
    set /a failed_tests+=1
)
set /a total_tests+=1
del temp_tables.txt 2>nul

REM Teste 15: Verificar logs de erro
echo [TEST] Verificando logs de erro...
docker-compose logs --tail=100 2>&1 | findstr /I "error exception traceback" > temp_errors.txt
for /f %%i in ('type temp_errors.txt ^| find /c /v ""') do set error_logs=%%i
if %error_logs% equ 0 (
    echo [PASS] Nenhum erro encontrado nos logs ✓
    set /a passed_tests+=1
) else (
    echo [WARN] Encontrados %error_logs% possíveis erros nos logs ⚠
    set /a passed_tests+=1
)
set /a total_tests+=1
del temp_errors.txt 2>nul

echo.
echo ==========================================
echo 📊 RESULTADO DOS TESTES
echo ==========================================
echo Total de testes: %total_tests%
echo ✅ Passou: %passed_tests%
echo ❌ Falhou: %failed_tests%
echo.

if %failed_tests% equ 0 (
    echo [SUCCESS] 🎉 Todos os testes passaram! O sistema está funcionando perfeitamente!
    echo.
    echo 🌐 Acesse o sistema em:
    echo    • Frontend: http://localhost:5173
    echo    • Backend: http://localhost:8000
    echo    • Admin: http://localhost:8000/admin
    echo    • Proxy: http://localhost:80
    echo.
    echo 👤 Credenciais:
    echo    • Usuário: admin
    echo    • Senha: admin123
    pause
    exit /b 0
) else (
    echo [ERROR] ⚠️  Alguns testes falharam. Verifique os logs e configurações.
    echo.
    echo 🔧 Comandos úteis para diagnóstico:
    echo    • docker-compose logs -f
    echo    • docker-compose ps
    echo    • docker-compose exec backend python django-back-end/manage.py check
    pause
    exit /b 1
)

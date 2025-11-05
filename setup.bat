@echo off
REM Script de inicialização do S.U.M (Sistema Único de Mapeamento) para Windows
REM Este script configura e inicia todos os serviços necessários

echo 🚀 Iniciando configuração do S.U.M...

REM Verificar se Docker está instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker não está instalado. Por favor, instale o Docker Desktop primeiro.
    pause
    exit /b 1
)

REM Verificar se Docker Compose está instalado
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro.
    pause
    exit /b 1
)

echo [INFO] Docker e Docker Compose encontrados ✓

REM Parar containers existentes (se houver)
echo [INFO] Parando containers existentes...
docker-compose down --remove-orphans

REM Perguntar sobre limpeza de volumes
set /p clean_volumes="Deseja limpar volumes antigos? (y/N): "
if /i "%clean_volumes%"=="y" (
    echo [INFO] Removendo volumes antigos...
    docker-compose down -v
    docker system prune -f
)

REM Construir imagens
echo [INFO] Construindo imagens Docker...
docker-compose build --no-cache

REM Iniciar serviços
echo [INFO] Iniciando serviços...
docker-compose up -d

REM Aguardar serviços ficarem prontos
echo [INFO] Aguardando serviços ficarem prontos...
timeout /t 10 /nobreak >nul

REM Verificar status dos serviços
echo [INFO] Verificando status dos serviços...

REM Verificar PostgreSQL
docker-compose exec -T db pg_isready -U sum_user -d sum_db >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] PostgreSQL está funcionando ✓
) else (
    echo [ERROR] PostgreSQL não está respondendo
)

REM Verificar Backend Django
curl -f http://localhost:8000/api/health/ >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] Backend Django está funcionando ✓
) else (
    echo [WARNING] Backend Django pode não estar totalmente pronto ainda
)

REM Verificar Frontend Vue.js
curl -f http://localhost:5173 >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] Frontend Vue.js está funcionando ✓
) else (
    echo [WARNING] Frontend Vue.js pode não estar totalmente pronto ainda
)

REM Verificar Nginx
curl -f http://localhost:80/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] Nginx está funcionando ✓
) else (
    echo [WARNING] Nginx pode não estar totalmente pronto ainda
)

echo.
echo [SUCCESS] 🎉 Configuração concluída!
echo.
echo 📋 Informações de acesso:
echo   🌐 Frontend: http://localhost:5173
echo   🔧 Backend API: http://localhost:8000
echo   🗄️  Admin Django: http://localhost:8000/admin
echo   🌍 Nginx (Proxy): http://localhost:80
echo.
echo 👤 Credenciais padrão:
echo   Usuário: admin
echo   Senha: admin123
echo   Email: admin@sum.local
echo.
echo 📊 Para verificar logs:
echo   docker-compose logs -f [serviço]
echo.
echo 🛑 Para parar os serviços:
echo   docker-compose down
echo.
echo [INFO] Acesse http://localhost:80 para começar a usar o S.U.M!
pause

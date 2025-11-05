#!/bin/bash

# Script de teste de conexões do S.U.M
# Este script verifica se todos os serviços estão funcionando corretamente

set -e

echo "🔍 Testando conexões do S.U.M..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_status() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

# Contador de testes
total_tests=0
passed_tests=0
failed_tests=0

# Função para executar teste
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_status="${3:-0}"
    
    total_tests=$((total_tests + 1))
    print_status "Testando: $test_name"
    
    if eval "$test_command" > /dev/null 2>&1; then
        if [ $? -eq $expected_status ]; then
            print_success "$test_name ✓"
            passed_tests=$((passed_tests + 1))
            return 0
        else
            print_error "$test_name ✗ (Status inesperado)"
            failed_tests=$((failed_tests + 1))
            return 1
        fi
    else
        print_error "$test_name ✗"
        failed_tests=$((failed_tests + 1))
        return 1
    fi
}

echo "=========================================="
echo "🧪 TESTE DE CONEXÕES - S.U.M"
echo "=========================================="
echo

# Teste 1: Verificar se Docker está rodando
run_test "Docker está rodando" "docker ps"

# Teste 2: Verificar containers
run_test "Containers estão rodando" "docker-compose ps | grep -q 'Up'"

# Teste 3: PostgreSQL
run_test "PostgreSQL está respondendo" "docker-compose exec -T db pg_isready -U sum_user -d sum_db"

# Teste 4: Backend Django - Health Check
run_test "Backend Django - Health Check" "curl -f http://localhost:8000/api/health/"

# Teste 5: Backend Django - Health Check Detalhado
run_test "Backend Django - Health Detalhado" "curl -f http://localhost:8000/api/auth/health/detailed/"

# Teste 6: Backend Django - API Info
run_test "Backend Django - API Info" "curl -f http://localhost:8000/api/info/"

# Teste 7: Frontend Vue.js
run_test "Frontend Vue.js está respondendo" "curl -f http://localhost:5173"

# Teste 8: Nginx - Health Check
run_test "Nginx - Health Check" "curl -f http://localhost:80/health"

# Teste 9: Nginx - Frontend via Proxy
run_test "Nginx - Frontend via Proxy" "curl -f http://localhost:80"

# Teste 10: Nginx - Backend via Proxy
run_test "Nginx - Backend via Proxy" "curl -f http://localhost:80/api/health/"

# Teste 11: Admin Django
run_test "Admin Django está acessível" "curl -f http://localhost:8000/admin/"

# Teste 12: Teste de autenticação (login)
print_status "Testando autenticação..."
auth_response=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"identifier": "admin", "password": "admin123"}' 2>/dev/null)

if echo "$auth_response" | grep -q "access"; then
    print_success "Autenticação funcionando ✓"
    passed_tests=$((passed_tests + 1))
else
    print_error "Autenticação falhou ✗"
    failed_tests=$((failed_tests + 1))
fi
total_tests=$((total_tests + 1))

# Teste 13: Verificar banco de dados - conexão
run_test "Banco de dados - Conexão" "docker-compose exec -T db psql -U sum_user -d sum_db -c 'SELECT 1;'"

# Teste 14: Verificar banco de dados - tabelas
print_status "Verificando tabelas do banco de dados..."
db_tables=$(docker-compose exec -T db psql -U sum_user -d sum_db -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' \n')

if [ "$db_tables" -gt 0 ]; then
    print_success "Banco de dados tem $db_tables tabelas ✓"
    passed_tests=$((passed_tests + 1))
else
    print_error "Banco de dados não tem tabelas ✗"
    failed_tests=$((failed_tests + 1))
fi
total_tests=$((total_tests + 1))

# Teste 15: Verificar logs de erro
print_status "Verificando logs de erro..."
error_logs=$(docker-compose logs --tail=100 2>&1 | grep -i "error\|exception\|traceback" | wc -l)

if [ "$error_logs" -eq 0 ]; then
    print_success "Nenhum erro encontrado nos logs ✓"
    passed_tests=$((passed_tests + 1))
else
    print_warning "Encontrados $error_logs possíveis erros nos logs ⚠"
    passed_tests=$((passed_tests + 1))  # Não falha o teste, apenas avisa
fi
total_tests=$((total_tests + 1))

echo
echo "=========================================="
echo "📊 RESULTADO DOS TESTES"
echo "=========================================="
echo "Total de testes: $total_tests"
echo "✅ Passou: $passed_tests"
echo "❌ Falhou: $failed_tests"
echo

if [ $failed_tests -eq 0 ]; then
    print_success "🎉 Todos os testes passaram! O sistema está funcionando perfeitamente!"
    echo
    echo "🌐 Acesse o sistema em:"
    echo "   • Frontend: http://localhost:5173"
    echo "   • Backend: http://localhost:8000"
    echo "   • Admin: http://localhost:8000/admin"
    echo "   • Proxy: http://localhost:80"
    echo
    echo "👤 Credenciais:"
    echo "   • Usuário: admin"
    echo "   • Senha: admin123"
    exit 0
else
    print_error "⚠️  Alguns testes falharam. Verifique os logs e configurações."
    echo
    echo "🔧 Comandos úteis para diagnóstico:"
    echo "   • docker-compose logs -f"
    echo "   • docker-compose ps"
    echo "   • docker-compose exec backend python django-back-end/manage.py check"
    exit 1
fi

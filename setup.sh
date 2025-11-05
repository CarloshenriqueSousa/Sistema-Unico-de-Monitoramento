#!/bin/bash

# Script de inicialização do S.U.M (Sistema Único de Mapeamento)
# Este script configura e inicia todos os serviços necessários

set -e

echo "🚀 Iniciando configuração do S.U.M..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
    exit 1
fi

print_status "Docker e Docker Compose encontrados ✓"

# Parar containers existentes (se houver)
print_status "Parando containers existentes..."
docker-compose down --remove-orphans || true

# Limpar volumes antigos (opcional)
read -p "Deseja limpar volumes antigos? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Removendo volumes antigos..."
    docker-compose down -v || true
    docker system prune -f || true
fi

# Construir imagens
print_status "Construindo imagens Docker..."
docker-compose build --no-cache

# Iniciar serviços
print_status "Iniciando serviços..."
docker-compose up -d

# Aguardar serviços ficarem prontos
print_status "Aguardando serviços ficarem prontos..."
sleep 10

# Verificar status dos serviços
print_status "Verificando status dos serviços..."

# Verificar PostgreSQL
if docker-compose exec -T db pg_isready -U sum_user -d sum_db > /dev/null 2>&1; then
    print_success "PostgreSQL está funcionando ✓"
else
    print_error "PostgreSQL não está respondendo"
fi

# Verificar Backend Django
if curl -f http://localhost:8000/api/health/ > /dev/null 2>&1; then
    print_success "Backend Django está funcionando ✓"
else
    print_warning "Backend Django pode não estar totalmente pronto ainda"
fi

# Verificar Frontend Vue.js
if curl -f http://localhost:5173 > /dev/null 2>&1; then
    print_success "Frontend Vue.js está funcionando ✓"
else
    print_warning "Frontend Vue.js pode não estar totalmente pronto ainda"
fi

# Verificar Nginx
if curl -f http://localhost:80/health > /dev/null 2>&1; then
    print_success "Nginx está funcionando ✓"
else
    print_warning "Nginx pode não estar totalmente pronto ainda"
fi

echo
print_success "🎉 Configuração concluída!"
echo
echo "📋 Informações de acesso:"
echo "  🌐 Frontend: http://localhost:5173"
echo "  🔧 Backend API: http://localhost:8000"
echo "  🗄️  Admin Django: http://localhost:8000/admin"
echo "  🌍 Nginx (Proxy): http://localhost:80"
echo
echo "👤 Credenciais padrão:"
echo "  Usuário: admin"
echo "  Senha: admin123"
echo "  Email: admin@sum.local"
echo
echo "📊 Para verificar logs:"
echo "  docker-compose logs -f [serviço]"
echo
echo "🛑 Para parar os serviços:"
echo "  docker-compose down"
echo
print_status "Acesse http://localhost:80 para começar a usar o S.U.M!"

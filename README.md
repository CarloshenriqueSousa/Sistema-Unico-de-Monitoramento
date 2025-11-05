# S.U.M - Sistema Único de Mapeamento

Sistema educacional completo com backend Django, frontend Vue.js e banco PostgreSQL, projetado para mapeamento inteligente de salas de aula e gestão educacional.

## 🚀 Início Rápido

### Pré-requisitos

- Docker Desktop instalado
- Docker Compose instalado
- Git instalado

### Instalação Automática

#### Linux/macOS:
```bash
chmod +x setup.sh
./setup.sh
```

#### Windows:
```cmd
setup.bat
```

### Instalação Manual

1. **Clone o repositório:**
```bash
git clone <seu-repositorio>
cd Sistema_Unico_de_Mapeamento
```

2. **Configure o ambiente:**
```bash
# Copie o arquivo de configuração
cp backend/django-back-end/env.local backend/django-back-end/.env

# Edite as configurações se necessário
nano backend/django-back-end/.env
```

3. **Inicie os serviços:**
```bash
docker-compose up -d
```

4. **Aguarde a inicialização completa:**
```bash
# Verifique os logs
docker-compose logs -f

# Verifique o status
docker-compose ps
```

## 📋 Informações de Acesso

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **Admin Django:** http://localhost:8000/admin
- **Nginx (Proxy):** http://localhost:80

### Credenciais Padrão

- **Usuário:** admin
- **Senha:** admin123
- **Email:** admin@sum.local

## 🏗️ Arquitetura do Sistema

### Backend (Django)
- **Framework:** Django 4.2+ com Django REST Framework
- **Autenticação:** JWT (Simple JWT)
- **Banco de Dados:** PostgreSQL 15
- **Cache:** Redis (opcional)
- **IA:** Integração OpenAI para geração de atividades

### Frontend (Vue.js)
- **Framework:** Vue 3 com Composition API
- **Build Tool:** Vite
- **UI:** Tailwind CSS
- **Estado:** Pinia
- **Roteamento:** Vue Router 4
- **PWA:** Service Worker com Workbox

### Banco de Dados
- **PostgreSQL 15** com configurações otimizadas
- **Encoding:** UTF-8
- **Locale:** pt_BR.UTF-8
- **Timezone:** America/Sao_Paulo

### Proxy Reverso
- **Nginx** configurado para roteamento inteligente
- **Load Balancing** entre frontend e backend
- **Cache** para arquivos estáticos

## 🔧 Configuração Avançada

### Variáveis de Ambiente

Crie um arquivo `.env` em `backend/django-back-end/`:

```env
# Configurações do Django
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1,backend,nginx

# Banco de Dados
DATABASE_URL=postgresql://sum_user:sum_password@db:5432/sum_db

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8080

# IA (Opcional)
OPENAI_API_KEY=sua-chave-openai-aqui

# Logging
LOG_LEVEL=INFO
```

### Configuração do Frontend

Crie um arquivo `.env` em `frontend/`:

```env
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=10000
```

## 📊 Monitoramento

### Health Checks

- **Backend:** http://localhost:8000/api/health/
- **Detalhado:** http://localhost:8000/api/auth/health/detailed/
- **Métricas:** http://localhost:8000/api/auth/metrics/

### Logs

```bash
# Todos os serviços
docker-compose logs -f

# Serviço específico
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
docker-compose logs -f nginx
```

### Status dos Serviços

```bash
docker-compose ps
```

## 🛠️ Desenvolvimento

### Estrutura do Projeto

```
Sistema_Unico_de_Mapeamento/
├── backend/
│   └── django-back-end/
│       ├── core/           # Autenticação e usuários
│       ├── escola/         # Gestão escolar
│       ├── estudantes/     # Gestão de estudantes
│       ├── professores/    # Gestão de professores
│       ├── atividades/     # Atividades e avaliações
│       ├── eventos/        # Eventos escolares
│       ├── placement/      # Mapeamento e IA
│       └── setup/          # Configurações Django
├── frontend/
│   └── src/
│       ├── components/      # Componentes Vue
│       ├── views/          # Páginas
│       ├── services/        # Serviços API
│       ├── store/          # Estado Pinia
│       └── types/          # Tipos TypeScript
├── nginx/
│   └── nginx.conf          # Configuração Nginx
└── docker-compose.yml      # Orquestração Docker
```

### Comandos Úteis

```bash
# Entrar no container do backend
docker-compose exec backend bash

# Executar migrações
docker-compose exec backend python django-back-end/manage.py migrate

# Criar superusuário
docker-compose exec backend python django-back-end/manage.py shell -c "from core.models import User; User.objects.create_superuser('admin', 'admin@sum.local', 'admin123', user_type='admin')"

# Coletar arquivos estáticos
docker-compose exec backend python django-back-end/manage.py collectstatic

# Entrar no container do frontend
docker-compose exec frontend sh

# Instalar dependências do frontend
docker-compose exec frontend npm install

# Executar testes
docker-compose exec backend python django-back-end/manage.py test
```

## 🔒 Segurança

### Produção

1. **Altere a SECRET_KEY:**
```python
SECRET_KEY = 'sua-chave-super-secreta-aqui'
```

2. **Configure HTTPS:**
```nginx
# Adicione certificados SSL no nginx.conf
```

3. **Restrinja ALLOWED_HOSTS:**
```python
ALLOWED_HOSTS = ['seu-dominio.com']
```

4. **Configure CORS adequadamente:**
```python
CORS_ALLOWED_ORIGINS = ['https://seu-dominio.com']
```

## 🐛 Troubleshooting

### Problemas Comuns

1. **Porta já em uso:**
```bash
# Verifique processos usando as portas
netstat -tulpn | grep :80
netstat -tulpn | grep :8000
netstat -tulpn | grep :5173
```

2. **Banco não conecta:**
```bash
# Verifique logs do PostgreSQL
docker-compose logs db

# Teste conexão manual
docker-compose exec db psql -U sum_user -d sum_db -c "SELECT 1;"
```

3. **Frontend não carrega:**
```bash
# Verifique logs do frontend
docker-compose logs frontend

# Reinstale dependências
docker-compose exec frontend npm install
```

4. **Backend não responde:**
```bash
# Verifique logs do backend
docker-compose logs backend

# Execute migrações
docker-compose exec backend python django-back-end/manage.py migrate
```

### Reset Completo

```bash
# Pare todos os serviços
docker-compose down

# Remova volumes e imagens
docker-compose down -v
docker system prune -af

# Reconstrua tudo
docker-compose build --no-cache
docker-compose up -d
```

## 📚 Documentação da API

### Endpoints Principais

- **Autenticação:** `/api/auth/`
- **Escola:** `/api/escola/`
- **Estudantes:** `/api/estudantes/`
- **Professores:** `/api/professores/`
- **Atividades:** `/api/atividades/`
- **Eventos:** `/api/eventos/`
- **Mapeamento:** `/api/mapeamento/`

### Exemplo de Uso

```javascript
// Login
const response = await fetch('/api/auth/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    identifier: 'admin',
    password: 'admin123'
  })
});

const data = await response.json();
// { access: 'token...', refresh: 'token...', user_type: 'admin', ... }
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte, abra uma issue no GitHub ou entre em contato através do email: suporte@sum.local

---

**S.U.M - Sistema Único de Mapeamento**  
*Transformando a educação através da tecnologia* 🚀

teste
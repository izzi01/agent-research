#!/bin/bash
# Start All GUI Tools for Vietnamese Marketing Automation

set -e

echo "🚀 Starting All GUI Tools"
echo "========================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# 1. Start PostgreSQL (if not running)
if ! docker ps | grep -q postgres-pgvector; then
    echo "📦 Starting PostgreSQL..."
    docker run -d \
      --name postgres-pgvector \
      -e POSTGRES_USER=agno \
      -e POSTGRES_PASSWORD=changeme123 \
      -e POSTGRES_DB=marketing_automation \
      -p 5432:5432 \
      pgvector/pgvector:pg16
    echo "✅ PostgreSQL started"
else
    echo "✅ PostgreSQL already running"
fi

# 2. Start pgAdmin (database GUI)
if ! docker ps | grep -q pgadmin; then
    echo "📦 Starting pgAdmin..."
    docker run -d \
      --name pgadmin \
      -p 5050:80 \
      -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
      -e PGADMIN_DEFAULT_PASSWORD=admin \
      dpage/pgadmin4
    echo "✅ pgAdmin started at http://localhost:5050"
else
    echo "✅ pgAdmin already running at http://localhost:5050"
fi

# 3. Start n8n (workflow GUI)
if ! docker ps | grep -q n8n; then
    echo "📦 Starting n8n..."
    docker run -d \
      --name n8n \
      -p 5678:5678 \
      -e N8N_BASIC_AUTH_USER=admin \
      -e N8N_BASIC_AUTH_PASSWORD=changeme123 \
      -e WEBHOOK_URL=http://localhost:5678/ \
      -v ~/.n8n:/home/node/.n8n \
      n8nio/n8n
    echo "✅ n8n started at http://localhost:5678"
else
    echo "✅ n8n already running at http://localhost:5678"
fi

# 4. Start AgentOS API server (in background)
if ! lsof -ti:8080 > /dev/null 2>&1; then
    echo "📦 Starting AgentOS API server..."
    source .venv/bin/activate 2>/dev/null || true
    nohup python main.py > agentos.log 2>&1 &
    sleep 3
    echo "✅ AgentOS API started at http://localhost:8080"
else
    echo "✅ AgentOS API already running at http://localhost:8080"
fi

echo ""
echo "========================================"
echo "🎉 All GUIs Started Successfully!"
echo "========================================"
echo ""
echo "📌 Access URLs:"
echo ""
echo "1. 🌐 FastAPI Docs (API Testing)"
echo "   → http://localhost:8080/docs"
echo "   → Interactive API documentation"
echo ""
echo "2. 🔄 n8n (Workflow Automation)"
echo "   → http://localhost:5678"
echo "   → Username: admin"
echo "   → Password: changeme123"
echo ""
echo "3. 💾 pgAdmin (Database Management)"
echo "   → http://localhost:5050"
echo "   → Email: admin@admin.com"
echo "   → Password: admin"
echo "   → Database connection:"
echo "      Host: host.docker.internal (Mac/Windows)"
echo "      Host: 172.17.0.1 (Linux)"
echo "      Port: 5432"
echo "      Database: marketing_automation"
echo "      Username: agno"
echo "      Password: changeme123"
echo ""
echo "4. 📊 Prometheus Metrics"
echo "   → http://localhost:8080/metrics"
echo ""
echo "========================================"
echo ""
echo "💡 Quick Actions:"
echo ""
echo "• Test API:     curl http://localhost:8080/health"
echo "• View logs:    tail -f agentos.log"
echo "• Stop all:     ./stop-all-guis.sh"
echo ""
echo "Press Ctrl+C to see this info again, or check agentos.log for API logs"
echo ""

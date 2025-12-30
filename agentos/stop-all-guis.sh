#!/bin/bash
# Stop All GUI Tools

echo "🛑 Stopping All GUI Tools"
echo "========================="
echo ""

# Stop AgentOS
if lsof -ti:8080 > /dev/null 2>&1; then
    echo "⏹️  Stopping AgentOS API server..."
    lsof -ti:8080 | xargs kill -9 2>/dev/null
    echo "✅ AgentOS stopped"
else
    echo "✅ AgentOS not running"
fi

# Stop n8n
if docker ps | grep -q n8n; then
    echo "⏹️  Stopping n8n..."
    docker stop n8n > /dev/null 2>&1
    docker rm n8n > /dev/null 2>&1
    echo "✅ n8n stopped"
else
    echo "✅ n8n not running"
fi

# Stop pgAdmin
if docker ps | grep -q pgadmin; then
    echo "⏹️  Stopping pgAdmin..."
    docker stop pgadmin > /dev/null 2>&1
    docker rm pgadmin > /dev/null 2>&1
    echo "✅ pgAdmin stopped"
else
    echo "✅ pgAdmin not running"
fi

# Stop PostgreSQL (optional - uncomment if you want to stop it too)
# if docker ps | grep -q postgres-pgvector; then
#     echo "⏹️  Stopping PostgreSQL..."
#     docker stop postgres-pgvector > /dev/null 2>&1
#     echo "✅ PostgreSQL stopped"
# fi

echo ""
echo "========================================"
echo "✅ All GUIs Stopped"
echo "========================================"
echo ""
echo "Note: PostgreSQL is still running (keeping your data safe)"
echo "To stop PostgreSQL: docker stop postgres-pgvector"
echo ""

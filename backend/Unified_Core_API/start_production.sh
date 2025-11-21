#!/bin/bash

# Unified Core API - Production Startup Script
# Lead: Rishabh Yadav

echo "🚀 Starting Unified Core API - Production Mode"
echo "================================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "✅ .env created. Please configure it before proceeding."
    echo "   Edit .env with: nano .env"
    exit 1
fi

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose found"
echo ""

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.production.yml down
echo ""

# Build containers
echo "🔨 Building containers..."
docker-compose -f docker-compose.production.yml build
echo ""

# Start services
echo "🚀 Starting all services..."
docker-compose -f docker-compose.production.yml up -d
echo ""

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10
echo ""

# Check health
echo "🏥 Checking service health..."
echo ""

# Check API
if curl -f http://localhost:8005/health &> /dev/null; then
    echo "✅ Unified Core API: Healthy"
else
    echo "❌ Unified Core API: Not responding"
fi

# Check RabbitMQ
if curl -f http://localhost:15672 &> /dev/null; then
    echo "✅ RabbitMQ: Healthy"
else
    echo "⚠️  RabbitMQ: Not responding"
fi

# Check Redis
if docker exec unified-redis redis-cli ping &> /dev/null; then
    echo "✅ Redis: Healthy"
else
    echo "⚠️  Redis: Not responding"
fi

# Check PostgreSQL
if docker exec unified-postgres pg_isready -U user &> /dev/null; then
    echo "✅ PostgreSQL: Healthy"
else
    echo "⚠️  PostgreSQL: Not responding"
fi

echo ""
echo "================================================"
echo "🎉 Unified Core API is running!"
echo "================================================"
echo ""
echo "📊 Access Points:"
echo "   API:          http://localhost:8005"
echo "   API Docs:     http://localhost:8005/docs"
echo "   Dashboard:    http://localhost:3000"
echo "   RabbitMQ UI:  http://localhost:15672 (guest/guest)"
echo ""
echo "🔍 Monitoring:"
echo "   Health:       http://localhost:8005/health"
echo "   Status:       http://localhost:8005/status"
echo "   Logs:         http://localhost:8005/logs"
echo ""
echo "📋 Management Commands:"
echo "   View logs:    docker-compose -f docker-compose.production.yml logs -f"
echo "   Stop:         docker-compose -f docker-compose.production.yml down"
echo "   Restart:      docker-compose -f docker-compose.production.yml restart"
echo ""
echo "🧪 Run tests:"
echo "   python test_pipeline.py"
echo ""
echo "✅ System ready for production!"
echo ""

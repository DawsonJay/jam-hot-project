#!/bin/bash
# Start Jam Hot database
# Usage: ./start-db.sh

echo "Starting Jam Hot database..."

# Check if container already exists and remove it
if docker ps -a --format 'table {{.Names}}' | grep -q "jam-hot-postgres"; then
    echo "Stopping and removing existing container..."
    docker stop jam-hot-postgres
    docker rm jam-hot-postgres
fi

# Start database using direct docker command
docker run --name jam-hot-postgres -e POSTGRES_PASSWORD="Glitter-Nebula-Frost" -e POSTGRES_DB=jam_hot -p 5433:5432 -v $(pwd)/data:/var/lib/postgresql/data -d postgres:15

# Wait for database to be ready
echo "Waiting for database to start..."
sleep 5

# Test connection
if PGPASSWORD='Glitter-Nebula-Frost' psql -h localhost -p 5433 -U postgres -d jam_hot -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Database is ready!"
    echo ""
    echo "Connection details:"
    echo "  Host: localhost"
    echo "  Port: 5433"
    echo "  Database: jam_hot"
    echo "  User: postgres"
    echo "  Password: Glitter-Nebula-Frost"
    echo ""
    echo "To connect: psql -h localhost -p 5433 -U postgres -d jam_hot"
    echo "To stop: ./scripts/database/stop-db.sh"
else
    echo "❌ Database failed to start"
    exit 1
fi

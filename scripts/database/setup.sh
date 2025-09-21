#!/bin/bash
# Setup Jam Hot database
# Usage: ./setup.sh

echo "Setting up Jam Hot database..."

# Start database
echo "Starting PostgreSQL database..."
docker-compose up -d

# Wait for database to be ready
echo "Waiting for database to start..."
sleep 5

# Create schema
echo "Creating database schema..."
PGPASSWORD=password psql -h localhost -p 5432 -U postgres -d jam_hot -f scripts/database/create_database.sql

if [ $? -eq 0 ]; then
    echo "✅ Database setup complete!"
    echo ""
    echo "Database connection:"
    echo "  Host: localhost"
    echo "  Port: 5432"
    echo "  Database: jam_hot"
    echo "  User: postgres"
    echo "  Password: password"
    echo ""
    echo "To connect: psql -h localhost -p 5432 -U postgres -d jam_hot"
    echo "To stop: docker-compose down"
else
    echo "❌ Database setup failed"
    exit 1
fi

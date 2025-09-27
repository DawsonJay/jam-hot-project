#!/bin/bash
# Export Jam Hot database data for production deployment
# Usage: ./export-data.sh

echo "Exporting Jam Hot database data..."

# Load environment variables
source .env

# Create deploy directory if it doesn't exist
mkdir -p deploy

# Export database as INSERT statements with proper ordering
echo "Creating database dump with INSERT statements..."

# Use pg_dump with --inserts and --column-inserts for clean INSERT statements
# This should create a properly ordered dump file
echo "Exporting complete database..."
PGPASSWORD="$DB_PASSWORD" pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" --inserts --column-inserts > deploy/db-dump.sql

echo "✅ Database exported to deploy/ directory"
echo ""
echo "File created:"
echo "  deploy/db-dump.sql - Complete database (schema + data)"
echo ""
echo "To import to production:"
echo "  psql -h production-host -U production-user -d production-db -f deploy/db-dump.sql"

#!/bin/bash
# Export Jam Hot database data for production deployment
# Usage: ./export-data.sh

echo "Exporting Jam Hot database data..."

# Load environment variables
source .env

# Create deploy directory if it doesn't exist
mkdir -p deploy

# Export database with simple CREATE TABLE and INSERT statements
echo "Creating simple database dump..."

# Use our custom Python script to create a clean dump
echo "Exporting with simple script..."
python3 scripts/database/create_simple_dump.py

echo "✅ Database exported to deploy/ directory"
echo ""
echo "File created:"
echo "  deploy/db-dump.sql - Complete database (schema + data)"
echo ""
echo "To import to production:"
echo "  psql -h production-host -U production-user -d production-db -f deploy/db-dump.sql"

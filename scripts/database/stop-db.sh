#!/bin/bash
# Stop Jam Hot database
# Usage: ./stop-db.sh

echo "Stopping Jam Hot database..."

# Stop database using direct docker command
docker stop jam-hot-postgres

echo "✅ Database stopped"

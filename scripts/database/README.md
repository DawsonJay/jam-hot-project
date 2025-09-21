# Database Setup - Jam Hot Project

## Quick Start

**Start database:**
```bash
./scripts/database/start-db.sh
```

**Stop database:**
```bash
./scripts/database/stop-db.sh
```

**Connect to database:**
```bash
psql -h localhost -p 5433 -U postgres -d jam_hot
```

## Connection Details

- **Host**: localhost
- **Port**: 5433
- **Database**: jam_hot
- **User**: postgres
- **Password**: Glitter-Nebula-Frost

## Database Structure

### Tables
- **fruits** - All AI-recognizable fruits (basic info)
- **profiles** - Detailed fruit information (only for covered fruits)
- **recipes** - Jam recipes with essential data
- **recipe_fruits** - Many-to-many relationship between recipes and fruits

### Views
- **recipe_summary** - Recipes with fruit information
- **fruit_coverage** - Fruit coverage status

## Data Management

### Export Data for Production
```bash
./scripts/database/export-data.sh
```
Creates exports in `exports/` directory:
- `schema.sql` - Database structure only
- `data.sql` - Data only  
- `full_export.sql` - Complete database

### Import to Production
```bash
psql -h production-host -U production-user -d production-db -f exports/full_export.sql
```

## Development Workflow

1. **Start database** - `./scripts/database/start-db.sh`
2. **Run scraper** - Populate with real recipe data
3. **Develop backend** - Build API with real data
4. **Develop frontend** - Test with actual recipes
5. **Export data** - `./scripts/database/export-data.sh`
6. **Deploy to Railway** - Import data to production

## Data Persistence

- **Data stored in**: `./data_fresh/` directory
- **Survives restarts** - Data persists between container restarts
- **Portable** - Move project folder, data comes with it
- **Version control** - Data directory in `.gitignore`

## Troubleshooting

**Database won't start:**
- Check if port 5432 is available
- Run `docker-compose logs` to see errors

**Connection failed:**
- Verify database is running: `docker ps | grep jam-hot`
- Check password: `Glitter-Nebula-Frost`
- Try connecting: `psql -h localhost -p 5432 -U postgres -d jam_hot`

**Reset database:**
- Stop: `./scripts/database/stop-db.sh`
- Remove data: `rm -rf data_fresh/`
- Start: `./scripts/database/start-db.sh`
- Recreate schema: `psql -h localhost -p 5432 -U postgres -d jam_hot -f scripts/database/create_database.sql`

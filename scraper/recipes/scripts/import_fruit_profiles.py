#!/usr/bin/env python3
"""
Fruit profile import script.

This script imports fruit profiles from JSON files into the database.
It maps the JSON structure to the database schema and handles any missing fields.
"""

import sys
import os
import json
import glob
from datetime import datetime
from typing import Dict, Any, Optional

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scraper.scripts.insert_recipes import connect_to_database
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_timestamp():
    """Get current timestamp for logging."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_fruit_profile(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Load a fruit profile from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dict with fruit profile data, or None if loading failed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            profile_data = json.load(f)
        return profile_data
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Error loading {file_path}: {e}")
        return None

def map_profile_to_database(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map fruit profile JSON structure to database schema.
    
    Args:
        profile_data: Fruit profile data from JSON
        
    Returns:
        Dict with database-compatible structure
    """
    # Map the JSON structure to database columns
    db_profile = {
        'fruit_id': profile_data.get('fruit_id'),
        'scientific_name': profile_data.get('scientific_name'),
        'description': profile_data.get('description'),
        'flavor_profile': profile_data.get('flavor_profile'),
        'jam_uses': profile_data.get('jam_properties'),  # Map jam_properties to jam_uses
        'season': profile_data.get('season'),
        'storage_tips': profile_data.get('storage_tips'),
        'nutrition': {
            'preparation': profile_data.get('preparation'),
            'country_of_origin': profile_data.get('country_of_origin'),
            'image_url': profile_data.get('image_url'),
            'jam_properties': profile_data.get('jam_properties')
        },
        'created_date': profile_data.get('created_date')
    }
    
    return db_profile

def insert_fruit_profile(connection, profile_data: Dict[str, Any]) -> bool:
    """
    Insert a fruit profile into the database.
    
    Args:
        connection: Database connection
        profile_data: Profile data to insert
        
    Returns:
        bool: True if successful, False otherwise
    """
    cursor = connection.cursor()
    
    try:
        # Check if profile already exists
        cursor.execute("SELECT fruit_id FROM profiles WHERE fruit_id = %s", (profile_data['fruit_id'],))
        if cursor.fetchone():
            print(f"[{get_timestamp()}] ⚠️  Profile for fruit_id {profile_data['fruit_id']} already exists, skipping")
            return False
        
        # Insert the profile (convert dicts to JSON strings for PostgreSQL)
        cursor.execute("""
            INSERT INTO profiles (
                fruit_id, scientific_name, description, flavor_profile, 
                jam_uses, season, storage_tips, nutrition, created_date
            ) VALUES (
                %(fruit_id)s, %(scientific_name)s, %(description)s, %(flavor_profile)s,
                %(jam_uses)s, %(season)s, %(storage_tips)s, %(nutrition)s, %(created_date)s
            )
        """, {
            'fruit_id': profile_data['fruit_id'],
            'scientific_name': profile_data['scientific_name'],
            'description': profile_data['description'],
            'flavor_profile': json.dumps(profile_data['flavor_profile']) if profile_data['flavor_profile'] else None,
            'jam_uses': json.dumps(profile_data['jam_uses']) if profile_data['jam_uses'] else None,
            'season': profile_data['season'][:50] if profile_data['season'] else None,
            'storage_tips': profile_data['storage_tips'],
            'nutrition': json.dumps(profile_data['nutrition']) if profile_data['nutrition'] else None,
            'created_date': profile_data['created_date']
        })
        
        connection.commit()
        return True
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Error inserting profile for fruit_id {profile_data['fruit_id']}: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()

def get_fruit_id_from_ai_identifier(connection, ai_identifier: str) -> Optional[int]:
    """
    Get fruit_id from ai_identifier.
    
    Args:
        connection: Database connection
        ai_identifier: AI identifier (e.g., 'strawberry', 'blueberry')
        
    Returns:
        int: fruit_id if found, None otherwise
    """
    cursor = connection.cursor()
    
    try:
        cursor.execute("SELECT id FROM fruits WHERE ai_identifier = %s", (ai_identifier,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Error getting fruit_id for {ai_identifier}: {e}")
        return None
    finally:
        cursor.close()

def import_fruit_profiles():
    """
    Import all fruit profiles from JSON files into the database.
    """
    print(f"[{get_timestamp()}] Starting fruit profile import...")
    
    # Get all JSON files in the fruit_profiles directory
    profile_files = glob.glob(os.path.join('fruit_profiles', '*.json'))
    profile_files.sort()  # Sort for consistent processing order
    
    if not profile_files:
        print(f"[{get_timestamp()}] ❌ No fruit profile JSON files found in fruit_profiles/ directory")
        return
    
    print(f"[{get_timestamp()}] Found {len(profile_files)} fruit profile files")
    
    connection = None
    
    try:
        # Connect to database
        connection = connect_to_database()
        
        imported_count = 0
        skipped_count = 0
        error_count = 0
        
        # Process each profile file
        for file_path in profile_files:
            filename = os.path.basename(file_path)
            fruit_name = os.path.splitext(filename)[0]
            
            print(f"[{get_timestamp()}] Processing {filename}...")
            
            # Load the profile data
            profile_data = load_fruit_profile(file_path)
            if not profile_data:
                error_count += 1
                continue
            
            # Get the fruit_id from the database using ai_identifier
            ai_identifier = fruit_name.replace('_', '_')  # Handle underscores in filenames
            fruit_id = get_fruit_id_from_ai_identifier(connection, ai_identifier)
            
            if not fruit_id:
                print(f"[{get_timestamp()}] ⚠️  Fruit '{ai_identifier}' not found in fruits table, skipping")
                error_count += 1
                continue
            
            # Update the profile data with the correct fruit_id
            profile_data['fruit_id'] = fruit_id
            
            # Map to database structure
            db_profile = map_profile_to_database(profile_data)
            
            # Insert into database
            if insert_fruit_profile(connection, db_profile):
                imported_count += 1
                print(f"[{get_timestamp()}] ✅ Imported profile for {fruit_name} (fruit_id: {fruit_id})")
            else:
                skipped_count += 1
        
        # Summary
        print(f"[{get_timestamp()}] ✅ Fruit profile import complete!")
        print(f"[{get_timestamp()}] Imported: {imported_count}")
        print(f"[{get_timestamp()}] Skipped: {skipped_count}")
        print(f"[{get_timestamp()}] Errors: {error_count}")
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Fruit profile import failed:")
        print(f"Error: {e}")
        raise
    finally:
        if connection:
            connection.close()
            print(f"[{get_timestamp()}] Database connection closed")

def verify_import():
    """
    Verify the import by checking how many profiles we have.
    """
    print(f"[{get_timestamp()}] Verifying import...")
    
    connection = None
    
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        
        # Count profiles
        cursor.execute("SELECT COUNT(*) FROM profiles")
        profile_count = cursor.fetchone()[0]
        
        # Count fruits
        cursor.execute("SELECT COUNT(*) FROM fruits")
        fruit_count = cursor.fetchone()[0]
        
        print(f"[{get_timestamp()}] Database now has {profile_count} profiles out of {fruit_count} fruits")
        
        # Show some examples
        cursor.execute("""
            SELECT f.fruit_name, p.scientific_name, p.season
            FROM fruits f
            LEFT JOIN profiles p ON f.id = p.fruit_id
            ORDER BY f.fruit_name
            LIMIT 10
        """)
        results = cursor.fetchall()
        
        print(f"[{get_timestamp()}] Sample profiles:")
        for fruit_name, scientific_name, season in results:
            status = "✅" if scientific_name else "❌"
            print(f"  {status} {fruit_name}: {scientific_name or 'No profile'}")
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Verification failed: {e}")
        raise
    finally:
        if connection:
            connection.close()

def main():
    """Main function."""
    print(f"[{get_timestamp()}] Fruit profile import script starting...")
    
    try:
        import_fruit_profiles()
        verify_import()
        print(f"[{get_timestamp()}] Script completed successfully!")
        
    except Exception as e:
        print(f"[{get_timestamp()}] ❌ Script failed:")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

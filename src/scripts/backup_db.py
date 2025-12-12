#!/usr/bin/env python3
"""
Database backup script.
Exports all collections to JSON files.
"""

import sys
import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config.settings import settings
from src.utils.logger import logger

def backup_database():
    """Backup MongoDB database using mongodump"""
    try:
        # Create backup directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = Path(f"backups/{timestamp}")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Starting database backup to {backup_dir}")
        
        # Run mongodump command
        cmd = [
            "mongodump",
            "--uri", settings.mongodb_uri,
            "--db", settings.master_db_name,
            "--out", str(backup_dir)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"✅ Backup completed successfully: {backup_dir}")
            
            # Create metadata file
            metadata = {
                "backup_timestamp": timestamp,
                "database": settings.master_db_name,
                "mongodb_uri": settings.mongodb_uri,
                "backup_dir": str(backup_dir),
                "size": get_directory_size(backup_dir)
            }
            
            metadata_file = backup_dir / "metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Metadata saved to: {metadata_file}")
            
            # Clean up old backups (keep last 7 days)
            cleanup_old_backups()
            
            return True
        else:
            logger.error(f"❌ Backup failed: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Backup error: {e}")
        return False

def get_directory_size(path):
    """Calculate directory size in MB"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return f"{total_size / (1024 * 1024):.2f} MB"

def cleanup_old_backups(days_to_keep=7):
    """Remove backups older than specified days"""
    try:
        backup_path = Path("backups")
        if not backup_path.exists():
            return
        
        from datetime import datetime, timedelta
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        for item in backup_path.iterdir():
            if item.is_dir():
                try:
                    # Extract timestamp from directory name
                    dir_timestamp = datetime.strptime(item.name.split('_')[0], "%Y%m%d")
                    
                    if dir_timestamp < cutoff_date:
                        import shutil
                        shutil.rmtree(item)
                        logger.info(f"Removed old backup: {item.name}")
                except (ValueError, IndexError):
                    continue
                    
    except Exception as e:
        logger.error(f"Error cleaning up old backups: {e}")

def list_backups():
    """List all available backups"""
    backup_path = Path("backups")
    if not backup_path.exists():
        print("No backups found")
        return
    
    print("Available backups:")
    print("-" * 60)
    for item in sorted(backup_path.iterdir()):
        if item.is_dir():
            size = get_directory_size(item)
            print(f"{item.name} - {size}")

if __name__ == "__main__":
    print("=" * 60)
    print("Organization Management Service - Database Backup")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_backups()
    else:
        if backup_database():
            print("\n✅ Backup completed successfully!")
        else:
            print("\n❌ Backup failed!")
            sys.exit(1)
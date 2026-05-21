"""
Database initialization script
Run this script to set up the database schema for AgentMemory
"""
import asyncio
import sys
import logging
from database import init_db, drop_db, close_db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main entry point for database setup"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "init":
            logger.info("Initializing database...")
            await init_db()
            logger.info("✓ Database initialization complete")
            
        elif command == "drop":
            confirm = input("⚠️  This will delete all tables. Type 'yes' to confirm: ")
            if confirm.lower() == "yes":
                await drop_db()
                logger.info("✓ All tables dropped")
            else:
                logger.info("Cancelled")
                
        elif command == "reset":
            confirm = input("⚠️  This will reset the database. Type 'yes' to confirm: ")
            if confirm.lower() == "yes":
                logger.info("Resetting database...")
                await drop_db()
                await init_db()
                logger.info("✓ Database reset complete")
            else:
                logger.info("Cancelled")
        else:
            print_help()
    else:
        print_help()
    
    await close_db()


def print_help():
    """Print help message"""
    print("""
    Usage: python init_db.py [command]
    
    Commands:
      init      Initialize database (create all tables)
      drop      Drop all tables (WARNING: destructive)
      reset     Drop and recreate all tables (WARNING: destructive)
      help      Show this message
    
    Example:
      python init_db.py init
    """)


if __name__ == "__main__":
    asyncio.run(main())

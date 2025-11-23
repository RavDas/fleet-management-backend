from app import create_app, db
from app.models.maintainance import MaintenanceItem
from app.utils.database_seeder import initialize_database, seed_database
import os
import logging
import threading
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Make shell context for flask shell command"""
    return {
        'db': db,
        'MaintenanceItem': MaintenanceItem
    }

@app.cli.command()
def init_db():
    """Initialize the database with tables"""
    db.create_all()
    print("Database tables created successfully!")

@app.cli.command()
def seed_db():
    """Seed database with sample data"""
    seed_database()

if __name__ == '__main__':
    # Initialize database with tables and sample data
    with app.app_context():
        try:
            logger.info("=" * 60)
            logger.info("🚀 Starting Maintenance Service")
            logger.info("=" * 60)
            initialize_database()
            logger.info("=" * 60)
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    # Start the Flask application
    port = int(os.environ.get('PORT', 5001))
    host = os.environ.get('HOST', '0.0.0.0')
    
    def heartbeat():
        """Log a heartbeat message every 10 seconds"""
        while True:
            logger.info("💓 Maintenance Service is alive and running...")
            time.sleep(10)

    # Start heartbeat in a background thread
    threading.Thread(target=heartbeat, daemon=True).start()

    logger.info(f"🌐 Starting server on {host}:{port}")
    app.run(
        host=host,
        port=port,
        debug=True
    )

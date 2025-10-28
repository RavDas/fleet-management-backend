from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    
    # Register blueprints
    from app.routes.maintenance_routes import maintenance_bp
    app.register_blueprint(maintenance_bp, url_prefix='/api/maintenance')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'maintenance-service'}, 200
    
    @app.route('/')
    def index():
        return {
            'service': 'Maintenance Management Service',
            'version': '1.0.0',
            'endpoints': {
                'health': '/health',
                'maintenance': '/api/maintenance/',
                'summary': '/api/maintenance/summary',
                'vehicle_history': '/api/maintenance/vehicle/<vehicle_id>/history'
            }
        }, 200
    
    return app
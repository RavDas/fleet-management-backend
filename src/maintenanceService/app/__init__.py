from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restx import Api
from config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configure CORS for all routes (including /health and /api/*)
    CORS(app, resources={
        r"/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize Flask-RESTX API with Swagger documentation
    api = Api(
        app,
        version='1.0.0',
        title='Fleet Management - Maintenance Service API',
        description='RESTful API for managing vehicle maintenance schedules, records, and tracking.\n\n'
                    '## Features\n'
                    '- Create, read, update, and delete maintenance items\n'
                    '- Filter and paginate maintenance records\n'
                    '- Track maintenance history by vehicle\n'
                    '- Generate summary statistics\n'
                    '- Automatic status updates based on due dates\n\n'
                    '## Authentication\n'
                    'Currently no authentication required (development mode)',
        doc='/docs',  # Swagger UI at /docs
        prefix='/api',
        contact='Fleet Management Team',
        contact_email='support@fleetmanagement.com',
    )
    
    # Register API namespaces (Flask-RESTX with Swagger)
    from app.routes.maintenance_api import api as maintenance_ns
    api.add_namespace(maintenance_ns, path='/maintenance')
    
    # Health check endpoint (outside API namespace)
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'maintenance-service'}, 200
    
    @app.route('/')
    def index():
        return {
            'service': 'Maintenance Management Service',
            'version': '1.0.0',
            'documentation': '/docs',  # Swagger UI
            'api_base': '/api',
            'endpoints': {
                'health': '/health',
                'swagger_ui': '/docs',
                'openapi_json': '/swagger.json',
                'maintenance': '/api/maintenance/',
                'summary': '/api/maintenance/summary',
                'vehicle_history': '/api/maintenance/vehicle/<vehicle_id>/history'
            }
        }, 200
    
    return app
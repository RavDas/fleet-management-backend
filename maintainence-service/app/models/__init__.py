from app.models.maintenance import MaintenanceItem


# from datetime import datetime
# from app import db

# class Maintenance(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     vehicle_id = db.Column(db.Integer, nullable=False)
#     maintenance_type = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
#     scheduled_date = db.Column(db.DateTime, nullable=False)
#     completed_date = db.Column(db.DateTime)
#     status = db.Column(db.String(50), default='SCHEDULED')
#     cost = db.Column(db.Float)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
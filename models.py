from database import db
from datetime import datetime

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    mime_type = db.Column(db.String(127))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def is_media(self):
        return self.mime_type and (
            self.mime_type.startswith('image/') or 
            self.mime_type.startswith('video/') or
            self.mime_type.startswith('audio/')
        )

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import app, db
import models

migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # Create a temporary table with the new structure
        with db.engine.connect() as conn:
            conn.execute(db.text('''
                CREATE TABLE file_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename VARCHAR(255) NOT NULL UNIQUE,
                    mime_type VARCHAR(127),
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            
            # Copy data from the old table to the new one
            conn.execute(db.text('''
                INSERT INTO file_new (id, filename, mime_type, upload_date)
                SELECT id, stored_name, mime_type, upload_date
                FROM file
            '''))
            
            # Drop the old table and rename the new one
            conn.execute(db.text('DROP TABLE file'))
            conn.execute(db.text('ALTER TABLE file_new RENAME TO file'))
            conn.commit()

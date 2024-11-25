from flask_migrate import Migrate, MigrateCommand
from app import app, db
import models

migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        if not db.engine.dialect.has_table(db.engine, 'file'):
            db.create_all()

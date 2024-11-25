import os
import logging
from flask import Flask, render_template, request, send_file, jsonify, abort
from werkzeug.utils import secure_filename
import mimetypes
import utils
from database import db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
# Ensure DATABASE_URL starts with postgresql://
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

try:
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'], mode=0o755)
    logger.info(f"Upload folder {app.config['UPLOAD_FOLDER']} is ready")
except Exception as e:
    logger.error(f"Error creating upload folder: {str(e)}")
    raise

db.init_app(app)

import models

def init_db():
    try:
        with app.app_context():
            db.create_all()
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

init_db()
File = models.File

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if not file or file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        original_name = secure_filename(file.filename if file.filename is not None else '')
        filename = utils.get_unique_filename(original_name, app.config['UPLOAD_FOLDER'])
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        mime_type = mimetypes.guess_type(filename)[0]
        
        new_file = File()
        new_file.filename = filename
        new_file.mime_type = mime_type
        
        db.session.add(new_file)
        db.session.commit()
        
        return jsonify({
            'url': f"/files/{filename}",
            'filename': filename
        })
    except Exception as e:
        logger.error(f"Error during file upload: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'An error occurred while uploading the file'}), 500

@app.route('/files/<filename>')
def view_file(filename):
    file_record = models.File.query.filter_by(filename=filename).first_or_404()
    
    if request.args.get('download'):
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], file_record.filename),
            as_attachment=True,
            download_name=file_record.filename
        )
    
    return render_template('view.html', file=file_record)

@app.route('/raw/<filename>')
def raw_file(filename):
    file_record = models.File.query.filter_by(filename=filename).first_or_404()
    return send_file(
        os.path.join(app.config['UPLOAD_FOLDER'], file_record.filename),
        mimetype=file_record.mime_type,
        as_attachment=True,
        download_name=file_record.filename
    )

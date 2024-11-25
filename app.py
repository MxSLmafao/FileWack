import os
from flask import Flask, render_template, request, send_file, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.utils import secure_filename
import mimetypes
import utils

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db.init_app(app)

with app.app_context():
    import models
    db.create_all()

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
        
        new_file = models.File(
            filename=filename,
            mime_type=mime_type
        )
        
        db.session.add(new_file)
        db.session.commit()
        
        return jsonify({
            'url': f"/files/{filename}",
            'filename': filename
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

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

import os
import mimetypes
from werkzeug.utils import secure_filename

def is_allowed_file(filename):
    """Check if the file type is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'pdf', 'txt'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_type(filename):
    """Get the mime type of a file"""
    return mimetypes.guess_type(filename)[0]

def generate_safe_filename(filename):
    """Generate a safe filename while preserving extension"""
    return secure_filename(filename)

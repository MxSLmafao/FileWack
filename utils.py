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

def get_unique_filename(original_filename, upload_folder):
    """
    Generate a unique filename by appending a number if the file already exists
    Returns: A unique filename that doesn't exist in the upload folder
    """
    base_name, extension = os.path.splitext(original_filename)
    counter = 1
    new_filename = original_filename
    
    while os.path.exists(os.path.join(upload_folder, new_filename)):
        new_filename = f"{base_name}({counter}){extension}"
        counter += 1
    
    return new_filename
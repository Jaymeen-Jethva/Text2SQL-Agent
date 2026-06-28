from pathlib import Path
import shutil

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def save_uploaded_file(uploaded_file):
    """
    save uploaded file locally to uploads folder
    """
    
    file_path = UPLOAD_DIR / uploaded_file.name
    
    with open(file_path, "wb") as f:
        shutil.copyfileobj(uploaded_file, f)
    
    return file_path
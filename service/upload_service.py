from pathlib import Path

from config import UPLOAD_DIR


def save_uploaded_file(uploaded_file):
    """
    Save the uploaded Streamlit file to the uploads folder.

    Parameters
    ----------
    uploaded_file : streamlit.runtime.uploaded_file_manager.UploadedFile

    Returns
    -------
    Path
        Local path of the saved file.
    """

    file_path = UPLOAD_DIR / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path
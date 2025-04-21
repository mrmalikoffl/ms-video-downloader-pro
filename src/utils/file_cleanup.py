import os

def cleanup_file(filename: str):
    """Delete the file if it exists."""
    if filename and os.path.exists(filename):
        try:
            os.remove(filename)
        except Exception as e:
            print(f"Failed to delete file {filename}: {e}")
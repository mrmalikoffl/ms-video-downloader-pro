import re

def is_valid_url(url: str) -> bool:
    """Check if the input is a valid URL."""
    pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.be|instagram\.com|x\.com|twitter\.com)/.+$"
    return bool(re.match(pattern, url))
# utils.py
import re

def slugify(name: str) -> str:
    """
    Converts 'My Business Name' into 'my-business-name'
    """
    return re.sub(r'\W+', '-', name.lower()).strip('-')

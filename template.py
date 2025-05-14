import os
from pathlib import Path
import logging

# Logging string
logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s:")

list_of_files = [
    "src/__init__.py",  # Constructor file for modular approach
    "src/helper.py",  # For developing functionality
    "src/prompt.py",  # For writing prompt
    "setup.py",
    "app.py",
    "src/__init__.py",
    "research/trials.ipynb",
    ".env",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} is already exists..!")

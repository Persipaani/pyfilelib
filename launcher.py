"""
A launcher that allows passing the database file path as a command line argument.
The passed file path is stored in db_config.py where it is fetched by the filebase database mock.
"""

import sys
import subprocess
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python launcher.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]
config_file = Path(__file__).parent / "db_config.py"

# Read the current config file.
lines = config_file.read_text(encoding="utf-8").splitlines()

# Write back the data in the config file changing only the FILE_PATH line.
with open(config_file, "w", encoding="utf-8") as f:
    for line in lines:
        if line.strip().startswith("FILE_PATH"):
            f.write(f'FILE_PATH = "{file_path}"\n')
        else:
            f.write(line + "\n")

# Launch the reflex app in the same directory.
subprocess.run(["reflex", "run"], cwd=Path(__file__).parent)

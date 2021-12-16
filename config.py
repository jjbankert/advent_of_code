import json
from pathlib import Path

with open(Path(__file__).parent / 'config.json', 'r', encoding='utf-8') as infile:
    config = json.load(infile)

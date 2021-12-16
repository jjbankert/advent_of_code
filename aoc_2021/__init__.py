from pathlib import Path
import requests
from config import config

data_folder = Path(__file__).parent / "data"


def load_data(python_file_path_string: str, splitlines=True):
    python_path = Path(python_file_path_string)

    file_path = data_folder / f"{python_path.stem}.txt"
    if not file_path.exists():
        day = file_path.stem.split('_')[0]
        year = data_folder.parent.stem.split('_')[-1]

        download_input(year, day, file_path)

    raw_data = file_path.read_text(encoding='utf-8')
    return [
        line for line in
        raw_data.splitlines()
        if line
    ] if splitlines else raw_data


def download_input(year, day, filepath):
    response = requests.get(
        f'https://adventofcode.com/{str(year)}/day/{str(day)}/input',
        cookies=config['cookies']
    )
    response.raise_for_status()

    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(response.text)

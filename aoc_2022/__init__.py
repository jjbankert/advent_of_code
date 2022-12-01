from pathlib import Path
import requests
from config import config

data_folder = Path(__file__).parent / "data"


def load_data(code_path: str, splitlines=True):
    data_path = get_data_path(code_path)
    if not data_path.exists():
        day = data_path.stem.split('_')[0]
        year = data_folder.parent.stem.split('_')[-1]

        download_input(year, day, data_path)

    raw_data = data_path.read_text(encoding='utf-8')
    return [
        line for line in
        raw_data.splitlines()
        if line
    ] if splitlines else raw_data


def get_data_path(code_path, suffix='txt'):
    return data_folder / f"{Path(code_path).stem}.{suffix}"


def download_input(year, day, filepath):
    response = requests.get(
        f'https://adventofcode.com/{str(year)}/day/{str(day)}/input',
        cookies=config['cookies']
    )
    response.raise_for_status()

    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(response.text)

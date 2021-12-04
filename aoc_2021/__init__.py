from pathlib import Path

data_folder = Path(__file__).parent / "data"


def load_data(python_file_path_string: str, splitlines=True):
    python_path = Path(python_file_path_string)

    raw_data = (data_folder / f"{python_path.stem}.txt").read_text(encoding='utf-8')
    return [
        line for line in
        raw_data.splitlines()
        if line
    ] if splitlines else raw_data

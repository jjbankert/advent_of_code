from pathlib import Path

data_folder = Path(__file__).parent / "data"


def load_data(python_file_path_string: str):
    python_path = Path(python_file_path_string)

    return [
        line for line in
        (data_folder / f"{python_path.stem}.txt").read_text(encoding='utf-8').splitlines()
        if line
    ]

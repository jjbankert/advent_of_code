from collections import Counter
from itertools import combinations
import sqlite3
import numpy as np
import pandas as pd
from pathlib import Path
from aoc_2021 import load_data, get_data_path


def main():
    raw_scanners_data = load_data(__file__, splitlines=False).split('\n\n')
    scanners_data = dict(parse_scanner_data(raw_scanner_data) for raw_scanner_data in raw_scanners_data)

    database = setup_db()

    for scanner, beacons in scanners_data.items():
        cursor = database.cursor()
        distances = get_scanner_beacon_distances(scanner, beacons)
        cursor.executemany(
            """
            INSERT INTO distances VALUES (?,?,?,?)
            """,
            distances
        )

    # distance_occurence = pd.DataFrame(scanners_beacon_distances.groupby('distance')['scanner'].apply(Counter))
    pass

    database.close()


def setup_db():
    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()

    # create table
    cursor.execute("""
        CREATE TABLE distances
        (scanner text, beacon_a_idx text, beacon_b_idx text, distance real)        
    """)

    connection.commit()
    return connection


def parse_scanner_data(data: str) -> (str, np.array):
    header, *raw_observations = data.strip().split('\n')

    observations = [tuple(np.fromstring(row, sep=',')) for row in raw_observations]
    return header.split()[2], observations


def get_scanner_beacon_distances(scanner, beacons) -> pd.DataFrame:
    scanner_beacon_distances = []

    for beacon_a_idx, beacon_b_idx in combinations(range(len(beacons)), 2):
        beacon_a = beacons[beacon_a_idx]
        beacon_b = beacons[beacon_b_idx]
        distance = euclidean_distance(beacon_a, beacon_b)
        scanner_beacon_distances.append(
            pd.DataFrame(
                [[scanner, beacon_a_idx, beacon_b_idx, distance]],
                columns=['scanner', 'beacon_a_idx', 'beacon_b_idx', 'distance'])
        )

    return pd.concat(scanner_beacon_distances, ignore_index=True)


def euclidean_distance(one, other) -> float:
    return np.linalg.norm(np.array(one) - np.array(other))


if __name__ == '__main__':
    main()

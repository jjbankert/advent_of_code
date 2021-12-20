import numpy as np
from scipy import ndimage

from aoc_2021 import load_data


def main():
    # preprocessing
    lookup_table, _, *image = load_data(__file__)
    lookup_table = [pixel_to_binary(pixel) for pixel in lookup_table]
    image = np.array(
        [[pixel_to_binary(pixel) for pixel in row] for row in image],
        dtype=int
    )

    # part 1
    image = enhance(image, lookup_table, 2)
    display_image(image)

    # part 2
    image = enhance(image, lookup_table, 48)
    display_image(image)


def binary_to_pixel(pixel: int) -> str:
    return '#' if pixel else '.'


def pixel_to_binary(pixel: str) -> int:
    return 0 if pixel == '.' else 1


def enhance(image, lookup_table, iterations):
    window_size = 3
    border = 0
    for _ in range(iterations):
        # add a border of 2 pixels outside the current image, the other infinite pixels are captured in 'border'
        image = np.pad(image, window_size - 1, constant_values=border)

        # apply filter to image
        image = ndimage.generic_filter(
            image,
            function=lookup_filter,
            size=(window_size, window_size),
            mode='constant',
            cval=border,
            extra_arguments=(lookup_table,)
        )

        # apply filter to border
        border = lookup_table[0] if border == 0 else lookup_table[-1]

        # trim the top, bottom, left and right sides that are the same as the infinite border
        image = trim(image, border)

    return image


def lookup_filter(window, lookup_table):
    idx = int(''.join(str(round(pixel)) for pixel in window), 2)
    return lookup_table[idx]


def trim(image, border):
    while np.all(image[0, :] == border):
        image = image[1:, :]
    while np.all(image[-1, :] == border):
        image = image[:-1, :]
    while np.all(image[:, 0] == border):
        image = image[:, 1:]
    while np.all(image[:, -1] == border):
        image = image[:, :-1]
    return image


def display_image(image):
    print()
    print('\n'.join([''.join([binary_to_pixel(pixel) for pixel in row]) for row in image]))
    print(int(np.sum(image)))


if __name__ == '__main__':
    main()

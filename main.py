import os
import sys

import cv2 as cv
import pandas as pd


def merge_channels(input_dir, output_dir):
    with open(os.path.join(input_dir, 'image_counter.txt'), 'r') as file:
        image_counter = int(file.read())
    description = pd.read_csv(os.path.join(input_dir, "description.csv"))

    images = dict()

    for _, row in description.iterrows():
        index = int(row["full_image_index"])
        color = row["color"]
        image_path = row["image_path"]
        colors = ["b", "g", "r"]
        index_of_color = colors.index(color)
        if index not in images:
            images[index] = dict()
        images[index][color] = cv.split(  # noqa
            cv.imread(os.path.join('input', 'data', image_path)))[index_of_color]  # noqa

    i = 0
    for key, item in images.items():
        if i == image_counter:
            break
        image = cv.merge((item["b"], item["g"], item["r"]))  # noqa
        cv.imwrite(os.path.join(output_dir, f"{key}.jpg"), image)  # noqa
        i += 1


merge_channels(*sys.argv[1:])

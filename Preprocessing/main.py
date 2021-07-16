import argparse


import path
import plot


def _get_cmd_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--image-dir',
        default='images',
        help='Directory to the image library.'
    )
    parser.add_argument(
        '--flatten',
        action='store_true',
        help='Flatten the subdirectories within the image directory. Not implemented.'
    )
    parser.add_argument(
        '--label-dir',
        default='labels',
        help='The directory to store the labels.'
    )
    cmd_args = parser.parse_args()
    return cmd_args


def main():
    cmd_args = _get_cmd_args()
    image_dir = cmd_args.image_dir
    flatten = cmd_args.flatten
    label_dir = cmd_args.label_dir

    image_paths = path.get_image_paths(image_dir)
    for image_path in image_paths:
        plot.cv2_imshow(image_path)

    return


if __name__ == '__main__':
    main()
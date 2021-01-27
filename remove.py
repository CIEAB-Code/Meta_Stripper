import piexif
from os import scandir
import argparse

parser = argparse.ArgumentParser(description="Remove exif data from JPEG image files.")
parser.add_argument('--directory', '-d', type=str, metavar='',
                    help="Enter path with / separators to directory containing JPEG files.")
args = parser.parse_args()


def remove_meta(path):
    """Removes exif data from JPEG image files."""
    count = 0
    length_images = 0

    try:
        images = [image.name for image in scandir(path) if '.JPG' in image.name]
        length_images = len(images)
        for image in images:
            image_path = f"{path}/{image}"
            data = piexif.load(image_path, key_is_name=False)
            # print(data)
            piexif.remove(image_path)
            data = piexif.load(image_path, key_is_name=False)
            print(image, data)
            count += 1
    except Exception as e:
        print(e)

    print(f"Removed exif data from {count} of {length_images} images.")


if __name__ == '__main__':

    if args.directory:
        path = args.directory
        remove_meta(path)
    else:
        print("Please enter path to directory of JPEG images using : '--directory' or '-d' ")

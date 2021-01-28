import piexif
from os import scandir
import argparse

parser = argparse.ArgumentParser(description="Remove exif data from JPEG image files.")
parser.add_argument('--directory', '-d', type=str, metavar='',
                    help="Enter path with / separators to directory containing JPEG files.")
parser.add_argument('--verbose', '-v', action='store_true',
                    help="Print dictionary of exif data before and after it is removed.")
args = parser.parse_args()

# Default values for argparse options
verbose = False


def remove_meta(path):
    """Removes exif data from JPEG image files."""
    count = 0
    length_images = 0
    data_dict = {}
    deleted_data = {}

    try:
        images = [image.name for image in scandir(path) if '.JPG' in image.name]
        length_images = len(images)
        for image in images:
            image_path = f"{path}/{image}"

            dct = piexif.load(image_path, key_is_name=False)
            dct.pop('thumbnail')
            dct.pop('Exif')
            data_dict[image] = dct

            piexif.remove(image_path)
            data = piexif.load(image_path, key_is_name=False)
            deleted_data[image] = data
            count += 1
    except Exception as e:
        print(e)

    if verbose:
        print("\nBEFORE DATA REMOVED (exif and thumbnail not shown): \n")
        for key, value in data_dict.items():
            print(f"{key}: {value}")

        print("\nAFTER DATA REMOVED: \n")
        for key, value in deleted_data.items():
            print(f"{key}: {value}")

    print(f"\nRemoved exif data from {count} of {length_images} images.")


if __name__ == '__main__':

    if args.directory:
        path = args.directory
        if args.verbose:
            verbose = True
        remove_meta(path)
    else:
        print("Please enter path to directory of JPEG images using : '--directory' or '-d' ")


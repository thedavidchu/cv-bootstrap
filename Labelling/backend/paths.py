import os


def standardize_path(path: str) -> str:
    """ Convert a path into its absolute version. Remove redundant slashes
        and convert to a consistent formatting. """
    # Bring the path to a consistent format
    path = os.path.abspath(path)  # Makes absolute path
    path = os.path.normpath(path)  # Convert to consistent format
    path = os.path.normcase(path)  # Convert to consistent case
    return path


if __name__ == '__main__':
    TEST_IMG_FILE_PATH: str = "../../data/images/airplane/1.jpg"

    print(standardize_path(TEST_IMG_FILE_PATH))

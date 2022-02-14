import main as m


TEST_IMG_DIR_PATH: str = "data/images/"


def delete_jsons():
    """Delete all JSONs associated with the test labels. This file is not called
    by default."""
    import os

    for directory in ["airplane", "cat", "dog", "truck"]:
        for file in ["1.json", "2.json", "3.json"]:
            full_path = os.path.join(TEST_IMG_DIR_PATH, directory, file)
            os.remove(full_path)


def main():
    app = m.App()
    app.bottom_tool_bar.line_width.set(1)
    # Open image (from main.add_img_dir())
    app.backend.image_paths.load_dir(TEST_IMG_DIR_PATH)
    app.setup_images()
    # Run app
    app.root.mainloop()


if __name__ == "__main__":
    main()

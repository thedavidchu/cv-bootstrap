import main as m


TEST_IMG_DIR_PATH: str = "data/images/"


def main():
    app = m.App()
    app.bottom_tool_bar.line_width.set(1)

    # Open image (from main.add_img_dir())
    app.backend.image_paths.load_dir(TEST_IMG_DIR_PATH)
    app.bottom_tool_bar.renew_progress_bar()
    app.workspace.display_image(app.backend.image_paths.get_image())

    # Run app
    app.root.mainloop()


if __name__ == "__main__":
    main()

import main as m


TEST_IMG_DIR_PATH: str = "data/images/"


def main():
    app = m.App()
    app.backend.image_paths.load_dir(TEST_IMG_DIR_PATH)
    app.bottom_tool_bar.line_width.set(1)
    app.workspace.display_image(app.backend.image_paths.get_image())
    app.root.mainloop()


if __name__ == "__main__":
    main()

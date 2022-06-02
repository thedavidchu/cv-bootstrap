Instructions
============
Welcome to the ArtisticCV instructions.

1 - Installation
----------------
The steps to install the basic programs necessary include:
1. Install Python 3.8 or higher (it should work on Python 3.6+, but don't quote me on this)
    1. Go to the [Python download page](https://www.python.org/downloads/)
    2. Download your desired version of Python (you might as well get Python 3.10)
2. Install Git
    1. Follow the instructions on [this website](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

2 - Setup
---------
The steps to setting up this repository include:

1. Clone this repository
    > ```bash
    > # In your terminal (enter the following line-by-line, replacing where necessary):
    > cd <path-to-your-directory>
    > git clone https://github.com/thedavidchu/ArtisticCV.git
    > ```
2. **OPTIONAL** Setting up a Virtual Environment
    * Why set up a virtual environment?
        * A virtual environment is a way to keep all of the Python packages you download for this project separate from packages you may use in other projects. This means: (1) this project is easier to delete (just delete the virtual environment and all of the project files, instead of uninstalling all the packages manually), (2) prevents you having to sort through different dependency  
    * Read the HOW-TO instructions [on Python's virtual environment](https://docs.python.org/3/tutorial/venv.html)
3. Install the requirements with `pip install -r requirements.txt` (don't quote me on this)
    > ```bash
    > # In your terminal (enter the following line-by-line):
    > cd ArtisticCV
    > pip install -r requirements.txt   # Assuming pip is installed. If not, install it!
    > ```
4. Setup the configuration file in `config.json` by adding your name in the empty quotes beside author
    * This is to keep track of who labelled which data.
    * The file should like like so, after inserting one's first and last names:
    > ```json
    > {
    > "author": "<First-Name> <Last-Name>"
    > }
    > ```

3 - Running
-----------
1. Run `main.py` with Python
    > ```bash
    > # In your terminal (enter one):
    > python3 main.py   # Your python version may be called just "python"
    > ```
2. Maximize the window for optimal experience (NOTE: if you have a small screen, this will be painful-- or may not work at all!)
3. Click on `File -> Open directory` (note: trying to do this multiple times in the same run will cause an error)
4. Select the directory of images you wish to label (there is a convenient directory named "data" that you may use for this purpose. It has some test images in it).
    * Note: we save the labels to this file, so make sure you have write permission!
5. Happy labelling!

4 - Data Labelling
------------------
  
### Adding Label Points
* Click on the image to lay a point
  
### Modes
**UTRA-ART People: You only need to use the Polygon mode -- N.B. that hitting 'Enter' closes the Polygon for you!!**
  
The various modes are:

1. Cursor (supposed to do nothing, but lays invisible points)
2. Point (lays visible point marks)
3. Line (lays a multi-line)
4. Polygon (lays a polygon, snaps closed upon hitting 'Enter') \[Default\]

### Keyboard Commands
* '\>' : Save labels and advance to the next image (N.B. you do not need to hit ctrl+s before advancing. It will save automatically with this shortcut!)
* '\<' : Save labels and go to the previous image
* BackSpace : Remove the previously laid point of the current label (if applicable)
* Delete : Remove the entire currently selected label
* Enter : Create a new label on the current image
* Right Arrow : Go to the next label
* Left Arrow : Go to the previous label
* Ctrl + 's' : Save the labels on the current image

### Exporting Labels
You can copy the labels to another folder, keeping the file structure the same.

1. Click on `File -> Export Labels`
2. A window will pop up. Select the source folder
3. A window will pop up. Select the destination folder
4. Double check that the labels are correctly moved!

5 - Reporting Bugs and Asking for Features
------------------------------------------
* Report bugs/feature requests to David Chu (file an Issue on github)
* Help maintaining is always welcome!

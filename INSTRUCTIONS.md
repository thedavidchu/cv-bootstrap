Instructions
============
Welcome to the ArtisticCV instructions.

Setup
-----
The steps to setting up this repository include:

1. Install the requirements with `pip install -r requirements.txt` (don't quote me on this)
2. Setup the configuration file in `config.json`


Running
-------

1. Run `main.py`
2. Click on `File -> Open directory` (note: trying to do this multiple times in the same run will cause an error)
3. Select the directory of images you wish to label
4. Happy labelling!


Modes
-----
The various modes are:

1. Cursor (supposed to do nothing, but lays invisible points)
2. Point (lays visible point marks)
3. Line (lays a multi-line)
4. Polygon (lays a polygon, snaps closed upon hitting 'Enter') \[Default\]

Keyboard Commands
-----------------
* '>' : Save labels and advance to the next image
* '<' : Save labels and go to the previous image
* BackSpace : Remove the previously laid point of the current label (if applicable)
* Delete : Remove the entire currently selected label
* Enter : Create a new label on the current image
* Right Arrow : Go to the next label
* Left Arrow : Go to the previous label
* Ctrl + 's' : Save the labels on the current image

Exporting Labels
----------------
You can copy the labels to another folder, keeping the file structure the same.

1. Click on `File -> Export Labels`
2. A window will pop up. Select the source folder
3. A window will pop up. Select the destination folder
4. Double check that the labels are correctly moved!

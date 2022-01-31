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
2. Click on `File -> Open dir`
3. Select the directory of images you wish to label
4. Happy labelling!


Modes
-----
The various modes are:

1. Cursor (supposed to do nothing, but lays invisible points)
2. Point (lays visible point marks)
3. Line (lays a multi-line)
4. Polygon (lays a polygon, snaps closed upon hitting 'Enter')
    
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

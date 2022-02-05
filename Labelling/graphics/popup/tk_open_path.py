"""
# Open Paths

## Contents of This File
The functions herein open a file/directory using a dialog box.

**Inputs**
All inputs are **kwargs.
    - parent - the window to place the dialog on top of
    - title - the title of the window
    - initialdir - the directory that the dialog starts in
    - initialfile - the file selected upon opening of the dialog
    - filetypes - a sequence of (label, pattern) tuples, ‘*’ wildcard is allowed
    - defaultextension - default extension to append to file (save dialogs)
    - multiple - when true, selection of multiple items is allowed
See https://docs.python.org/3/library/dialog.html#native-load-save-dialogs

**Outputs**
dir_path: str
    path to the chosen directory

***

## Note on Decorators
This file uses decorators. Decorators are just syntactic sugar for "wrapping"
a function. For example, consider we are given the following:
```
def decorator(func):
    def wrapper(arg):
        do_something_to_start()
        r = func(arg)   # Note: closure allows us to access func
        do_something_to_finish()
        return r
    return wrapper
```

Applying a decorator as such:
```
@decorator
def func(arg):
    return do_something_in_the_middle(arg)
```

is equivalent to the following:
```
def func(arg):
    return do_something_in_the_middle(arg)

func = decorator(func)
```

Knowing this, you can derive other use cases.
"""

import functools
import tkinter as tk
import tkinter.filedialog  # Necessary
from typing import Tuple


def _initial_directory(initialdir: str = None):
    """Change the initially opened directory to the argument `initialdir`.

    ## Notes
    1. The leading underscore in this functions name denotes the fact that it
        is a private function. It should not be accessed outside of this file.
    2. This function is called using _decorators_. See my note above for an
        explanation. I admit that my use of decorators is a little bit overkill
        for what I am trying to accomplish. I apologize, but it was fun."""
    def decorator_initial_directory(func_with_kwargs):
        # This renames wrapper to the function it wraps
        @functools.wraps(func_with_kwargs)
        def wrapper(**kwargs):
            if "initialdir" not in kwargs and initialdir is not None:
                kwargs["initialdir"] = initialdir
            return func_with_kwargs(**kwargs)
        return wrapper
    return decorator_initial_directory


@_initial_directory("/data")
def tk_open_dir(**kwargs) -> str:
    dir_path = tk.filedialog.askdirectory(**kwargs)
    return dir_path


@_initial_directory("/data")
def tk_open_files(**kwargs) -> Tuple[str]:
    file_paths = tk.filedialog.askopenfilenames(**kwargs)
    return file_paths


if __name__ == '__main__':
    root = tk.Tk()
    dir_path = tk_open_dir()
    file_paths = tk_open_files()
    tk.mainloop()

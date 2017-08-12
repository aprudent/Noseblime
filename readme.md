# Nose plugin for Sublime Text

## About
Run Python tests using [Nose2](http://nose2.readthedocs.io/en/latest/) or [Nose](http://nose.readthedocs.io/en/latest/) from Sublime Text 3.


## Features

* run all tests in files or folders from the side bar
* run some or all tests from the current view
* capture error from Nose output for navigation


## Installation

1. [Download the plugin archive](https://github.com/aprudent/Noseblime/releases/download/1.0.0/Noseblime.sublime-package.zip)
2. Extract the archive into the Sublime Text **Packages** directory, which you can find using the menu item `Preferences → Browse Packages...`


## Using

The Nose actions are only visible for files or folders that are recognized as possible Python tests entries.
By default, actions are available, if:

* a file's full path contains **test** or **Test** and its extension is **.py**,
* a folder's full path contains **test** or **Test**.

The keys `test_file_regex` and `test_dir_regex` of the Noseblime package settings, can override the default recognition patterns.  

### SideBar

Right click on the file(s) or folder(s) to run Nose on those.

### View

Right click on the view, or use the `Command Palette`.

The position of the carets in the view will determine which test(s) to run with Nose. If a caret is inside:

* a class's method, only this method will run,
* a class declaration, this class will run,
* before any class declaration, the file will run.


## Requirements

Sublime Text 3 version 3124 or above is required.
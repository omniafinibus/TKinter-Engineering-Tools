# tkinter tools

A collection of useful methods to configure tkinter and ttk widgets with.
It also adds several custom widgets to make developing technical GUI's easier

## Authors

- Arjan Lemmens

## Scripts

### build_docs

This script automatically updates the toc trees related to the package.
After which it generates the HTML and LaTeX files based on the comments in this packages source code using sphinx.
NOTE: Before this script can be run, the sphinx-quickstart should be run(If not done already), where all of its output files are
placed in the ./docs/sphinx/ directory

### image_encoder

This script converts any PNG file in the ./assets/ directory into an base64 string and saves these strings to the
./tkinter_tools/resources/_encoded_images.py.
This is done to embed the images and make a single file package possible.

### Installation

To install the tkinter tools packages, run one of the following scripts:
- ./scripts/install_global.py     Installs the package in the global python environment
- ./scripts/install_venv.py   Installs the package in the virtual environment dedicated to GUI development
- ./scripts/install_everywhere.py Do all of the above

NOTE: Before attempting to install this package, if assets have been added, the image encoder first needs to be run

## Requirements

* Pillow >= 10.0.0

## Added tools

- Lists
    - WidgetList: Provides a lists of rows where all entries have the same widgets.
    - ListEntry: A single row of widgets with some added functionality, used by WidgetList.
    - WidgetMatrix: A matrix of the same type of widget, sorted by the value inside them.
- Widgets
    - Button: Button which uses the Callback set and supports dark and light mode images.
    - EntryLabelPair: Widget which can toggle between an entry and a label (showing the value of the Entry).
    - SelectionLabelPair: Widget which can toggle between an OptionMenu and a label (showing the value of the OptionMenu).
    - ValueUnitPair: Widget which can toggle between a label and an Entry paired with and OptionMenu (The label shows the value of the entry and OptionMenu combined).
- Frames
    - ScrollableFrame: Frame which provides a scrolling feature.
    - ScrollableLabelFrame: LabelFrame which provides a scrolling feature.
- Callbacks
    - CallbackSets: Set of callbacks which are sorted by a key like a dict but ordered like a list.
    - FancyCallbacks: A hybrid of a lambda and method.
- Methods
    - set_widget_position: Places a widget with the grid manager with reference to another widget.
    - is_widget_this: Check if a widget is of a specific type.
    - is_widget_this_list: Check if a widget is of a specific type present in a list.
    
## Naming conventions

- Data types
    - myVariable
    - gMyGlobalVariable
    - lMyListVariable
    - dMyDictionairy
    - tMyTuple
    - sMyString
    - MY_CONSTANT_DEFINITION
    - ldMyListHoldingDictionaries
- Objects
    - MyClass
- Other
    - my_file.py
    - my_function
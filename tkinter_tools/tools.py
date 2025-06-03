# ==================================================================== #
#  File name:      tools.py                     #        _.==._        #
#  Author:         Arjan Lemmens                #     .+=##**##=+.     #
#  Date:           11-May-2023                  #    *= #        =*    #
# ============================================= #   #/  #         \#   #
#  Description:    Methods to providing extra   #  |#   #   $      #|  #
#                  functionality for using      #  |#   #   #      #|  #
#                  tkinter widgets and weird    #   #\  #   #     /#   #
#                  widgets.                     #    *= #   #    =+    #
#  Rev:            2.0                          #     *++######++*     #
#                                               #        *-==-*        #
# ==================================================================== #
#  Revision history:                                                   #
#  Date        Description                                             #
#  22-Feb-2023 File created                                            #
#  28-Feb-2023 Several methods added                                   #
#  11-May-2023 Cleaned code and added comments                         #
# ==================================================================== #
#  To-Do: !=Priority, ~=Bug, ?=Idea/nice to have                       #
#                                                                      #
# ==================================================================== #

# =========== #
#   Imports   #
# =========== #
import tkinter as tk
from tkinter import ttk
from tkinter_tools.composite_widgets import EntryLabelPair, Button, ValueUnitPair, SelectionLabelPair

# =============== #
#   Definitions   #
# =============== #
# Used for widget recognition
WIDGET_LABEL = "label"
WIDGET_ENTRY = "entry"
WIDGET_BUTTON = "button"
WIDGET_TKT_BUTTON = "tktButton"
WIDGET_FRAME = "frame"
WIDGET_CHECK_BUTTON = "checkButton"
WIDGET_SELECTION_LABEL = "selectionLabel"
WIDGET_ENTRY_LABEL = "entryLabel"
WIDGET_VALUE_UNIT = "valueUnit"

# =========== #
#   Methods   #
# =========== #
def set_widget_position(widget, reference, columnOffset:int, rowOffset:int, **kwargs):
    """
    Place a widget in its parent frame with respect to a reference.
    The widget is placed using tkinter's grid geometric manager. 
    Other grid options can also be set for the widget

    :param widget: Widget to change the location of
    :type widget: tkinter, ttk, or weird_widget widget
    :param reference: Reference widget which acts as the reference (acts as row=0, column=0)
    :type reference: tkinter, ttk, or weird_widget widget
    :param columnOffset: Offset from the reference column (can be negative to move left from reference)
    :type columnOffset: integer
    :param rowOffset: Offset from the reference row (can be negative to move up from reference)
    :type rowOffset: integer
    """    
    # Required for widgets using itself as a reference, and allows other settings to be set
    widget.grid(**kwargs)

    widget.grid(
        column=reference.grid_info()["column"] + columnOffset,
        row=reference.grid_info()["row"] + rowOffset,
    )  # Set the row and column with reference to the reference

def is_widget_this(widget, this:str):
    """
    Check if a widget is of a specific type

    :param widget: Widget to check the type of
    :type widget: tkinter, ttk, or weird_widget widget
    :param this: Widget type to compare too, requires the use of tkinter_tools definitions
    :type this: string
    :return: If the widget is indeed of the "this" type
    :rtype: boolean
    """
    # Compare to the correct widget type
    if this == WIDGET_LABEL:
        return isinstance(widget, tk.Label) or isinstance(widget, ttk.Label)
    elif this == WIDGET_ENTRY:
        return isinstance(widget, tk.Entry) or isinstance(widget, ttk.Entry)
    elif this == WIDGET_BUTTON:
        return isinstance(widget, tk.Button) or isinstance(widget, ttk.Button)
    elif this == WIDGET_TKT_BUTTON:
        return isinstance(widget, Button)
    elif this == WIDGET_FRAME:
        return isinstance(widget, tk.Frame) or isinstance(widget, ttk.Frame)
    elif this == WIDGET_ENTRY_LABEL:
        return isinstance(widget, EntryLabelPair)
    elif this == WIDGET_VALUE_UNIT:
        return isinstance(widget, ValueUnitPair)
    elif this == WIDGET_SELECTION_LABEL:
        return isinstance(widget, SelectionLabelPair)
    elif this == WIDGET_CHECK_BUTTON:
        return isinstance(widget, tk.Checkbutton) or isinstance(widget, ttk.Checkbutton)
    else:
        return False

def is_widget_this_list(widget, *lThis):
    """
    Check if a widget falls in a list of widgets

    :param widget: Widget to check the type of
    :type widget: ttk, tkinter, weird_widget widgets
    :param lThis: List of tkinter_tools definitions of widget type to compare too
    :type lThis: list
    :return: If the widgets type is found in the lThis list
    :rtype: boolean
    """
    
    # Comparer the widget to each item chosen
    for item in lThis:
        if is_widget_this(widget, item):
            return True

    # Non were found so return false
    return False
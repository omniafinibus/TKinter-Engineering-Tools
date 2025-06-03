# ==================================================================== #
#  File name:      selection_label_pair.py      #        _.==._        #
#  Author:         Arjan Lemmens                #     .+=##**##=+.     #
#  Date:           26-May-2023                  #    *= #        =*    #
# ============================================= #   #/  #         \#   #
#  Description:    Custom composite dropdown    #  |#   #   $      #|  #
#                  label widget.                #  |#   #   #      #|  #
#  Rev:            1.0                          #   #\  #   #     /#   #
#                                               #    *= #   #    =+    #
#                                               #     *++######++*     #
#                                               #        *-==-*        #
# ==================================================================== #
#  Revision history:                                                   #
#  Date        Description                                             #
#  02-Mar-2023 File created                                            #
#  03-Mar-2023 Commented all methods                                   #
#  06-Mar-2023 Bug fixes for complete overhaul                         #
#  13-Mar-2023 First release                                           #
#  11-May-2023 Cleaned up code and added comments                      #
#  26-May-2023 Migrate from shared composite_widgets file              #
# ==================================================================== #
#  To-Do: !=Priority, ~=Bug, ?=Idea/nice to have                       #
#                                                                      #
# ==================================================================== #

# =========== #
#   Imports   #
# =========== #
import tkinter as tk
from tkinter import ttk

# =========== #
#   Classes   #
# =========== #

class SelectionLabelPair:
    """A set of 2 widgets, a label and an OptionMenu.
    The label will show what has been selected in the option menu.
    Only 1 of the 2 widgets is visible since they will be toggled.
    """

    def __init__(self, parent=None, value:str="", lValues=None, command=None, **kwargs):
        """Constructor

        :param parent: Parent tkinter frame in which this widget will be placed, defaults to None
        :type parent: tkinter frame, optional
        :param value: Initial value to which the selectionMenu will be set, defaults to ""
        :type value: any, optional
        :param lValues: List of values to be shown in the lValues, defaults to list()
        :type lValues: list, optional
        :param command: command to run when the selectionMenu is changed, defaults to None
        :type command: function, optional
        """

        self.value = tk.StringVar(parent)
        """ Tkinter variable for holding the selected value """

        # Text shown is based on the value of self.value
        self.label = ttk.Label(parent, textvariable=self.value)
        """ Tkinter label """
        self.label.grid(**kwargs)

        lValues = [""] if lValues is None or len(lValues) < 1 else lValues

        self.selectionMenu = ttk.OptionMenu(
            parent, self.value, lValues[0], *lValues, command=command if command is not None else self.set)
        """ Tkinter option menu """

        # Set value of the option menu and label
        self.value.set(str(value))
        self.selectionMenu.grid(**kwargs)

    def __del__(self):
        """Destructor"""
        try:
            self.label.destroy()
            self.selectionMenu.destroy()
        except:
            pass

    def grid_info(self):
        """Return information about the options for positioning this widget in a grid"""
        return self.label.grid_info()

    def grid(self, **kwargs):
        """Position a widget in the parent widget in a grid. Use as options:
        column=number - use cell identified with given column (starting with 0)
        columnspan=number - this widget will span several columns
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        row=number - use cell identified with given row (starting with 0)
        rowspan=number - this widget will span several rows
        sticky=NSEW - if cell is larger on which sides will this
                      widget stick to the cell boundary
        """
        self.label.grid(**kwargs)
        self.selectionMenu.grid(**kwargs)

    def grid_remove(self):
        """Unmap this widget but remember the grid options"""
        self.label.grid_remove()
        self.selectionMenu.grid_remove()

    def show_label(self):
        """Show label and hide the selectionMenu"""
        self.selectionMenu.grid_remove()
        self.label.grid()

    def show_input(self):
        """Show selectionMenu and hide the label"""
        self.selectionMenu.grid()
        self.label.grid_remove()
        
    def set_options(self, lNewOptions:list[str], value:str=None):
        """
        set_options Update the options shown in the selection menu

        :param lNewOptions: List of new options
        :type lNewOptions: list[string]
        :param value: value to set the option menu too, defaults to None
        :type value: string, optional
        """        
        self.selectionMenu.set_menu(value, *lNewOptions) 

    def set(self, text:str=""):
        """set Set the text of the label and selectionMenu

        :param text: Text to set the label to
        :type text: string
        """
        self.value.set(str(text))

    def get(self):
        """get Get the input string from the entry

        :return: Selected data in SelectionMenu
        :rtype: string
        """
        return self.value.get()
    
    def __repr__(self):
        """
        Representation of this class when it is printed or viewed in debugger window

        :return: String of how this object should be represented
        :rtype: string
        """
        f"label: {self.label}\nselectionMenu: {self.selectionMenu}\nvalue: {self.value.get()}"
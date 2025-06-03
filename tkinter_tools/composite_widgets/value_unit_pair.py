# ==================================================================== #
#  File name:      value_unit_pair.py           #        _.==._        #
#  Author:         Arjan Lemmens                #     .+=##**##=+.     #
#  Date:           26-May-2023                  #    *= #        =*    #
# ============================================= #   #/  #         \#   #
#  Description:    Custom composite value unit  #  |#   #   $      #|  #
#                  pair widget.                 #  |#   #   #      #|  #
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


class ValueUnitPair:
    """A set of 3 widgets and a frame.
    The label shows the combination of what is entered in the entry and the selected unit in the selectionMenu.
    The optionMenu and entry are placed in their own frame, it is recommended to use the grid and grid remove methods for geometric management.
    """

    def __init__(self, parent=None, value:str="", unit:str="", lOptions:list[str]=None, **kwargs):
        """Constructor

        :param parent: Tkinter parent frame in which this widget will be placed, defaults to None
        :type parent: tkinter frame, optional
        :param value: Initial value, defaults to ""
        :type value: any, optional
        :param unit: Initial value for the unit, defaults to ""
        :type unit: string, optional
        :param lOptions: list of options available when selecting the units, defaults to list()
        :type lOptions: list[str], optional
        """
        self.label = ttk.Label(parent)
        """ Tkinter label """
        self.label.grid(**kwargs)

        self.inputFrame = ttk.Frame(parent)
        """ Tkinter frame holding the option menu and entry"""
        self.inputFrame.grid(**kwargs)

        self.entry = ttk.Entry(self.inputFrame)
        """ Tkinter entry allowing user input for the value """
        self.entry.grid(column=0, row=0)

        self.unit = tk.StringVar(self.inputFrame)
        """ Tkinter variable for unit value """

        lOptions = [""] if lOptions is None or len(lOptions) < 1 else lOptions
        self.optionMenu = ttk.OptionMenu(
            self.inputFrame, self.unit, lOptions[0], *lOptions, command=self.set_label)
        """ Tkinter option menu """
        self.optionMenu.grid(column=1, row=0)

        self.set(value, unit)

    def __del__(self):
        """Destructor"""
        try:
            self.label.destroy()
            self.inputFrame.destroy()
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
        self.inputFrame.grid(**kwargs)

        # Don't change the location of the widgets inside the input frame
        self.entry.grid()
        self.optionMenu.grid()

    def grid_remove(self):
        """Unmap this widget but remember the grid options"""
        self.label.grid_remove()
        self.entry.grid_remove()
        self.optionMenu.grid_remove()
        self.inputFrame.grid_remove()

    def set_label(self, value=None):
        """set_label Update the label text, which is a combination of the text in the entry and the selected value in the selectionMenu

        :param value: string received by the OptionMenu callback. Data enter is not used, defaults to None
        :type value: Nothing, optional
        """
        self.label.configure(text=self.entry.get() + self.unit.get())

    def show_label(self):
        """show_label Show the label showing the value and unit, hide the entry and selectionMenu
        """
        self.set_label()
        self.inputFrame.grid_remove()
        self.label.grid()

    def show_input(self):
        """show_label Show the entry and selectionMenu, hide the label
        """
        self.inputFrame.grid()
        self.label.grid_remove()

    def set(self, value, unit:str):
        """set Set the widget to a specific value unit value

        :param value: Value shown in the entry
        :type value: any
        :param unit: Unit to which the selectionMenu is set
        :type unit: string
        """
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(value))
        self.unit.set(unit)
        self.set_label()

    def get(self):
        """get Read the value unit inputs

        :return: Tuple where the first index is the value in string form, and the second is the unit
        :rtype: tuple
        """
        return (self.entry.get(), self.unit.get())

    def get_string(self):
        """Get the value and unit in the form of a single string

        :return: Value and unit combined into 1 string
        :rtype: string
        """
        return self.entry.get() + str(self.unit.get())
    
    def set_options(self, lOptions, value=None):
        """
        Set the options of the selection menu

        :param lOptions: List of new options
        :type lOptions: list
        :param value: value to set the option menu too, defaults to None
        :type value: any, optional
        """
        self.optionMenu.set_menu(value, *lOptions)
        
    def __repr__(self): 
        """
        Representation of this class when it is printed or viewed in debugger window

        :return: String of how this object should be represented
        :rtype: string
        """        
        return f"entry: {self.entry}\nmenu: {self.optionMenu}\nlabel:{self.label}\nframe:{self.inputFrame}"
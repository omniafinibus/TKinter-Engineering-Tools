# ==================================================================== #
#  File name:      entry_label_pair.py          #        _.==._        #
#  Author:         Arjan Lemmens                #     .+=##**##=+.     #
#  Date:           26-May-2023                  #    *= #        =*    #
# ============================================= #   #/  #         \#   #
#  Description:    Custom composite entry label #  |#   #   $      #|  #
#                  widget                       #  |#   #   #      #|  #
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
class EntryLabelPair:
    """A set of 2 widgets, a label and an entry.
    The label will show what has been typed in the entry.
    Only 1 of the 2 widgets is visible since they will be toggled.
    """

    def __init__(self, parent=None, text:str="", **kwargs):
        """Constructor

        :param parent: tkinter parent, defaults to None
        :type parent: tkinter frame, optional
        :param text: Text to enter into the entry and label, defaults to ""
        :type text: str, optional
        """
        self.root = parent
        self.entry = ttk.Entry(self.root)
        """ Tkinter entry """
        # Add text to the entry
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)

        self.label = ttk.Label(self.root, text=text)
        """ Tkinter label """

        self.entry.grid(**kwargs)
        self.label.grid(**kwargs)

    def __del__(self):
        """Destructor"""
        try:
            self.label.destroy()
            self.entry.destroy()
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
        self.entry.grid(**kwargs)

    def grid_remove(self):
        """Unmap this widget but remember the grid options"""
        self.label.grid_remove()
        self.entry.grid_remove()

    def show_label(self):
        """Hide the entry widget and show the label widget"""
        self.entry.grid_remove()
        # Update the text when switching
        self.label.configure(text=self.entry.get())
        self.label.grid()

    def show_entry(self):
        """Hide the label widget and show the entry widget"""
        self.label.grid_remove()
        self.entry.grid()

    def set(self, text:str=""):
        """set Set the text for both the entry and label

        :param text: Text to place in entry and label, defaults to ""
        :type text: string, optional
        """
        self.label.configure(text=str(text))
        self.entry.delete(0, "end")
        self.entry.insert(0, str(text))

    def get(self):
        """get Get the input string from the entry

        :return: Data entered in entry
        :rtype: string
        """
        return self.entry.get()

    def __repr__(self):
        """
        Representation of this class when it is printed or viewed in debugger window

        :return: String of how this object should be represented
        :rtype: string
        """
        return f"root: {self.root}\ndata: {self.entry.get()}\nentry: {self.entry}\nlabel: {self.label}"
        
        
        
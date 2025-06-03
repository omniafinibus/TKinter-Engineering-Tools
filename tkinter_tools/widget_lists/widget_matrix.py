# ==================================================================== #
#  File name:      widget_matrix.py             #        _.==._        #
#  Author:         Arjan Lemmens                #     .+=##**##=+.     #
#  Date:           11-May-2023                  #    *= #        =*    #
# ============================================= #   #/  #         \#   #
#  Description:    Provides a matrix class      #  |#   #   $      #|  #
#                  which can sort and           #  |#   #   #      #|  #
#                  automatically place widgets  #   #\  #   #     /#   #
#                  in a matrix of predefined    #    *= #   #    =+    #
#                  width.                       #     *++######++*     #
#  Rev:            3.0                          #        *-==-*        #
# ==================================================================== #
#  Revision history:                                                   #
#  Date        Description                                             #
#  28-Feb-2023 File created                                            #
#  01-Mar-2023 Finished first version of class                         #
#  07-Mar-2023 Converted lllWidgets into a matrix from list            #
#  14-Mar-2023 Added comments                                          #
#  11-May-2023 Cleaned up code and added comments                      #
#  10-May-2023 Cleaned and commented code                              #
# ==================================================================== #
#  To-Do: !=Priority, ~=Bug, ?=Idea/nice to have                       #
#                                                                      #
# ==================================================================== #

# =========== #
#   Imports   #
# =========== #
import os
import PIL.Image as Image
import PIL.ImageTk as ImageTk
from tkinter_tools.resources import decode_image, assets
from tkinter_tools.tools import Button, is_widget_this_list, WIDGET_ENTRY_LABEL, WIDGET_SELECTION_LABEL,WIDGET_VALUE_UNIT

# =========== #
#   Classes   #
# =========== #
class WidgetMatrix:
    """ A class for a matrix of widgets of the same type"""

    def __init__(self, parent, widgetType, maxColumns:int=-1, editMode:bool=False):
        """Constructor

        :param parent: Parent frame to place matrix in
        :type parent: tkinter frame
        :param widgetType: The type of widget to add when the add button is pressed
        :type widgetType: tkinter, ttk, composite_widgets widget
        :param maxColumns: How many columns are allowed before a new row is added. If it is -1, this is infinite, defaults to -1
        :type maxColumns: integer, optional
        :param editMode: Editing state, defaults to False
        :type editMode: boolean, optional
        """
        self.root = parent
        """ Matrix parent frame where all widgets are placed in"""

        self.widgetType = widgetType
        """ All elements will have be a clone of this widget. """

        self.maxColumns = maxColumns
        """ Maximum amount of columns in the matrix, before a new row is added. """

        self.currentRow = 0
        """ What the current row is (internally used). """

        self.lllWidgets = list()
        """ Matrix of all widgets, coupled with a value for sorting. [row][column][value, widget] """

        self.add_icon_light=ImageTk.PhotoImage(Image.open(decode_image(assets.plus_icon)).resize((15, 15)), master=self.root)
        self.add_icon_dark=ImageTk.PhotoImage(Image.open(decode_image(assets.plus_icon_inv)).resize((15, 15)), master=self.root)

        self.addButton = Button(
            self.root, self.add_icon_light, self.add_icon_dark, image=self.add_icon_light, highlightthickness=0, bd=0
        )
        """ Add button used to add elements to the matrix """

        # Overwrite internal callback of button to add functionality prior to calling the callbacks
        self.addButton.configure(command=lambda: self.add_widget())
        self.addButton.grid(row=0, column=0)

        self.colorMode = "light"

        # Hide the add button in view mode
        if not editMode:
            self.addButton.grid_remove()

    def set_add_button_command(self, command):
        """
        Change the callback of the add button

        :param command: New function to run when the add button is clicked
        :type command: function
        """
        self.addButton.configure(command=command)

    def __del__(self):
        """ Destructor """
        for row in self.lllWidgets:
            for widget in row:
                # Delete each widget from frame
                if is_widget_this_list(widget, WIDGET_ENTRY_LABEL, WIDGET_SELECTION_LABEL,  WIDGET_VALUE_UNIT):
                    widget[1].__del__()
                else:
                    widget[1].destroy()

                # Clear the widget value set
                widget.clear()
            row.clear()
        self.lllWidgets.clear()

        # Finally destroy the delete button
        self.addButton.destroy()

    def set_theme(self, mode:str="light"):
        """set_theme Set color mode of this object

        :param mode: Name of mode, "dark" and "light" are supported, defaults to "light"
        :type mode: string, optional
        """        
        if mode is None:
            mode = self.colorMode
        else:
            self.colorMode = mode

        self.addButton.set_theme(mode)

    def explode_widget_list(self):
        """explode_widget_list Convert the widget matrix into a one dimensional list holding (value, widget)

        :return: List of widgets and value pairs (value, widget)
        :rtype: list[[any, Widget]]
        """

        # Place all widgets into a list
        llBufferList = list()
        for llRow in self.lllWidgets:
            llBufferList += llRow

        # Pass the list on
        return llBufferList

    def set_value(self, oldValue:str, newValue:str):
        """
        set_value Change the value of a 

        :param oldValue: Old value to look for
        :type oldValue: string
        :param newValue: Value to replace the old value with
        :type newValue: string
        """        
        # Convert the list for sorting
        oneDimensionalList = self.explode_widget_list()

        # Delete the widget of the selected value
        for entry in oneDimensionalList:
            if oldValue == entry[0]:
                entry[0] = newValue
                entry[1].configure(text=newValue)
                newValue = -1

        # Sort the list order based on the value element (index=0)
        oneDimensionalList.sort(key=lambda index: index[0])

        # Recreate the matrix
        self.lllWidgets = self.create_matrix(oneDimensionalList)

        # Place all widgets into the correct spot
        self.set_all_positions()
        self.set_add_button_position()
        
    def clear_all(self):
        """
        clear_all Clear all widgets from the matrix
        """
        # Convert the list for sorting
        oneDimensionalList = self.explode_widget_list()

        # Delete the widget of the selected value
        oneDimensionalList.clear()

        # Recreate the matrix
        self.lllWidgets = self.create_matrix(oneDimensionalList)

        # Place all widgets into the correct spot
        self.set_all_positions()
        self.set_add_button_position()
        
    def add_widget(self, value:int=None):
        """add_widget Add a new widget to the matrix

        :param value: Value of the new widget, defaults to None
        :type value: integer, optional
        """
        # Convert the list for sorting
        llOneDimensionalList = self.explode_widget_list()

        # Clone the widget configuration
        llOneDimensionalList.append([value if value is not None else len(
            llOneDimensionalList), clone_widget(self.widgetType, self.root)])

        newWidget = llOneDimensionalList[-1]

        llOneDimensionalList[-1][1].configure(text=str(value if value is not None else len(llOneDimensionalList)+1))

        # Sort the list order based on the value element (index=0)
        llOneDimensionalList.sort(key=lambda index: index[0])

        # Recreate the matrix
        self.lllWidgets = self.create_matrix(llOneDimensionalList)

        # Place all widgets into the correct spot
        self.set_all_positions()
        self.set_add_button_position()
        
        return newWidget
    
    def get_widget(self, value):
        """
        Retrieve the widget of a specific value from the widget matrix

        :param value: Value to check for
        :type value: any
        :return: Widget which has the requested value, if none are found None will be returned
        :rtype: Widget
        """        
        widgetList = self.explode_widget_list()
        for widgetValue, widget in widgetList:
            if widgetValue == value:
                return widget
            
        return None
    
    def remove_widget(self, value):
        """remove_widget Remove a widget from the matrix

        :param value: Value of the widget to remove
        :type value: string
        """
        # Convert the list for sorting
        oneDimensionalList = self.explode_widget_list()

        # Delete the widget of the selected value
        for entry in oneDimensionalList:
            if value == entry[0]:
                oneDimensionalList.remove(entry)
                entry[1].destroy()

        # Sort the list order based on the value element (index=0)
        oneDimensionalList.sort(key=lambda index: index[0])

        # Recreate the matrix
        self.lllWidgets = self.create_matrix(oneDimensionalList)

        # Place all widgets into the correct spot
        self.set_all_positions()
        self.set_add_button_position()

    def create_matrix(self, llOneDimensionalList:list[list]):
        """create_matrix Create a matrix from a one dimensional list

        :param llOneDimensionalList: One dimensional list of (value, widget) elements
        :type llOneDimensionalList: list
        :return: List of lists of (value, widget)
        :rtype: list[list[(any, Widget)]]
        """
        lllNewMatrix = list()

        for index in range(len(llOneDimensionalList)):
            # With a maxColumns of 7, each row will have index 0 to 6
            column = index % self.maxColumns
            # Formula works, it"s hard to explain in a comment
            row = (index - column) / self.maxColumns
            # If the current column is equal to the maxColumns (Because indexing start from 0)
            if column == 0:
                lllNewMatrix.append([llOneDimensionalList[index]])  # Create a new row
            else:  # Add it into the current row
                # int is used to because floats are not accepted
                lllNewMatrix[int(row)].append(llOneDimensionalList[index])
                
        if len(llOneDimensionalList) == 0:
            lllNewMatrix = [[]]

        return lllNewMatrix

    def set_all_positions(self):
        """set_all_positions Place all widgets in the frame based on their row and column inside the matrix lllWidgets"""

        for row in self.lllWidgets:
            for element in row:
                element[1].grid(
                    column=row.index(element),
                    row=self.lllWidgets.index(row)
                )  # place the widget on the same location as it is in the lllWidgets

    def set_add_button_position(self):
        """ set_add_button_position Place the add button at the end of the matrix)"""
        lastRow = self.lllWidgets[-1]
        # Check if the last row has space for the add button
        if len(lastRow) == self.maxColumns:  # No space left, place it on the next row
            self.addButton.grid(
                column=0, row=self.lllWidgets.index(lastRow) + 1)
        else:  # Place it in the current row
            self.addButton.grid(column=len(lastRow),
                                row=self.lllWidgets.index(lastRow))

    def get_values(self):
        """
        Get the saved values in a sorted list

        :return: List of sorted values
        :rtype: list[int]
        """        
        values = [entry[0] for entry in self.explode_widget_list()]
        values.sort()
        return values   

    def __repr__(self): 
        """
        Representation of this class when it is printed or viewed in debugger window

        :return: String of how this object should be represented
        :rtype: string
        """   
        return f"root: {self.root}\naddButton cb: {self.addButton.dCallbackSets[self.addButton.currentMode]}\n widget type: {self.widgetType.__name__}\nmax columns: {self.maxColumns}"

def clone_widget(widget, parent=None):
    """clone_widget Clone a widget

    :param widget: Widget to copy
    :type widget: tkinter, ttk, or composite_widgets widget
    :param parent: Parent to which the new widget will be assigned, defaults to None
    :type parent: tkinter frame, optional
    :return: A carbon copy of the widget
    :rtype: tkinter, ttk, or composite_widgets widget
    """
    cls = widget.__class__

    # Clone the widget configuration
    cfg = {key: widget.cget(key) for key in widget.configure()}
    dolly = cls(parent if parent is not None else widget.parent, **cfg)

    return dolly

    
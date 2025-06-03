# ==================================================================== #
#  File name:      list_entry.py                #        _.==._        #
#  Author:         Arjan Lemmens                #     .+=##**##=+.     #
#  Date:           08-May-2023                  #    *= #        =*    #
# ============================================= #   #/  #         \#   #
#  Description:    Defines the ListEntry class  #  |#   #   $      #|  #
#                  which is used by the         #  |#   #   #      #|  #
#                  WidgetList to control full   #   #\  #   #     /#   #
#                  row of widget.               #    *= #   #    =+    #
#  Rev:            5.0                          #     *++######++*     #
#                                               #        *-==-*        #
# ==================================================================== #
#  Revision history:                                                   #
#  Date        Description                                             #
#  23-Feb-2023 File created                                            #
#  24-Feb-2023 Made class more flexible                                #
#  28-Feb-2023 Made class more flexible (fixed)                        #
#  28-Feb-2023 Simplified class to make it less buggy                  #
#  03-Feb-2023 Removed excess methods                                  #
#  06-Feb-2023 Bug fixes for complete overhaul                         #
#  08-May-2023 Cleaned up code and added comments                      #
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
from tkinter_tools.fancy_callbacks import  CallbackSet
from tkinter_tools.resources import decode_image, assets
from tkinter_tools.tools import is_widget_this, WIDGET_TKT_BUTTON, set_widget_position, is_widget_this_list, WIDGET_ENTRY_LABEL, WIDGET_VALUE_UNIT, WIDGET_SELECTION_LABEL, Button


# =========== #
#   Classes   #
# =========== #
class ListEntry:
    """
    Entry to be placed in a widget list
    \tIt holds the widgets themself in lWidgets.\n\r
    \tVariables related to these widgets or the entry in general can be place in lVariables.\n\r
    \tCustom callbacks can be attached to the editCallbacks and viewCallbacks (type = Callbackset).\t
    \tThe editCallbacks and viewCallbacks are called through set_edit_mode and set_view_mode respectively
    """

    def __init__(self, parent, rowIndex:int, editMode:bool=False, rowOffset:int=0, colorMode:str="light"):
        """
        Constructor for the ListEntry class

        :param parent: parent Frame in which the entry will be placed
        :type parent: tkinter.Frame
        :param rowIndex: row location of this entry in the parent frame
        :type rowIndex: integer
        :param editMode: If the entry needs to be set to edit mode after the constructor is finished, defaults to False
        :type editMode: boolean, optional
        :param rowOffset: Amount of rows which need to be added to the row index, defaults to 0
        :type rowOffset: integer, optional
        :param colorMode: Color mode of this entry, default to "light"
        :type colorMode: string, optional
        """

        self.root = parent
        """Parent Frame where the entry is located"""
        self.rowIndex = rowIndex
        """Row location of the entry in the parent frame"""
        self.editMode=editMode
        """Boolean defining if this object is in edit (True) or view mode (False)"""
        self.colorMode = colorMode
        """Color mode of this entry"""
        self.lWidgets = list()
        """List of widget objects placed in the entry (From tkinter, tkk, or composite_widgets)"""
        self.editCallbacks = CallbackSet()
        """Callbacks which are called when entering edit mode (uses tkinter_tools.CallbackSet class)"""
        self.viewCallbacks = CallbackSet()
        """Callbacks which are called when entering view mode (uses tkinter_tools.CallbackSet class)"""
        self.lVariables = list()
        """Used for all variable or data related to widgets in the entry (tkinter.StringVar for example)"""
        self.rowOffset = rowOffset
        """Offset applied to the rows to shift the whole list to which this entry belongs"""

    def __del__(self):
        """
        __del__ Destructor for the ListEntry class, deletes all widgets and variable related to this entry
        """
        for widget in reversed(self.lWidgets):
            self.remove_widget(self.lWidgets.index(widget))

        # Remove all variables
        for variable in reversed(self.lVariables):
            self.lVariables.remove(variable)

    def add_widget( self, widget, editKey:str=None, editCallback=None, viewKey:str=None, viewCallback=None, rowOffset:int=0):
        """
        add_widget Add a widget at the far most right position in the entry

        :param widget: Widget which needs to be added
        :type widget: tkinter, ttk, or composite_widgets Widget
        :param editKey: Key of callback to run when the ListEntry is set too edit mode, which relates to the new widget, defaults to None
        :type editKey: string, optional
        :param editCallback: callback to run when the ListEntry is set too edit mode, which relates to the new widget, defaults to None
        :type editCallback: method , optional
        :param viewKey: Key of callback to run when the ListEntry is set too view mode, which relates to the new widget, defaults to None
        :type viewKey: string, optional
        :param viewCallback: callback to run when the ListEntry is set too view mode, which relates to the new widget, defaults to None
        :type viewCallback: method, optional
        :param rowOffset: The row offset from where the row index needs to be added, defaults to 0
        :type rowOffset: integer, optional
        :return: Widget which was added
        :rtype: tkinter, ttk or composite_widgets Widget
        """

        self.rowOffset = rowOffset

        # Add and set widget location
        self.lWidgets.append(widget)
        self.lWidgets[-1].grid(
            column=len(self.lWidgets) - 1, row=self.rowIndex + self.rowOffset
        )

        # Attach callbacks
        if editKey is not None and editCallback is not None:
            self.editCallbacks.add_callback(editKey, editCallback)

        if viewKey is not None and viewCallback is not None:
            self.viewCallbacks.add_callback(viewKey, viewCallback)

        # Return widget for further setup
        return self.lWidgets[-1]

    def add_widget_at_index(self, index, widget, editKey:str=None, editCallback=None, viewKey:str=None, viewCallback=None, rowOffset:int=0):
        """
        add_widget_at_index Add a widget to this entry, specificizing the the column location where to place the widgets

        :param index: Column and list index where to add the new Widget
        :type index: tkinter, ttk, or composite_widgets Widget
        :param widget: Widget to add the at the specified index
        :type widget: tkinter, ttk, or composite_widgets Widget
        :param editKey: Key of callback to run when the ListEntry is set too edit mode, which relates to the new widget, defaults to None
        :type editKey: string, optional
        :param editCallback: callback to run when the ListEntry is set too edit mode, which relates to the new widget, defaults to None
        :type editCallback: method, optional
        :param viewKey: Key of callback to run when the ListEntry is set too view mode, which relates to the new widget, defaults to None
        :type viewKey: string, optional
        :param viewCallback: callback to run when the ListEntry is set too view mode, which relates to the new widget, defaults to None
        :type viewCallback: method, optional
        :param rowOffset: The row offset from where the row index needs to be added, defaults to 0
        :type rowOffset: integer, optional
        :return: Widget which was added
        :rtype: tkinter, ttk or composite_widgets Widget
        """
        # for an index which wraps around, change the integer value to the corresponding positive value
        if index < 0:
            index = len(self.lWidgets) + index

        self.rowOffset = rowOffset

        # Place widget at the index of the entry
        self.lWidgets.insert(index, widget)
        self.lWidgets[index].grid(column=index, row=self.rowIndex + rowOffset)
        
        # Move all widgets to the right of the new widget one column over
        for widget in self.lWidgets[index + 1:]:
            set_widget_position(widget, widget, 1, 0)

        # Add callback keys
        if editKey is not None and editCallback is not None:
            self.editCallbacks.add_callback(editKey, editCallback)

        if viewKey is not None and viewCallback is not None:
            self.viewCallbacks.add_callback(viewKey, viewCallback)

        # Return the new Widget
        return self.lWidgets[index]

    def remove_widget(self, index:int):
        """
        remove_widget Remove a widget from the entry 

        :param index: Index of the widget which needs to be remove
        :type index: integer
        """
        # If the widget does not have a destructor, destroy it manually
        if is_widget_this_list(
            self.lWidgets[index],
            WIDGET_SELECTION_LABEL, WIDGET_ENTRY_LABEL, WIDGET_TKT_BUTTON, WIDGET_VALUE_UNIT,
        ):
            self.lWidgets[index].__del__()
        else:
            self.lWidgets[index].destroy()
        # Remove the widget from the widget list
        self.lWidgets.pop(index)

        # Update location for following widgets
        for widget in self.lWidgets[index:]:
            set_widget_position(widget, widget, -1, 0)

    def replace_widget(self, index, newWidget, editKey:str=None, editCallback=None, viewKey:str=None, viewCallback=None):
        """
        replace_widget Replace a widget in the entry with a different widget, the old widget will be destroyed

        :param index: Index of the widget which needs to be remove
        :type index: integer
        :param widget: Widget to add the at the specified index
        :type widget: tkinter, ttk, or composite_widgets Widget
        :param editKey: Key of callback to run when the ListEntry is set too edit mode, which relates to the new widget, defaults to None
        :type editKey: string, optional
        :param editCallback: callback to run when the ListEntry is set too edit mode, which relates to the new widget, defaults to None
        :type editCallback: method, optional
        :param viewKey: Key of callback to run when the ListEntry is set too view mode, which relates to the new widget, defaults to None
        :type viewKey: string, optional
        :param viewCallback: callback to run when the ListEntry is set too view mode, which relates to the new widget, defaults to None
        :type viewCallback: method, optional
        :return: Widget which was added
        :rtype: tkinter, ttk or composite_widgets Widget
        """
        # Replace the widget
        self.remove_widget(index)
        return self.add_widget_at_index(
            index, newWidget, editKey, editCallback, viewKey, viewCallback, self.rowOffset
        )

    def set_edit_mode(self):
        """
        Set this object to edit mode, to allow changing the user input fields
        """    
        self.editMode = True
        self.editCallbacks.call_callbacks()

    def set_view_mode(self):
        """
        Set this object to view mode, to prevent changing the user input fields
        """    
        self.editMode = False
        self.viewCallbacks.call_callbacks()

    def set_theme(self, mode:str="light"):
        """set_theme Set color mode of this object

        :param mode: Name of mode, "dark" and "light" are supported, defaults to "light"
        :type mode: string, optional
        """
        self.colorMode = mode
        for widget in self.lWidgets:
            if is_widget_this(widget, WIDGET_TKT_BUTTON):
                widget.set_theme(mode)

    def reset_mode(self):
        """
        reset_mode Reset all widgets in the entry to the correct mode (view or edit)
        """
        self.set_theme(self.colorMode)
        if self.editMode:
            self.set_edit_mode()
        else:
            self.set_view_mode()

    def add_deletion_button(self, deleteCallback, visibleInViewMode:bool=False):
        """ 
        remove_widget Add a deletion button at the far most right of the entry

        :param deleteCallback: Callback of a method which deletes this entry "removeEntry0"
        :type deleteCallback: method
        :param visibleInViewMode: Show the delete button in view mode instead of edit mode, defaults to False
        :type visibleInViewMode: boolean, optional
        :return: Newly created deletion button
        :rtype: weird_widget.Button
        """
        # Configure deletion button
        baseDir =  os.path.abspath('./assets') + "\\"
        self.minus_icon_light=ImageTk.PhotoImage(Image.open(decode_image(assets.minus_icon)).resize((15, 15)), master=self.root)
        self.minus_icon_dark=ImageTk.PhotoImage(Image.open(decode_image(assets.minus_icon_inv)).resize((15, 15)), master=self.root)

        deletionButton = Button(
            parent=self.root, 
            lightImage= self.minus_icon_light,
            darkImage=self.minus_icon_dark,
            image=self.minus_icon_dark if self.colorMode == "dark" else self.minus_icon_light,
            highlightthickness=0, 
            bd=0
        )
        
        deletionButton.grid(
            padx= 2.5,
            pady= 2.5,
            sticky= "news"
            )
        
        # Attach callback
        deletionButton.add_callback(
            callbackKey="removeEntry0",
            callback=deleteCallback,
            argument=self.rowIndex
        )

        # Append button to the entry
        return self.add_widget(
            widget=deletionButton,
            editKey="editDeleteButton",
            editCallback=deletionButton.grid if not visibleInViewMode else deletionButton.grid_remove,
            viewKey="viewDeleteButton",
            viewCallback=deletionButton.grid_remove if not visibleInViewMode else deletionButton.grid,
            rowOffset=self.rowOffset
        )

    def set_row_index(self, newIndex:int, baseRow:int=None):
        """
        set_row_index Update the row index of this list entry, this includes widget position

        :param newIndex: New row index where to place the widgets
        :type newIndex: integer
        :param baseRow: new base row off with which the new row index needs to be offset, if left as None it will keep the current base row, defaults to None
        :type baseRow: integer, optional
        """
        if baseRow is None:  # Get the current base row if the base row is left as None
            baseRow = self.lWidgets[0].grid_info()["column"] - self.rowIndex

        self.rowIndex = newIndex

        # Update the row value of each widget on this entry
        newRow = self.rowIndex + baseRow
        for widget in self.lWidgets:
            widget.grid(row=newRow)

        # Correct widgets which were shown due to the result of calling grid
        self.reset_mode()

        
    def __repr__(self): 
        """
        Representation of this class when it is printed or viewed in debugger window

        :return: String of how this object should be represented
        :rtype: string
        """   
        
        return f"root: {self.root}\nrowOffset: {self.rowOffset}\nrowIndex: {self.rowIndex}\nlWidgets: {self.lWidgets}"
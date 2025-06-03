# ==================================================================== #
#  File name:      list_with_header.py          #        _.==._        #
#  Author:         Arjan Lemmens                #     .+=##**##=+.     #
#  Date:           10-May-2023                  #    *= #        =*    #
# ============================================= #   #/  #         \#   #
#  Description:    Defines the WidgetList class,#  |#   #   $      #|  #
#                  used to implement lists of   #  |#   #   #      #|  #
#                  row entries which have the   #   #\  #   #     /#   #
#                  same functionality.          #    *= #   #    =+    #
#  Rev:            4.0                          #     *++######++*     #
#                                               #        *-==-*        #
# ==================================================================== #
#  Revision history:                                                   #
#  Date        Description                                             #
#  23-Feb-2023 File created                                            #
#  24-Feb-2023 Made class more flexible (broken)                       #
#  28-Feb-2023 Made class more flexible (fixed)                        #
#  03-Mar-2023 Complete overhaul                                       #
#  06-Mar-2023 Bug fixes for complete overhaul                         #
#  10-May-2023 Cleaned and commented code                              #
# ==================================================================== #
#  To-Do: !=Priority, ~=Bug, ?=Idea/nice to have                       #
#                                                                      #
# ==================================================================== #

# =========== #
#   Imports   #
# =========== #
import os
from tkinter import ttk
import PIL.Image as Image
import PIL.ImageTk as ImageTk
from .list_entry import ListEntry
from tkinter_tools.composite_widgets import Button
from tkinter_tools.resources import decode_image, assets
from tkinter_tools.tools import is_widget_this, WIDGET_TKT_BUTTON

# =========== #
#   Classes   #
# =========== #
class WidgetList:
    """
    A list of entries filled with widgets, placed in the parent frame in a list like manner.
    The list uses the ListEntry class to add, remove and edit separate rows.
    """

    def __init__(self, parent, editMode:bool=False, lTitles:list[str]=None):
        """Constructor

        :param parent: parent Frame in which the entry will be placed
        :type parent: tkinter.Frame
        :param editMode: If the entry needs to be set to edit mode after the constructor is finished, defaults to False
        :type editMode: boolean, optional
        :param lTitles: List of titles to add to the WidgetList, if it is in the form of: list[list[strings]], each listed list will be added on a new row, defaults to None
        :type lTitles: list[strign], optional
        """

        self.root = parent
        """ Parent frame which list uses """
        self.editMode = editMode
        """Boolean defining if this object is in edit (True) or view mode (False)"""
        self.lEntries = list()
        """ All entries in the list (uses ListEntry class) """
        self.baseRowIndex = 0
        """ Starting row index offset """
        self.mode = "light"
        """ Theme mode for this list, used when new entries are added """

        baseDir =  os.path.abspath('./assets') + "\\"
        add_icon_light=ImageTk.PhotoImage(Image.open(decode_image(assets.plus_icon)).resize((15, 15)), master=self.root)
        add_icon_dark=ImageTk.PhotoImage(Image.open(decode_image(assets.plus_icon_inv)).resize((15, 15)), master=self.root)
        
        # Add the add button at the bottom of the list
        self.addButton = Button(
            self.root, 
            add_icon_light,
            add_icon_dark,
            image=add_icon_light,
            highlightthickness=0, 
            bd=0
        )
        """ Add button used to add entries """

        # Configure the button
        self.addButton.add_callback(
            callbackKey="addEntry", callback=self.add_empty_entry
        )
        self.addButton.grid(row=len(self.lEntries) + self.baseRowIndex, column=0)
        
        # Add titles
        if isinstance(lTitles, list) and isinstance(lTitles[0], str):
            # lTitles is in the form of a list so only add 1 entry of titles
            self.add_titles(lTitles)
        elif isinstance(lTitles, list) and isinstance(lTitles[0], list):
            # Add a title entry for each list item
            for titles in lTitles:
                self.add_titles(titles, lTitles.index(titles))

        # Hide the add button in view mode
        if not self.editMode:
            self.addButton.grid_remove()

    def __del__(self):
        """Destructor"""
        for entry in reversed(range(len(self.lEntries))):
            self.lEntries.pop(-1)

        self.addButton.destroy()

    def set_add_button_command(self, command):
        """
        Change the callback of the add button

        :param command: New function to run when the add button is clicked
        :type command: function
        """        
        self.addButton.configure(command=command)

    def set_theme(self, mode:str="light"):
        """set_theme Set color mode of this object

        :param mode: Name of mode, "dark" and "light" are supported, defaults to "light"
        :type mode: string, optional
        """
        # Check each entry and update any weird_widget Buttons
        if mode == "dark":
            self.mode = "dark"
        else:
            self.mode = "light"
        for entry in self.lEntries:
            entry.set_theme(mode)

        # Update the add button
        self.addButton.set_theme(mode)

    def set_row_offset(self, newRowOffset:int):
        """set_row_offset Move the whole list down by X amount of rows from the the 0th row

        :param newRowIndex: Number of rows to move the list
        :type newRowIndex: integer
        """

        # Save value for future use
        self.baseRowIndex = newRowOffset

        # Update each entry
        for entry in self.lEntries:
            entry.set_row_index(entry.rowIndex, newRowOffset)
            
        self.addButton.grid(row=len(self.lEntries) + self.baseRowIndex, column=0)

        # Callbacks need to be updated since a changed rowIndex could break some callbacks
        self.update_callbacks()

    def add_titles(self, lTitles:list[str], index:int=0):
        """add_titles Add titles to the WidgetList.
        This function will overwrite any entry already present at the specified index.
        If not index is defined, it will write the titles to the zeroth entry (taking row offset into account)

        :param lTitles: List of titles to write, if a column needs to be blank, enter a empty string: "" at that index
        :type lTitles: list[string]
        :param index: Index where the titles will be placed, defaults to 0
        :type index: integer, optional
        :return: The create title entry
        :rtype: ListEntry
        """

        if isinstance(lTitles, list):
            # If an entry with the provided index is already present, delete and clear it
            if len(self.lEntries) - 1 >= index:
                self.remove_entry(index)
            entry = self.add_empty_entry(index)

            # Add each title to the new entry
            for title in lTitles:
                widget = entry.add_widget(
                    ttk.Label(self.root, text=str(title)), rowOffset=self.baseRowIndex
                )
                widget.grid(
                    padx=2.5,
                    pady=2.5,
                    sticky="news"
                )

        return entry

    def add_empty_entry(self, index:int=None):
        """
        add_empty_entry Add an entry at the specified index without any widgets inside
        If index is left as None, the entry will be placed at the end of the list

        :param index: Row location of the new entry, defaults to None
        :type index: integer, optional
        :return: The entry which was created in this method
        :rtype: ListEntry
        """

        # Check if the provided position is valid
        if index is None or index >= len(self.lEntries):
            index = len(self.lEntries)

        # Add the entry
        self.lEntries.insert(
            index,
            ListEntry(
                parent=self.root,
                rowIndex=len(self.lEntries),
                rowOffset=self.baseRowIndex,
                editMode=self.editMode,
                colorMode=self.mode
            ),
        )

        # Update any following entries and the add button
        self.update_indices(index)

        return self.lEntries[index]

    def remove_entry(self, index:int=-1):
        """
        remove_entry Remove entry from the list by calling it's destructor

        :param index: Index which needs to be deleted, defaults to -1
        :type index: integer, optional
        """

        self.lEntries[index].__del__()
        self.lEntries.pop(index)

        # Reorder the remaining entries
        self.update_indices(index)

    def remove_entries(self, startIndex:int=0, stopIndex:int=None):
        """
        remove_entries Remove multiple entries by defining the first and last entry index.

        :param startIndex: Index of the first entry which needs to be deleted, defaults to 0
        :type startIndex: integer, optional
        :param stopIndex: Index of the last entry which needs to be deleted, defaults to None
        :type stopIndex: integer, optional
        """
        # Check if indices exist
        if len(self.lEntries) > 0 and startIndex < len(self.lEntries):
            if stopIndex is None:
                stopIndex = len(self.lEntries)

            for entry in reversed(self.lEntries[startIndex:stopIndex]):
                self.lEntries.remove(entry)
                entry.__del__()

            self.update_indices(startIndex)

    def update_indices(self, startIndex:int=0):
        """
        update_indices Update the row indices and location of the ListEntry objects in the lEntries list

        :param startIndex: Starting index from which the entries will be updated, defaults to 0
        :type startIndex: integer, optional
        """        
        for index in range(startIndex, len(self.lEntries)):
            self.lEntries[index].set_row_index(index, self.baseRowIndex)

        # Update the location of the add button
        self.addButton.grid(row=len(self.lEntries) + self.baseRowIndex)

        # Update callbacks which use the row index as argument
        self.update_callbacks(startIndex)

        # Hide add button if not in edit mode
        if not self.editMode:
            self.addButton.grid_remove()

    def set_edit_mode(self):
        """
        Set this object to edit mode, to allow changing the user input fields
        """    

        self.editMode = True

        for entry in self.lEntries:
            entry.set_edit_mode()

        # Show add button
        self.addButton.grid()

    def set_view_mode(self):
        """
        Set this object to view mode, to prevent changing the user input fields
        """    
        self.editMode = False

        for entry in self.lEntries:
            entry.set_view_mode()

        # Hide the add button
        self.addButton.grid_remove()

    def update_callbacks(self, startIndex:int=0):
        """
        update_callbacks Update callback arguments which are related to the row index of an entry

        :param startIndex: Index of the first entry to update, defaults to 0
        :type startIndex: integer, optional
        """        
        for entry in self.lEntries[startIndex:]:
            if (
                len(entry.lWidgets) > 0
                and is_widget_this(entry.lWidgets[-1], WIDGET_TKT_BUTTON)
                and "default" in entry.lWidgets[-1].dCallbackSets
            ):
                # Retreive the callback dictionary from the entry
                callbackSet = entry.lWidgets[-1].dCallbackSets["default"]
                                
                # Update remove entry callback which point to entries below the current one
                # This is used in for the setup and hold and period width parameters in the parameter window
                i = 0
                while i < 25:
                    key = "removeEntry" + str(i)
                    if key in callbackSet.get_keys():
                        callbackSet.update_callback_argument(key,  entry.rowIndex + i)
                        i += 1
                    else: break
                    
                # Update the remove list callback
                # Used where a seperate list is placed inside the entry, could be made redundant if the lVariables is used by such an entry
                if "removeListEntry" in callbackSet.get_keys():
                    callbackSet.update_callback_argument("removeListEntry", entry.rowIndex)
                    
    def __repr__(self): 
        """
        Representation of this class when it is printed or viewed in debugger window

        :return: String of how this object should be represented
        :rtype: string
        """   
        return f"root: {self.root}\naddButton cb: {self.addButton.dCallbackSets[self.addButton.currentMode]}\nbaseRowIndex: {self.baseRowIndex}\nedit mode: {self.editMode}"
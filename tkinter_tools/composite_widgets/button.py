# ==================================================================== #
#  File name:      button.py                    #        _.==._        #
#  Author:         Arjan Lemmens                #     .+=##**##=+.     #
#  Date:           13-Mar-2023                  #    *= #        =*    #
# ============================================= #   #/  #         \#   #
#  Description:    Custom composite button      #  |#   #   $      #|  #
#                  widgets                      #  |#   #   #      #|  #
#  Rev:            3.0                          #   #\  #   #     /#   #
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
# ==================================================================== #
#  To-Do: !=Priority, ~=Bug, ?=Idea/nice to have                       #
#                                                                      #
# ==================================================================== #

# =========== #
#   Imports   #
# =========== #
import tkinter as tk
from tkinter_tools.fancy_callbacks import CallbackSet

# =========== #
#   Classes   #
# =========== #
class Button(tk.Button):
    """ A more advanced version of the tk.Button widget.
        This class adds more versatile callback handling.
        The class uses dictionaries to save callbacks in modes, 
        allowing collections of callbacks to be entered and switched between.
        Each mode can have multiple callbacks (together with arguments) attached.
        The callbacks are sorted using their key, and are run in the order added.
        This order can be altered. (see fancy_callbacks.py)
    """

    def __init__(self, parent=None, lightImage=None, darkImage=None, **kwargs):
        """Constructor

        :param parent: Parent tkinter frame, defaults to None
        :type parent: tkinter frame, optional
        :param lightImage: Image shown in light theme, defaults to None
        :type lightImage: ImageTK, optional
        :param darkImage: Image shown in dark theme, defaults to None
        :type darkImage: ImageTK, optional
        """
        # Initialize the inherited button
        kwargs["command"] = self.call_callbacks
        super().__init__(parent, **kwargs)

        # Save the images
        self.darkImage = darkImage
        """Image shown in dark mode"""

        self.lightImage = lightImage
        """Image shown in light mode"""

        self.currentMode = "default"
        """Current mode key, this controls which callbacks will be called"""

        self.dCallbackSets = dict()
        """Dictionary of callback sets"""

    def __del__(self):
        """Class destructor"""
        try:
            super().destroy()
            self.dCallbackSets.clear()
        except:
            pass

    def set_theme(self, mode:str="light"):
        """set_theme Set color mode of this object

        :param mode: Name of mode, "dark" and "light" are supported, defaults to "light"
        :type mode: string, optional
        """
        if mode == "dark" and self.darkImage is not None:
            super().configure(image=self.darkImage)
        elif self.lightImage is not None:
            super().configure(image=self.lightImage)

    def call_callbacks(self):
        """ Call all callbacks in this mode """
        if self.currentMode in self.dCallbackSets:
            self.dCallbackSets[self.currentMode].call_callbacks()

    def add_callback(self, modeKey:str="default", callbackKey:str="default", callback=None, argument=None):
        """add_callback Add a callback to the button

        :param modeKey: Name of the mode too which the callback needs to be added, defaults to "default"
        :type modeKey: string, optional
        :param callbackKey: Descriptive name of the callback, defaults to "default"
        :type callbackKey: string, optional
        :param callback: The callback to add, defaults to None
        :type callback: function, optional
        :param argument: Arguments to enter when running the callback, defaults to None
        :type argument: any, optional
        """
        # Add new mode if it's not already present
        if modeKey not in self.dCallbackSets:
            self.dCallbackSets[modeKey] = CallbackSet()

        # Add the callback to the calback set
        self.dCallbackSets[modeKey].add_callback(
            callbackKey, callback, argument)

    def set_mode(self, modeKey:str="default"):
        """set_mode Set the current callback mode

        :param modeKey: Name of the mode which the button needs to called upon a click, defaults to "default"
        :type modeKey: string, optional
        """
        if modeKey in self.dCallbackSets:
            self.currentMode = modeKey
    
    def __repr__(self):
        """
        Representation of this class when it is printed or viewed in debugger window

        :return: String of how this object should be represented
        :rtype: string
        """
        return f"mode: {self.currentMode}, cb: {self.dCallbackSets[self.currentMode]}"
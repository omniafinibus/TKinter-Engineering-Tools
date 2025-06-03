# ==================================================================== #
#  File name:      scrollable_frame.py          #        _.==._        #
#  Author:         Arjan Lemmens                #     .+=##**##=+.     #
#  Date:           24-Aug-2023                  #    *= #        =*    #
# ============================================= #   #/  #         \#   #
#  Description:    Provides a frame in which    #  |#   #   $      #|  #
#                  widgets can be placed. The   #  |#   #   #      #|  #
#                  widgets main feature is that #   #\  #   #     /#   #
#                  it's scrollable.             #    *= #   #    =+    #
#  Rev:            2.2                          #     *++######++*     #
#                                               #        *-==-*        #
# ==================================================================== #
#  Revision history:                                                   #
#  Date        Description                                             #
#  31-Feb-2023 File created                                            #
#  11-May-2023 Cleaned code and added comments                         #
#  24-Aug-2023 Tweaked update_scroll and set_size                      #
#  24-Aug-2023 Added _clean_scroll for better scrolling                #
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
class ScrollableFrame:
    """ Frame holding the scroll window in which widgets can be placed.
        To add widgets use, the frame attribute
    """
    
    def __init__(self, parent, flexibleWidth:bool=False, **kwargs):
        """Constructor

        :param parent: Parent frame in which to place the scrollable frame
        :type parent: tkinter.Frame
        :param flexibleWidth: The width of the window will be changed based on the internal frame, defaults to False
        :type flexibleWidth: boolean, optional
        """
        self.uberRoot=ttk.Frame(parent)
        """ Outer most frame, this frame holds the canvas """
        self.uberRoot.grid(**kwargs, sticky="news")

        # Add the canvas on which
        self.scrollCanvas=tk.Canvas(self.uberRoot)
        """ Canvas which allows a frame to be placed in it, placed inside the uberroot """
        self.scrollCanvas.grid(column=0, row=0, sticky="news")
        
        # Add scroll bar
        self.scrollBar=ttk.Scrollbar(self.uberRoot, orient="vertical", command=self._clean_scroll)
        """ Scrollbar, placed in uberroot """
        self.scrollBar.grid(column=1, row=0, sticky="ns")

        # Place frame in the scroll window  # self.frame=ttk.Frame(self.scrollCanvas)
        self.frame=ttk.Frame(self.scrollCanvas)
        """ Frame actually allowing widgets to be placed inside """
        self.scrollCanvas.create_window((0, 0), window=self.frame, anchor="nw")

        # Connecting scroll bar to canvas
        self.scrollCanvas.configure(yscrollcommand=self.scrollBar.set) 
        
        # Attach scrolling on the frame to scrolling in the canvas # self.frame.bind("<Configure>", lambda event, canvas=self.scrollCanvas: self.update_scroll())
        self.frame.bind("<Configure>", lambda event: self.update_scroll(configEvent=event, flexibleWidth=flexibleWidth))
        
        # Bind scroll button to widgets (so that it actives when mouse hovers over them)
        self.bind_widget(self.scrollCanvas)
        self.bind_widget(self.uberRoot)
        self.bind_widget(self.frame)
        self.bind_widget(self.scrollBar)

    def _clean_scroll(self, *args):
        """
        A more robust way of scrolling compared to the original direct use of yview
        """        
        if args[0] == 'scroll':
            self.scrollCanvas.yview_scroll(1 if int(args[1])>0 else -1, args[2])
                
        elif args[0] == 'moveto':
            if float(args[1]) < 1.0 and float(args[1]) > 0.0:
                self.scrollCanvas.yview_moveto(float(args[1]))  

    def bind_widget(self, widget):
        """Make the scroll window scroll when the scroll wheel is used when hovering over the provided widget

        :param widget: Widget over which the mouse hover allows scrolling
        :type widget: tkinter, ttk, composite_widgets widget
        """
        widget.bind("<MouseWheel>", self._clean_scroll) # Windows mouse wheel event
        widget.bind("<Button-4>", self._clean_scroll) # Linux mouse wheel event (Up)
        widget.bind("<Button-5>", self._clean_scroll) # Linux mouse wheel event (Down)

    def update_scroll(self, configEvent=None, flexibleWidth:bool=False):
        """
        Update the size of the scrollbar, this method should be called whenever the amount of rows or columns is changed

        :param configEvent: Tkinter configuration event, defaults to None
        :type configEvent: Event, optional
        :param flexibleWidth: Also update the width of the frame based on the internal frame, defaults to False
        :type flexibleWidth: boolean, optional
        """
        if configEvent:
            # If scroll region is smaller than scroll canvas hide the scroll bar
            if configEvent.height <= self.scrollBar.winfo_height():
                offset = self.scrollBar.winfo_width()
                self.scrollBar.grid_remove()
            else:
                offset = 0
                self.scrollBar.grid()
                
            if flexibleWidth:
                # Update the window width based on the scroll region
                self.uberRoot.configure(width=configEvent.width+25+offset)
                self.scrollCanvas.configure(width=configEvent.width+2+offset)
                
            # Update the scroll region
            self.scrollCanvas.configure(scrollregion=(configEvent.x, configEvent.y if configEvent.y <= 0 else 0, configEvent.width, configEvent.height))

    def grid_info(self, **kwargs):
        """Return information about the options
        for positioning this widget in a grid"""
        return self.uberRoot.grid_info(**kwargs)

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
        return self.uberRoot.grid(**kwargs)

    def grid_remove(self, **kwargs):
        """Unmap this widget but remember the grid options"""
        return self.uberRoot.grid_remove(**kwargs)
    
    def set_size(self, width:int=None, height:int=None):
        """
        Set the size of the frame

        :param width: Width of frame in pixels, defaults to None
        :type width: integer, optional
        :param height: height of frame in pixels, defaults to None
        :type height: integer, optional
        """        
        if width and height:
            self.uberRoot.configure(width=width-4, height=height)
            self.scrollCanvas.configure(width=width-27, height=height-2)
            self.frame.configure(width=width-29)
        elif width:
            self.uberRoot.configure(width=width-4)
            self.scrollCanvas.configure(width=width-27)
            self.frame.configure(width=width-29)
        elif height:
            self.uberRoot.configure(height=height)
            self.scrollCanvas.configure(height=height-2)
        
        
    def __repr__(self):
        """
        Representation of this class when it is printed or viewed in debugger window

        :return: String of how this object should be represented
        :rtype: string
        """
        return f"uberRoot: {self.uberRoot}\nscrollCanvas: {self.scrollCanvas}\nscrollBar: {self.scrollBar}\nframe: {self.frame}"

class ScrollableLabelFrame(ScrollableFrame):
    """ Frame holding the scroll window in which widgets can be placed.
        To add widgets, use the frame attribute
    """
    
    def __init__(self, parent:ttk.Frame, text:str="", flexibleWidth:bool=False, **kwargs):
        """Constructor

        :param parent: Parent frame in which to place the scrollable frame
        :type parent: tkinter.Frame
        :param text: Name shown at the top of the frame
        :type text: string
        :param flexibleWidth: The width of the window will be changed based on the internal frame, defaults to False
        :type flexibleWidth: boolean, optional
        """
        self.uberRoot=ttk.LabelFrame(parent, text=text)
        """ Outer most frame, this frame holds the canvas """
        self.uberRoot.grid(**kwargs, sticky="news")

        # Add the canvas on which
        self.scrollCanvas=tk.Canvas(self.uberRoot)
        """ Canvas which allows a frame to be placed in it, placed inside the uberroot """
        self.scrollCanvas.grid(column=0, row=0, sticky="news")
        
        # Add scroll bar
        self.scrollBar=ttk.Scrollbar(self.uberRoot, orient="vertical", command=self.scrollCanvas.yview)
        """ Scrollbar, placed in uberroot """
        self.scrollBar.grid(column=1, row=0, sticky="ns")

        # Place frame in the scroll window
        self.frame=ttk.Frame(self.scrollCanvas)
        """ Frame actually allowing widgets to be placed inside """
        self.scrollCanvas.create_window((0, 0), window=self.frame, anchor="nw")
        
        # Connecting scroll bar to canvas
        self.scrollCanvas.configure(yscrollcommand=self.scrollBar.set)
        
        # Attach scrolling on the frame to scrolling in the canvas
        self.frame.bind("<Configure>", lambda event: self.update_scroll(configEvent=event, flexibleWidth=flexibleWidth))

        # Bind scroll button to widgets (so that it actives when mouse hovers over them)
        self.bind_widget(self.scrollCanvas)
        self.bind_widget(self.uberRoot)
        self.bind_widget(self.frame)
        self.bind_widget(self.scrollBar)
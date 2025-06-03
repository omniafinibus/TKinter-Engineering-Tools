# ==================================================================== #
#  File name:      fancy_callbacks.py           #        _.==._        #
#  Author:         Arjan Lemmens                #     .+=##**##=+.     #
#  Date:           22-Aug-2023                  #    *= #        =*    #
# ============================================= #   #/  #         \#   #
#  Description:    This module creates the      #  |#   #   $      #|  #
#                  CallbackSet and              #  |#   #   #      #|  #
#                  FancyCallback classes.       #   #\  #   #     /#   #
#                  The FancyCallback allows a   #    *= #   #    =+    #
#                  callback to be paired with   #     *++######++*     #
#                  an indefinite amount of      #        *-==-*        #
#                  arguments. The CallbackSet   # ==================== #
#                  group callbacks, making it easier to call many      #
#                  callbacks in a specific order.                      #
#  Rev:            2.1                                                 #
# ==================================================================== #
#  Revision history:                                                   #
#  Date        Description                                             #
#  13-Mar-2023 Migrated from composite_widgets to own file             #
#  10-May-2023 Cleaned code and added comments                         #
#  22-Aug-2023 Added representation to classes                         #
# ==================================================================== #
#  To-Do: !=Priority, ~=Bug, ?=Idea/nice to have                       #
#                                                                      #
# ==================================================================== #

#=============#
#   Classes   #
#=============#
class CallbackSet:
    """
     A grouping of callbacks, allowing them to be called in a predefined order by just running the call_callbacks method.
    """    

    def __init__(self):
        """
        __init__ Constructor
        """ 
                
        self.dCallbacks=dict()
        """ Dictionary of callback argument pairs """
        self.lCallbackOrder=list()
        """ List of dictionary keys in the order in which the callbacks are run """

    def clear_all(self):
        """
        Remove all callbacks
        """        
        self.lCallbackOrder.clear()
        self.dCallbacks.clear()

    def update_callback_argument(self, key:str, newArguments):
        """
        update_callback_argument Change the arguments for a callback

        :param key: Key of the callback which needs an argument update
        :type key: string
        :param newArguments: The new arguments, lists will be "exploded"
        :type newArguments: any
        """        
        self.dCallbacks[key].set_argument(newArguments)

    def update_callback_key(self, oldKey:str, newKey:str):
        """
        update_callback_key Change the key of a callback while keeping all other attributes

        :param oldKey: Key of callback which needs to be changed
        :type oldKey: string
        :param newKey: New key
        :type newKey: string
        """        
        if oldKey in self.dCallbacks:
            # Create a new callback argument with the old callback and arguments
            self.dCallbacks[newKey]=FancyCallback(
                callback=self.dCallbacks[oldKey].callback, 
                argument=self.dCallbacks[oldKey].argument
            )

            # Place the new key in the old key's spot
            self.lCallbackOrder.insert(
                self.lCallbackOrder.index(oldKey), 
                newKey
            )
            
            # Delete the old callback
            self.remove_callback(oldKey)

    def add_callback(self, key:str, callback, arguments=None):
        """
        add_callback Add a new callback to the set, it will be run after all other callbacks

        :param key: Key for the new callback
        :type key: string
        :param callback: Callback to attach, not allowed to be a lambda
        :type callback: function
        :param arguments: arguments to run in the callback, lists will be in the order of the argument added, defaults to None
        :type arguments: any, optional
        """
        self.dCallbacks[key]=FancyCallback(callback, arguments)
        self.lCallbackOrder.append(key)

    def remove_callback(self, key:str):
        """
        remove_callback Remove callback from the set.

        :param key: Key of the callback which needs to be removed
        :type key: string
        """        
        self.dCallbacks.pop(key)
        self.lCallbackOrder.remove(key)

    def call_callbacks(self):
        """
        call_callbacks Run all callbacks in the order of lCallbackOrder
        """        
        for key in self.lCallbackOrder:
            self.dCallbacks[key].call_callback()

    def get_keys(self):
        """
        get_keys Get the keys of the callbacks in the order in which they're called

        :return: List of keys
        :rtype: list[string]
        """        
        return self.lCallbackOrder

    def set_callback_order(self, lKeys:list):
        """
        set_callback_order Set the callbacks into a new order, if the key provided is not in the dictionary it will be omitted

        :param lKeys: List of keys in the correct order
        :type lKeys: list
        """        
        # Clear the list to save the new callback order
        self.lCallbackOrder.clear()

        # Create new callback order if the callbacks are present
        self.lCallbackOrder = [key for key in lKeys if key in self.dCallbacks.keys()]
    
    def __repr__(self):
        """
        Representation of this class when it is printed or viewed in debugger window

        :return: String of how this object should be represented
        :rtype: string
        """        
        return "\n".join([f"{index}: {key}-{self.dCallbacks[key]}" for index, key in enumerate(self.lCallbackOrder)])

class FancyCallback:
    """
    Class holding both the callback and arguments which need to be placed in the callback at runtime
    """    

    def __init__(self, callback, argument=None):
        """
        Constructor

        :param callback: The callback
        :type callback: function
        :param argument: Arguments, if the arguments are in a list, the order of the items will be the order in which they are entered, defaults to None
        :type argument: any, optional
        """        
        
        self.callback=callback
        """ The callback which is run at call_callback() """
        self.argument=argument
        """ The arguments, this can contain no arguments, 1 argument or a list """

    def call_callback(self):
        """
        Run the callback saved in this object, together with the provided arguments
        """        
        
        if isinstance(self.argument, list):
            self.callback(*self.argument)
        elif self.argument is not None:
            self.callback(self.argument)
        else:
            self.callback()

    def set_argument(self, argument=None):
        """
        Change the argument entered when the callback is run

        :param argument: New arguments, if the arguments are in a list, the order of the items will be the order in which they are entered, defaults to None
        :type argument: any
        """        
        self.argument=argument
        
    def __repr__(self):
        """
        Representation of this class when it is printed or viewed in debugger window

        :return: String of how this object should be represented
        :rtype: string
        """        
        return f"{self.callback.__name__}(" + ", ".join(self.argument) if isinstance(self.argument, list) else str(self.argument) + ")"
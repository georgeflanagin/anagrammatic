# -*- coding: utf-8 -*-
import typing
from   typing import *

###
# Standard imports.
###

import os
import sys

from   multiprocessing import shared_memory
import platform

###
# Parts of this project.
###

from   gkfdecorators import show_exceptions_and_frames as trap

###
# Credits
###
__author__ = 'George Flanagin'
__copyright__ = 'Copyright 2020'
__credits__ = None
__version__ = 1.0
__maintainer__ = 'George Flanagin'
__email__ = ['me@georgeflanagin.com', 'gflanagin@richmond.edu']
__status__ = 'Teaching example'
__license__ = 'MIT'

class PidList:
    """
    Class to keep track of pids in a multiprocessing environment.
    """
    def __init__(self, name:str=None, list_size:int=128):

        self.list_size = list_size
        # Initialize correctly based on whether we are the creator
        # of the list or latching onto one that already exists.
        self.creator = name is None
        if self.creator:
            self.pids = shared_memory.ShareableList( [0]*list_size )
        else:
            self.pids = shared_memory.ShareableList( None, name=name )

        self.name = self.pids.shm.name if name is None else name

        # always add our own pid to the list.
        self += os.getpid()
        

    def __del__(self) -> None:
        if self.creator: 
            self.pids.unlink() 
        else:
            self.pids.close()
    
    def __len__(self) -> int:
        """
        return the number of pids currently in the PidList.
        """ 
        return self.list_size - self.pids.count(0)


    def __str__(self) -> str:
        """ 
        return the name of this PidList.
        """
        return self.name
                 

    def __iadd__(self, pid:int) -> None:
        """
        Add pid to the PidList object.
        """
        try:
            self[self.index(0)] = pid
        except ValueError as e:
            print(f"{self.name} is full")   


    def __isub__(self, pid:int) -> None:
        """
        Remove pid from the PidList object.
        """ 
        try:
            self[self.index(pid)] = 0
        except ValueError as e:
            print(f"{pid} was not in the list.")



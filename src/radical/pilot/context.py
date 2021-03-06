#pylint: disable=C0301, C0103, W0212

"""
.. module:: radical.pilot.context
   :platform: Unix
   :synopsis: Implementation of the Context class(es).

.. moduleauthor:: Ole Weidner <ole.weidner@rutgers.edu>
"""

__copyright__ = "Copyright 2013-2014, http://radical.rutgers.edu"
__license__   = "MIT"

import saga

# ------------------------------------------------------------------------------
#
class Context (saga.Context):

    # --------------------------------------------------------------------------
    #
    def __init__ (self, ctype, thedict=None) :

        # init the saga.Context
        self._apitype  = 'saga.Context'
        super (Context, self).__init__ (ctype, )

        # set given defaults
        if  thedict :
            for key in thedict :
                self.set_attribute (key, thedict[key])


    #---------------------------------------------------------------------------
    #
    @classmethod
    def from_dict(cls, thedict):
        """
        Creates a new object instance from a string.
        c._from_dict(x.as_dict) == x
        """

        return cls(thedict)


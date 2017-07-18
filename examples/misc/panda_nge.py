#!/usr/bin/env python

import radical.pilot as rp


#------------------------------------------------------------------------------
#
if __name__ == '__main__':

    panda_nge = None

    try:
        panda_nge = rp.PandaNGE(url=None)

        print 'uid'
        print panda_nge.uid

        print 'list resources'
        print panda_nge.list_resources()

        print 'find resources'
        print panda_nge.find_resources()

        print 'get_resource_info'
        print panda_nge.get_resource_info()

        print 'get_resource_states'
        print panda_nge.get_resource_states()

        print 'wait_resource_states'
        print panda_nge.wait_resource_states(states=rp.PMGR_ACTIVE)

    finally:
        if panda_nge:
            panda_nge.close()



#-------------------------------------------------------------------------------


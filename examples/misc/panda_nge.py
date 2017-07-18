#!/usr/bin/env python

import radical.utils as ru
import radical.pilot as rp


#------------------------------------------------------------------------------
#
if __name__ == '__main__':

    panda_nge = None
    try:
        panda_nge = rp.PandaNGE(url=None)

        print 'inspect resources'
        print panda_nge.list_resources()
        print

        print 'find resources'
        print panda_nge.find_resources()
        print

        print 'get_resource_info'
        print panda_nge.get_resource_info()
        print

        print 'get_resource_states'
        print panda_nge.get_resource_states()
        print

        print 'wait_resource_states'
        print panda_nge.wait_resource_states(states=rp.PMGR_ACTIVE)
        print

        print 'submit a task'
        print panda_nge.submit_tasks([{'executable' : '/bin/true'}])
        print

        print 'list tasks'
        print panda_nge.list_tasks()
        print

        print 'get task states'
        print panda_nge.get_task_states()
        print

        print 'wait for task completion'
        print panda_nge.wait_task_states(states=rp.FINAL)
        print

    finally:
        if panda_nge:
            print 'close panda-nge session'
            panda_nge.close()
            print



#-------------------------------------------------------------------------------


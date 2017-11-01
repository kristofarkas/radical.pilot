#!/usr/bin/env python

import radical.utils as ru
import radical.pilot as rp


#------------------------------------------------------------------------------
#
if __name__ == '__main__':

    panda_nge = None
    try:
      # panda_nge = rp.PandaNGE(binding=rp.RP,  url=None)
        panda_nge = rp.PandaNGE(binding=rp.RPS, url='http://localhost:8090/')


        print 'request backfill resources'
        pprint.pprint(panda_nge.request_backfill_resources(
                                           {'resource' : 'ornl.titan_orte', 
                                            'queue'    : 'debug',
                                            'project'  : "CSC230"},
                                           partition='titan',
                                           max_cores=30*5,
                                           max_walltime=30))
        print

        print 'inspect resources'
        print panda_nge.list_resources()
        print
        sys.exit()

        print 'request resources'
        print panda_nge.request_resources([{'resource' : 'ornl.titan_orte', 
                                            'queue'    : 'debug',
                                            'cores'    : 16*5,
                                            'project'  : "CSC230",
                                            'walltime' : 20}])
        print

        print 'inspect resources'
        print panda_nge.list_resources()
        print

        print 'find resources'
        print panda_nge.find_resources()
        print

        print 'get_requested_resources'
        print panda_nge.get_requested_resources()
        print

        print 'get_available_resources'
        print panda_nge.get_available_resources()
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


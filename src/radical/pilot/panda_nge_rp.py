
__copyright__ = "Copyright 2013-2014, http://radical.rutgers.edu"
__license__   = "MIT"


import os
import sys

from .panda_nge import PandaNGE

from .session                   import *
from .pilot_manager             import *
from .unit_manager              import *
from .compute_unit_description  import *
from .compute_pilot_description import *
from .states                    import *

# --------------------------------------------------------------------------
#
# see https://docs.google.com/document/d/1bm8ucgfi9SHjDy0w-ZX5NIdkjk87qFClMB9jMse75uM
#
class PandaNGE_RP(PandaNGE):
    '''
    This is the RP bound implementation of the abstract PandaNGE class/
    '''

    # --------------------------------------------------------------------------
    #
    def __init__(self, url=None):
        '''
        url: contact point (unused)
        '''

        self._url = url
        self._session = Session()
        self._pmgr    = PilotManager(self._session)
        self._umgr    = UnitManager(self._session)

        self._umgr.register_callback(self._unit_state_cb)


    # --------------------------------------------------------------------------
    #
    @property
    def uid(self):

        return self._session.uid


    # --------------------------------------------------------------------------
    #
    def close(self):

        self._session.close()


    # --------------------------------------------------------------------------
    #
    def request_resources(self, requests):
        '''
        request a new resource (ie. submit a new RP pilot) for a given set of
        cores / walltime.
        '''


        pds = list()
        for request in requests:
            pd  = {'resource': 'local.localhost',
                    'cores'   : request['cores'],
                    'runtime' : request['walltime']
                  }
            pds.append(ComputePilotDescription(pd))

        pilots = self._pmgr.submit_pilots(pds)
        self._umgr.add_pilots(pilots)


    # --------------------------------------------------------------------------
    #
    def list_resources(self):

        return [pilot.uid for pilot in self._pmgr.get_pilots()]


    # --------------------------------------------------------------------------
    #
    def find_resources(self, states=None):

        if   not states                  : states = list()
        elif not isinstance(states, list): states = [states]

        ret = list()
        if states:
            for pilot in self._pmgr.get_pilots():
                if pilot.state in states:
                    ret.append(pilot.uid)
        else:
            ret = self._pmgr.list_pilots()

        return ret


    # --------------------------------------------------------------------------
    #
    def get_requested_resources(self):

        ret = list()
        for info in self.get_resource_info():
            ret.append([info['uid'], info['state'], 
                        info['description']['cores'], 
                        info['description']['runtime']
                      ])

        return ret


    # --------------------------------------------------------------------------
    #
    def get_available_resources(self):

        ret = list()
        for info in self.get_resource_info():
            if info['state'] == PMGR_ACTIVE:
                ret.append([info['uid'], info['state'], 
                            info['description']['cores'], 
                            info['description']['runtime']
                           ])

        return ret


    # --------------------------------------------------------------------------
    #
    def get_resource_info(self, resource_ids=None):

        if   not resource_ids                  : resource_ids = list()
        elif not isinstance(resource_ids, list): resource_ids = [resource_ids]

        ret = list()
        if resource_ids:

            pilots = self._pmgr.get_pilots()

            if   not pilots                  : pilots = list()
            elif not isinstance(pilots, list): pilots = [pilots]

            for pilot in pilots:
                if pilot.uid in resource_ids:
                    ret.append(pilot.as_dict())
        else:
            for pilot in self._pmgr.get_pilots():
                ret.append(pilot.as_dict())

        return ret


    # --------------------------------------------------------------------------
    #
    def get_resource_states(self, resource_ids=None):

        pilots = self._pmgr.get_pilots(resource_ids)

        if   not pilots                  : pilots = list()
        elif not isinstance(pilots, list): pilots = [pilots]

        return [pilot.state for pilot in pilots]


    # --------------------------------------------------------------------------
    #
    def wait_resource_states(self, resource_ids=None, states=None, timeout=None):

        return self._pmgr.wait_pilots(uids=resource_ids, state=states,
                                      timeout=timeout)


    # --------------------------------------------------------------------------
    #
    def submit_tasks(self, descriptions):

        # FIXME: we actually get PANDA task descriptions here, which we need to
        #        translate into RP unit descriptions

        # before we hand over tasks to the RP layer, we will stage files
        # FIXME: panda level input file staging goes here.

        cuds = list()
        for descr in descriptions:
            cuds.append(ComputeUnitDescription(descr))

        units = self._umgr.submit_units(cuds)

        return [unit.uid for unit in units]


    # --------------------------------------------------------------------------
    #
    def _unit_state_cb(self, unit, state):

        # once the units are in final state, we can run the panda output staging
        # routines.  To learn about final units, we registered this unit state
        # callback.on umgr creation.
        if state == DONE:
            pass
            # FIXME: panda level output file staging goes here.
            # FIXME: we need to make sure that PANDA is informed when our output
            #        staging is done, and when the units can be controlled by
            #        the panda layer again.  For that, we will set
            #            'control': 'panda_pending'
            #        in the unit dict returned to Panda on inspection, to signal
            #        that control is relinguished.  Note that `DONE` is
            #        insufficient, precisely because of the additional output
            #        staging.
            # NOTE:  can we translate the panda staging into proper RP staging
            #        directives, to avoid explicit control management?

            
    # --------------------------------------------------------------------------
    #
    def list_tasks(self):

        return self._umgr.list_units()


    # --------------------------------------------------------------------------
    #
    def get_task_states(self, task_ids=None):

        if   not task_ids                  : task_ids = []
        elif not isinstance(task_ids, list): task_ids = [task_ids]

        units = self._umgr.get_units(task_ids)

        if   not units:                   units = list()
        elif not isinstance(units, list): units = [units]

        return [unit.state for unit in units]


    # --------------------------------------------------------------------------
    #
    def wait_task_states(self, task_ids=None, states=None, timeout=None):

        return self._umgr.wait_units(uids=task_ids, state=states,
                                     timeout=timeout)


# ------------------------------------------------------------------------------


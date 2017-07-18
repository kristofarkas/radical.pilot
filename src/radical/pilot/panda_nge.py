
__copyright__ = "Copyright 2013-2014, http://radical.rutgers.edu"
__license__   = "MIT"



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
class PandaNGE(object):

    # --------------------------------------------------------------------------
    #
    def __init__(self, url):
        '''
        url: bridge db URL
        '''

        self._url = url
        self._session = Session()
        self._pmgr    = PilotManager(self._session)
        self._umgr    = UnitManager(self._session)

        pd = {'resource' : 'local.localhost',
              'cores'    : 4, 
              'runtime'  : 15}
        self._pmgr.submit_pilots(ComputePilotDescription(pd))


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
    def get_resource_info(self, resource_ids=None):

        if   not resource_ids                  : resource_ids = list()
        elif not isinstance(resource_ids, list): resource_ids = [resource_ids]

        ret = list()
        if resource_ids:
            for pilot in self._pmgr.get_pilots():
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
        return [pilot.state for pilot in pilots]


    # --------------------------------------------------------------------------
    #
    def wait_resource_states(self, resource_ids=None, states=None, timeout=None):

        return self._pmgr.wait_pilots(uids=resource_ids, state=states,
                                      timeout=timeout)


    # --------------------------------------------------------------------------
    #
    def submit_units(self, descriptions):

        units = self._umgr.submit_units(descriptions)

        return [unit.uid for unit in units]


    # --------------------------------------------------------------------------
    #
    def get_unit_states(self, unit_ids=None):

        units = self._umgr.get_units()
        return [unit.state for unit in units]


    # --------------------------------------------------------------------------
    #
    def wait_unit_states(self, unit_ids=None, states=None, timeout=None):

        return self._umgr.wait_units(uids=unit_ids, state=states,
                                     timeout=timeout)


# ------------------------------------------------------------------------------


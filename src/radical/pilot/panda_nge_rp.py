
__copyright__ = "Copyright 2013-2014, http://radical.rutgers.edu"
__license__   = "MIT"

from .panda_nge import PandaNGE

from .session                   import *
from .pilot_manager             import *
from .unit_manager              import *
from .compute_unit_description  import *
from .compute_pilot_description import *
from .states                    import *

RP   = 'radical.pilot'
RPS  = 'radical.pilot.service'
DB   = 'radical.pilot.db'

# --------------------------------------------------------------------------
#
# see https://docs.google.com/document/d/1bm8ucgfi9SHjDy0w-ZX5NIdkjk87qFClMB9jMse75uM
#
class PandaNGE_RP(PandaNGE):
    '''
    This is an abstract base class for the Panda-NGE integration API.  We will
    provide different implementations to use it:

      - simple mockup dircetly against RP, for ease of testing
      - REST based against the integration service, for testing and tight
        integration
      - MongoDB based according to the plan layed out in the document above

    The API binding is determined at session construction, and default to RP.
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

        pd = {'resource' : 'local.localhost',
              'cores'    : 4, 
              'runtime'  : 15}
        pilot = self._pmgr.submit_pilots(ComputePilotDescription(pd))
        self._umgr.add_pilots(pilot)


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
    def submit_tasks(self, descriptions):

        cuds = list()
        for descr in descriptions:
            cuds.append(ComputeUnitDescription(descr))

        units = self._umgr.submit_units(cuds)

        return [unit.uid for unit in units]


    # --------------------------------------------------------------------------
    #
    def get_task_states(self, task_ids=None):

        units = self._umgr.get_units(task_ids)
        return [unit.state for unit in units]


    # --------------------------------------------------------------------------
    #
    def wait_task_states(self, task_ids=None, states=None, timeout=None):

        return self._umgr.wait_units(uids=task_ids, state=states,
                                     timeout=timeout)


# ------------------------------------------------------------------------------


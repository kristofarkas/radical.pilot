
__copyright__ = "Copyright 2013-2014, http://radical.rutgers.edu"
__license__   = "MIT"



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
class PandaNGE(object):
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
    def __init__(self, binding=RP, url=None):
        '''
        binding: API implementation binding [RP, RPS, DB]
        url    : contact point for the service and DB bindings
        '''

        from .panda_nge_rp import PandaNGE_RP

        if   binding == RP : self._binding = PandaNGE_RP (url)
        elif binding == RPS: self._binding = PandaNGE_RPS(url)
        elif binding == DB : self._binding = PandaNGE_DB (url)
        else               : raise ValueError('unknown binding %s' % binding)


    # --------------------------------------------------------------------------
    #
    @property
    def uid(self):

        return self._binding.uid


    # --------------------------------------------------------------------------
    #
    def close(self):

        return self._binding.close()


    # --------------------------------------------------------------------------
    #
    def list_resources(self):

        return self._binding.list_resources()


    # --------------------------------------------------------------------------
    #
    def find_resources(self, states=None):

        return self._binding.find_resources(states)


    # --------------------------------------------------------------------------
    #
    def get_resource_info(self, resource_ids=None):

        return self._binding.get_resource_info(resource_ids)


    # --------------------------------------------------------------------------
    #
    def get_resource_states(self, resource_ids=None):

        return self._binding.get_resource_states(resource_ids)

    # --------------------------------------------------------------------------
    #
    def wait_resource_states(self, resource_ids=None, states=None, timeout=None):

        return self._binding.wait_resource_states(resource_ids, states, timeout)


    # --------------------------------------------------------------------------
    #
    def submit_tasks(self, descriptions):

        return self._binding.submit_tasks(descriptions)


    # --------------------------------------------------------------------------
    #
    def list_tasks(self):

        return self._binding.list_tasks()


    # --------------------------------------------------------------------------
    #
    def get_task_states(self, task_ids=None):

        return self._binding.get_task_states(task_ids)


    # --------------------------------------------------------------------------
    #
    def wait_task_states(self, task_ids=None, states=None, timeout=None):

        return self._binding.wait_task_states(task_ids, states, timeout)


# ------------------------------------------------------------------------------


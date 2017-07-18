
def magic(*arg, **kwarg):
    return None


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
        self._session = rp.Session()
        self._pmgr    = rp.PilotManager(self._session)
        self._umgr    = rp.UnitManager(self._session)


    # --------------------------------------------------------------------------
    #
    def list_resources(self):

        return [pilot.uid for pilot in self._pmgr.get_pilots()]


    # --------------------------------------------------------------------------
    #
    def find_resources(self, states):

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
    def get_resource_states(self, resource_ids):

        pilots = self._pmgr.get_pilots(resource_ids)
        return [pilot.state for pilot in pilots]



    # --------------------------------------------------------------------------
    #
    def get_resource_info(self, resource_ids):

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
    def wait_resource(self, resource_ids, states, timeout=None):

        return self._pmgr.wait_units(uids=resource_ids, state=states,
                                     timeout=timeout)


    # --------------------------------------------------------------------------
    #
    def get_states(self, unit_ids):

        units = self._umgr.get_units(unit_ids)
        return [unit.state for unit in units]




    # --------------------------------------------------------------------------
    #
    def submit_units(self, descriptions):

        units = self._umgr.submit_units(descriptions)

        return [unit.uid for unit in units]


    # --------------------------------------------------------------------------
    #
    def wait_units(self, unit_ids, states, timeout=None):

        return self._umgr.wait_units(uids=unit_ids, state=states,
                                     timeout=timeout)


    # --------------------------------------------------------------------------
    #
    def get_states(self, unit_ids):

        units = self._umgr.get_units()
        return [unit.state for unit in units]








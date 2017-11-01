#!/usr/bin/env python

__copyright__ = "Copyright 2017, http://radical.rutgers.edu"
__license__   = "MIT"


import radical.utils as ru
import radical.pilot as rp

import bottle
import json


# ------------------------------------------------------------------------------
# https://stackoverflow.com/questions/8725605/
def methodroute(route, **kwargs):
    def decorator(f):
        f.route = route
        for arg in kwargs:
            setattr(f, arg, kwargs[arg])
        return f
    return decorator

def routeapp(obj):
    for kw in dir(obj):
        attr = getattr(obj, kw)
        if hasattr(attr, "route"):
            if hasattr(attr, "method"):
                method = getattr(attr, "method")
            else:
                method = "GET"
            if hasattr(attr, "callback"):
                callback = getattr(attr, "callback")
            else:
                callback = None
            if hasattr(attr, "name"):
                name = getattr(attr, "name")
            else:
                name = None
            if hasattr(attr, "apply"):
                aply = getattr(attr, "apply")
            else:
                aply = None
            if hasattr(attr, "skip"):
                skip = getattr(attr, "skip")
            else:
                skip = None

            bottle.route(attr.route, method, callback, name, aply, skip)(attr)



# ------------------------------------------------------------------------------
#
class PandaNGE_Server(object):

    # --------------------------------------------------------------------------
    #
    def __init__(self):

        self._log     = ru.get_logger('radical.pilot.nge')
        self._backend = rp.PandaNGE(binding=rp.RP)
        self._closed  = False



    # --------------------------------------------------------------------------
    #
    @methodroute('/close/', method="PUT")
    def close(self):

        try:
            self._log.info('closing')
            self._closed = True
            self._backend.close()
            self._log.info('closed')
            return {"success" : True,
                    "result"  : None}
        except Exception as e:
            self._log.exception('oops')
            return {"success" : False,
                    "error"   : repr(e)}


    # --------------------------------------------------------------------------
    #
    def _is_alive(self):

        if self._closed:
            raise RuntimeError('session closed')

    # --------------------------------------------------------------------------
    #
    def serve(self):

        self._log.info('start serving')
        bottle.run(host='localhost', port=8090, debug=True)


    # --------------------------------------------------------------------------
    #
    @methodroute('/uid/', method="GET")
    def uid(self):

        try:
            ret = self._backend.uid
            return {"success" : True,
                    "result"  : ret}
        except Exception as e:
            self._log.exception('oops')
            return {"success" : False,
                    "error"   : repr(e)}



    # --------------------------------------------------------------------------
    #
    @methodroute('/resources/backfill/<partition>/<max_cores>-<max-walltime>/', method="PUT")
    def request_backfill_resources(self, partition, max_cores, max_walltime):

        request_stub = json.loads(bottle.request.body.read())

        try:
            ret = self._backend.request_resources(request_stub, partition,
                                                  max_cores, max_walltime)
            return {"success" : True,
                    "result"  : ret}
        except Exception as e:
            self._log.exception('oops')
            return {"success" : False,
                    'error'   : repr(e)}


    # --------------------------------------------------------------------------
    #
    @methodroute('/resources/', method="PUT")
    def request_resources(self):

        requests = json.loads(bottle.request.body.read())

        try:
            ret = self._backend.request_resources(requests)
            return {"success" : True,
                    "result"  : ret}
        except Exception as e:
            self._log.exception('oops')
            return {"success" : False,
                    'error'   : repr(e)}


    # --------------------------------------------------------------------------
    #
    @methodroute('/resources/', method="GET")
    def list_resources(self):

        try:
            ret = self._backend.list_resources()
            return {"success" : True,
                    "result"  : ret}
        except Exception as e:
            self._log.exception('oops')
            return {"success" : False,
                    'error'   : repr(e)}


    # --------------------------------------------------------------------------
    #
    @methodroute('/resources/<states>', method="GET")
    def find_resources(self, states=None):

        try:
            ret = self._backend.find_resources(states)
            return {"success" : True,
                    "result"  : ret}
        except Exception as e:
            self._log.exception('oops')
            return {"success" : False,
                    'error'   : repr(e)}


    # --------------------------------------------------------------------------
    #
    @methodroute('/resources/requested', method="GET")
    def get_requested_resources(self):

        try:
            ret = self._backend.get_requested_resources()
            return {"success" : True,
                    "result"  : ret}
        except Exception as e:
            self._log.exception('oops')
            return {"success" : False,
                    'error'   : repr(e)}


    # --------------------------------------------------------------------------
    #
    @methodroute('/resources/available', method="GET")
    def get_available_resources(self):

        try:
            ret = self._backend.get_available_resources()
            return {"success" : True,
                    "result"  : ret}
        except Exception as e:
            self._log.exception('oops')
            return {"success" : False,
                    'error'   : repr(e)}


    # --------------------------------------------------------------------------
    #
    @methodroute('/resources/<resource_ids>/info', method="GET")
    def get_resource_info(self, resource_ids):

        try:
            ret = self._backend.get_resource_info(resource_ids)
            return {"success" : True,
                    "result"  : ret}
        except Exception as e:
            self._log.exception('oops')
            return {"success" : False,
                    'error'   : repr(e)}


    # --------------------------------------------------------------------------
    #
    @methodroute('/resources/<resource_ids>/state', method="GET")
    def get_resource_states(self, resource_ids):

        try:
            ret = self._backend.get_resource_states(resource_ids)
            return {"success" : True,
                    "result"  : ret}
        except Exception as e:
            self._log.exception('oops')
            return {"success" : False,
                    'error'   : repr(e)}


    # --------------------------------------------------------------------------
    #
    @methodroute('/resources/<resource_ids>/wait/<states>/<timeout>', method="GET")
    def wait_resource_states(self, resource_ids, states, timeout):

        try:
            ret = self._backend.wait_resource_states(resource_ids, states, timeout)
            return {"success" : True,
                    "result"  : ret}
        except Exception as e:
            self._log.exception('oops')
            return {"success" : False,
                    'error'   : repr(e)}


    # --------------------------------------------------------------------------
    #
    @methodroute('/tasks/', method="GET")
    def list_tasks(self):

        try:
            ret = self._backend.list_tasks()
            return {"success" : True,
                    "result"  : ret}
        except Exception as e:
            self._log.exception('oops')
            return {"success" : False,
                    'error'   : repr(e)}


    # --------------------------------------------------------------------------
    #
    @methodroute('/tasks/', method="PUT")
    def submit_tasks(self):

        descriptions = json.loads(bottle.request.body.read())

        try:
            ret = self._backend.submit_tasks(descriptions)
            return {"success" : True,
                    "result"  : ret}
        except Exception as e:
            self._log.exception('oops')
            return {"success" : False,
                    'error'   : repr(e)}


    # --------------------------------------------------------------------------
    #
    @methodroute('/tasks/<task_ids>/state', method="GET")
    def get_task_states(self, task_ids):

        try:
            ret = self._backend.get_task_states(task_ids)
            return {"success" : True,
                    "result"  : ret}
        except Exception as e:
            self._log.exception('oops')
            return {"success" : False,
                    'error'   : repr(e)}


    # --------------------------------------------------------------------------
    #
    @methodroute('/tasks/<task_ids>/wait/<states>/<timeout>', method="GET")
    def wait_task_states(self, task_ids, states, timeout):

        try:
            ret = self._backend.wait_task_states(task_ids, states, timeout)
            return {"success" : True,
                    "result"  : ret}
        except Exception as e:
            self._log.exception('oops')
            return {"success" : False,
                    'error'   : repr(e)}


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    server = None
    try:
        server = PandaNGE_Server()
        routeapp(server)
        server.serve()
    finally:
        if server:
            server.close()


# ------------------------------------------------------------------------------



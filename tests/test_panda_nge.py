#!/usr/bin/env python

__copyright__ = "Copyright 2017, http://radical.rutgers.edu"
__license__   = "MIT"


import json
import time
import requests

url = 'http://localhost:8080'

def test_query(op, query, data=None):

    print 'test %s %s' % (op, query)

    if op == 'get':
        r = requests.get(url + query)
        try:
            print r.status_code
            print r.content
            result = json.loads(r.content)
            assert(result['success']), result
            assert(r.status_code == 200), r.status
        except ValueError as e:
            print 'no json: %s' % r.content

    elif op == 'put':
        r = requests.put(url + query, json=data)
        result = json.loads(r.content)
        assert(r.status_code == 200)
        assert(result['success'])


test_query('get', '/resources/')
test_query('get', '/resources/pilot.0000/info')
test_query('get', '/resources/pilot.0000/state')
# test_query('get', '/resources/pilot.0000/wait/ACTIVE/0')
test_query('put', '/tasks/', data=[{'executable': '/bin/date'}])
time.sleep(1)
test_query('get', '/tasks/')
test_query('get', '/tasks/unit.000000/state')
test_query('get', '/tasks/unit.000000/wait/DONE/0')


#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
from user import *

class UserManage:
    def __init__(self):
        resource1 = User(1)
        resource2 = User(2)
        resource3 = User(3)
        resource4 = User(4)
        resource5 = User(5)
        self.resources_feature = {}
        for pid in resource1.resources_feature:
            self.resources_feature[pid] = resource1.resources_feature[pid] + \
                    " |z " + resource2.resources_feature[pid] + \
                    " |y " + resource3.resources_feature[pid] + \
                    " |x " + resource4.resources_feature[pid] + \
                    " |w " + resource5.resources_feature[pid]


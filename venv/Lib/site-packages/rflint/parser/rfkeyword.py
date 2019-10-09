# Copyright 2019-     DNB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from .common import RobotStatements

class Keyword(RobotStatements):
    '''A robotframework keyword

    A keyword is identical to a testcase in almost all respects
    except for some of the metadata it supports (which this definition
    doesn't (yet) account for...).
    '''
    def __init__(self, parent, linenumber, name):
        RobotStatements.__init__(self)
        self.linenumber = linenumber
        self.name = name
        self.rows = []
        self.parent = parent

    def __repr__(self):
        # should this return the fully qualified name?
        return "<Keyword: %s>" % self.name


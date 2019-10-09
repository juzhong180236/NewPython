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

import warnings


class Deprecated(object):

    def __init__(self, old_name, new_name):
        self.old_name = old_name
        self.new_name = new_name

    def __get__(self, instance, owner):
        self._warn()
        return getattr(instance, self.new_name)

    def __set__(self, instance, value):
        self._warn()
        setattr(instance, self.new_name, value)

    def _warn(self):
        warnings.warn('"rbfWEB.%s" is deprecated, use '
                      '"rbfWEB.%s" instead.'
                      % (self.old_name, self.new_name),
                      DeprecationWarning)

# -*- coding: utf-8 -*-

#  Copyright 2019-  DNB
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

def keyword(types=()):
    """Decorator to set custom argument types to keywords.

    This decorator creates ``robot_types`` attribute on the decorated
    keyword method or function based on the provided arguments.
    Robot Framework checks them to determine the keyword's
    argument types.

    Types must be given as a dictionary mapping argument names to types or as a list
    (or tuple) of types mapped to arguments based on position. It is OK to
    specify types only to some arguments, and setting ``types`` to ``None``
    disables type conversion altogether.

    Examples::

        @keyword(types={'length': int, 'case_insensitive': bool})
        def types_as_dict(length, case_insensitive=False):
            # ...

        @keyword(types=[int, bool])
        def types_as_list(length, case_insensitive=False):
            # ...

        @keyword(types=None])
        def no_conversion(length, case_insensitive=False):
            # ...

        @keyword
        def func():
            # ...
    """

    def decorator(func):
        func.robot_types = types
        return func
    return decorator

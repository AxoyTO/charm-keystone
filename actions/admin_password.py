#!/usr/bin/env python3
#
# Copyright 2022 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

sys.path.append('.')
sys.path.append('./hooks')

from charmhelpers.core.hookenv import (
    function_set,
    function_fail,
    leader_get,
)

from keystone_utils import rotate_admin_passwd


def get_admin_password(arg):
    """Implementation of 'get-admin-password' action."""
    function_set({'admin-password': leader_get("admin_passwd")})


def rotate_admin_password(args):
    """Rotate the admin user's password.

    @raises Exception if keystone client cannot update the password
    """
    rotate_admin_passwd()


ACTIONS = {
    "get-admin-password": get_admin_password,
    "rotate-admin-password": rotate_admin_password,
}


def main(args):
    action_name = os.path.basename(args[0])
    try:
        action = ACTIONS[action_name]
    except KeyError:
        return "Action {} undefined".format(action_name)
    else:
        try:
            action(args)
        except Exception as e:
            function_fail("Action {} failed: {}".format(action_name, str(e)))


if __name__ == "__main__":
    sys.exit(main(sys.argv))

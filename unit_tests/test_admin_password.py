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

from unittest import mock
from test_utils import CharmTestCase

from actions import admin_password


TO_PATCH = [
    'leader_get',
    'function_set',
]


class GetAdminPasswordTestCase(CharmTestCase):
    def setUp(self):
        super(GetAdminPasswordTestCase, self).setUp(
            admin_password, TO_PATCH)

    def test_get_admin_password(self):
        admin_password.get_admin_password([])
        self.function_set.assert_called_with({'admin-password':
                                             self.leader_get("admin_passwd")})


class RotateAdminPasswordTestCase(CharmTestCase):

    def setUp(self):
        super(RotateAdminPasswordTestCase, self).setUp(
            admin_password, ["rotate_admin_passwd"])

    def test_rotate_admin_password(self):
        admin_password.rotate_admin_password([])
        self.rotate_admin_passwd.assert_called_once()


class MainTestCase(CharmTestCase):

    def setUp(self):
        super(MainTestCase, self).setUp(admin_password, ["function_fail"])

    def test_invokes_action(self):
        dummy_calls = []

        def dummy_action(arg):
            dummy_calls.append(True)

        with mock.patch.dict(admin_password.ACTIONS, {"foo": dummy_action}):
            admin_password.main(["foo"])
        self.assertEqual(dummy_calls, [True])

    def test_unknown_action(self):
        """Unknown actions aren't a traceback."""
        exit_string = admin_password.main(["foo"])
        self.assertEqual("Action foo undefined", exit_string)

    def assert_function_fail_msg(self, action_name, msg):
        """Shortcut for asserting error with default structure"""
        admin_password.function_fail.assert_called_with("Action {} "
                                                        "failed: {}"
                                                        .format(action_name,
                                                                msg))

    def test_failing_action(self):
        """Actions which traceback trigger function_fail() calls."""
        def dummy_action(arg):
            raise ValueError("uh oh")

        with mock.patch.dict(admin_password.ACTIONS, {"foo": dummy_action}):
            admin_password.main(["foo"])
        self.assert_function_fail_msg("foo", "uh oh")

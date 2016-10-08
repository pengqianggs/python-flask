#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: test user permission

import unittest
from application.models import Role, User, AnonymousUser, Permission

class UserModelTestCase(unittest.TestCase):
    def test_role_and_permission(self):
        Role.insert_roles()
        user = User(email='pengqiang@126.com', name='pengqiang')
        user.set_password('cat')
        self.assertTrue(user.can(Permission.PERMISSION_ARTICLE))
        self.assertFalse(user.can(Permission.PERMISSION_ADMIN))

    def test_anonymous_user(self):
        user = AnonymousUser()
        self.assertFalse(user.can(Permission.PERMISSION_FOLLOW))

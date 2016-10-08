#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: unit test user model password

import unittest
from application.models import User

class UserPasswordTestCase(unittest.TestCase):
    # test set password
    def test_set_password(self):
        user = User(email='pengqiang@126.com', name='pengqiang')
        user.set_password('password')
        self.assertTrue(user.password is not None)

    # test check password
    def test_check_password(self):
        user = User(email='pengqiang@126.com', name='pengqiang')
        user.set_password('password')
        self.assertTrue(user.check_password('password'))
        self.assertFalse(user.check_password('pessword'))

    # test same password, different password hash
    def test_diff_user_password(self):
        user1 = User(email='pengqiang@126.com', name='pengqiang')
        user2 = User(email='pengqiang@163.com', name='pengqiang')
        user1.set_password('password')
        user2.set_password('password')
        self.assertTrue(user1.password != user2.password)


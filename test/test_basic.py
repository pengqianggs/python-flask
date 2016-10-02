#! /usr/bin/python
# _*_ coding: utf-8 _*_
# Desc: basic unit test

import unittest
from application import create_application, database
from flask import current_app

class BasicTestCase(unittest.TestCase):
    # set up test environment
    def setUp(self):
        self.application = create_application('testing')
        self.app_context = self.application.app_context()
        self.app_context.push()
        database.create_all()

    # remove test environment
    def tearDown(self):
        database.session.remove()
        database.drop_all()
        self.app_context.pop()

    # judge test application does exist or not
    def test_app_exist(self):
        self.assertFalse(current_app is None)

    # judge test application is testing or not
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

from unittest import TestCase
import sqlite3
import server_checker


class TestPassword_check(TestCase):

    def setUp(self):
        self.db = sqlite3.connect('userinfo.db')

    def test_password_check(self):
        self.assertTrue(server_checker.password_check('admin', '123456', self.db))

    def tearDown(self):
        self.db.close()

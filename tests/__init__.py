# -*- coding: utf-8 -*-
import unittest
import os
import time


class PythonFacebookTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['TZ'] = 'Europe/Paris'
        time.tzset()

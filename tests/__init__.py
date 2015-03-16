# -*- coding: utf-8 -*-
from tests.facebook_test_helper import FacebookTestHelper
#
#
# def setUpModule():
#     FacebookTestHelper.initialize()
#
#
# def tearDownModule():
#     FacebookTestHelper.delete_test_user()


def teardown_module(module):
    print "TEARDOWN DUH2"
    FacebookTestHelper.delete_test_user()

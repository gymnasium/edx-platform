"""
Tests to ensure proper permission are set on the Appsembler API views.
"""
from django.test import TestCase
from inspect import isclass

import ddt

from appsembler_api import views as api_views


def get_api_classes():
    api_classes = []

    for member_name in dir(api_views):
        member = getattr(api_views, member_name)
        if isclass(member):
            # Exclude imported classes
            if member.__module__ == api_views.__name__:
                api_classes.append(member)

    return api_classes


@ddt.ddt
class AppsemblerAPIPermissionsTests(TestCase):

    def test_api_classes_are_being_found(self):
        self.assertTrue(get_api_classes())  # Ensure the API classes are getting filtered correctly

    @ddt.data(*get_api_classes())
    def test_auth_classes_are_tuples(self, api_class):
        """
        The commas that makes the tuple tend to be tricky! This ensures it's being set right.

        This will NOT ensure that the classes being set are secure or
        correct, we still rely on manual review for that matter.
        """
        self.assertIsInstance(api_class.authentication_classes, (tuple, list))
        self.assertIsInstance(api_class.permission_classes, (tuple, list))

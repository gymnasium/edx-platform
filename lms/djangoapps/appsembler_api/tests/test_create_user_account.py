"""
Tests for the CreateUserAccountView.
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from rest_framework.permissions import AllowAny

import ddt
from mock import patch


@ddt.ddt
@patch('appsembler_api.views.CreateUserAccountView.authentication_classes', [])
@patch('appsembler_api.views.CreateUserAccountView.permission_classes', [AllowAny])
@override_settings(APPSEMBLER_FEATURES={
    'SKIP_LOGIN_AFTER_REGISTRATION': False,
})
class CreateUserAccountViewTests(TestCase):
    def setUp(self):
        self.url = reverse('create_user_account_api')
        self.sample_user_data = {
            'username': 'MrRobot',
            'password': 'edX',
            'email': 'mr.robot@example.com',
            'name': 'Mr Robot'
        }

    def test_happy_path(self):
        res = self.client.post(self.url, self.sample_user_data)
        self.assertContains(res, 'user_id', status_code=200)

    def test_duplicate_identifiers(self):
        self.client.post(self.url, self.sample_user_data)

        res = self.client.post(self.url, {
            'username': self.sample_user_data['username'],
            'password': 'Another Password!',
            'email': 'me@example.com',
            'name': 'The Boss'
        })
        self.assertContains(res, 'User already exists', status_code=409)

        res = self.client.post(self.url, {
            'username': 'world_changer',
            'password': 'Yet Another Password!',
            'email': self.sample_user_data['email'],
            'name': 'World Changer'
        })
        self.assertContains(res, 'User already exists', status_code=409)

    @ddt.data('username', 'name')
    def test_missing_field(self, field):
        params = self.sample_user_data.copy()
        del params[field]
        res = self.client.post(self.url, params)
        self.assertContains(res, 'Wrong parameters on user creation', status_code=400)

    @ddt.data('username', 'email')
    def test_incorrect_field_format(self, field):
        params = self.sample_user_data.copy()
        params[field] = '%%%%%%%'
        res = self.client.post(self.url, params)
        self.assertContains(res, 'Wrong parameters on user creation', status_code=400)

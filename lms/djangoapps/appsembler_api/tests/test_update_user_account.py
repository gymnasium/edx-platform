"""
Tests for the CreateUserAccountView.
"""
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework.permissions import AllowAny
from student.tests.factories import UserFactory
from django.contrib.auth.models import User
import attr

from itertools import combinations

import ddt
from mock import patch


@attr.s
class Field(object):
    """
    A class to represent a update-able field.

    Note this class uses <http://www.attrs.org/> to manage its boilerplate.
    """
    name = attr.ib()
    valid = attr.ib(default=None)
    invalid = attr.ib(default=None)


@ddt.ddt
@patch('appsembler_api.views.UpdateUserAccount.authentication_classes', [])
@patch('appsembler_api.views.UpdateUserAccount.permission_classes', [AllowAny])
class CreateUserAccountViewTests(TestCase):
    # TODO: The API does not support validation for profile fields!
    # TODO: Use `update_account_settings` to ensure little validation is done!
    PROFILE_FIELDS = [
        Field(name='name', valid='John Doe'),
        Field(name='country', valid='JO'),
        Field(name='gender', valid='m'),
        Field(name='level_of_education', valid='p'),
        Field(name='year_of_birth', valid=1985),
        Field(name='city', valid='Foo'),
        Field(name='mailing_address', valid='MA, ELM Street'),
        Field(name='language', valid='ES'),
        Field(name='goals', valid='Learning for life'),
        Field(name='bio', valid='I am from Mars'),
    ]

    def setUp(self):
        self.url = reverse('user_account_update_user')
        self.user = UserFactory.create(
            email='edx@example.com',
            username='rubber_duck',
            profile__name='Rubber Duck',
        )

    def test_happy_scenario(self):
        new_name = 'Ms Rubber Duck'
        res = self.client.post(self.url, {
            'user_lookup': self.user.email,
            'name': new_name,
        })

        self.assertIn('success', res.content)
        self.assertContains(res, 'name=')
        self.assertNotContains(res, 'email=')

        updated_user = User.objects.get(email=self.user.email)
        self.assertEqual(updated_user.profile.name, new_name)  # The name should be updated

    def test_with_invalid_email(self):
        new_value = 'zzz%%'
        res = self.client.post(self.url, {
            'user_lookup': self.user.email,
            'email': new_value,
        })

        updated_user = User.objects.get(pk=self.user.pk)
        self.assertNotEqual(updated_user.email, new_value)  # The field should NOT be updated

        self.assertNotIn('success', res.content)
        self.assertNotContains(res, 'email=', status_code=400)

    def test_found_two_users(self):
        UserFactory.create(
            email='sneaky@example.com',
            username=self.user.email,
        )

        res = self.client.post(self.url, {
            'user_lookup': self.user.email,
            'name': 'Innocent Requester',
        })

        self.assertIn('Two users have been found with the provided user_lookup', res.content)
        self.assertEqual(res.status_code, 400)

    def test_two_fields(self):
        res = self.client.post(self.url, {
            'user_lookup': self.user.email,
            'email': 'new.mail@example.com',
            'name': 'New Name!',
        })

        self.assertIn('success', res.content)
        self.assertContains(res, 'email=')
        self.assertContains(res, 'name=')

    def test_user_not_found(self):
        res = self.client.post(self.url, {
            'user_lookup': 'dr_who',
            'name': 'Ms Rubber Duck',
        })

        self.assertContains(res, 'user_not_found', status_code=404)

    def test_missing_lookup_field(self):
        res = self.client.post(self.url, {
            'name': 'Jerry',
        })

        self.assertContains(res, 'lookup_error', status_code=400)

    def test_duplicate_email(self):
        instructor_email = 'instructor@example.com'
        UserFactory.create(
            email=instructor_email,
        )

        res = self.client.post(self.url, {
            'user_lookup': instructor_email,
            'email': self.user.email,
        })

        self.assertIn(r'An account with this e-mail already exists.', res.content)
        self.assertEqual(res.status_code, 400)

    @ddt.data(*PROFILE_FIELDS)
    def test_profile_fields_update(self, field):
        new_value = field.valid
        res = self.client.post(self.url, {
            'user_lookup': self.user.email,
            field.name: new_value,
        })

        self.assertIn('success', res.content)
        self.assertContains(res, '{field_name}='.format(field_name=field.name))

        updated_user = User.objects.get(email=self.user.email)
        new_value_from_db = getattr(updated_user.profile, field.name)
        self.assertEqual(new_value_from_db, new_value)  # The field should be updated

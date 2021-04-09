from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Profile


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        new_user = get_user_model().objects.create_user(
                                                username='testuser01',
                                                email='testemail01@gmail.com',
                                                password='testpassword01235',
        )

    def test_user_field_type(self):
        profile = Profile.objects.get(id=1)
        field_type = profile._meta.get_field('user').get_internal_type()
        self.assertEquals(field_type,'OneToOneField')

    def test_email_confirmed_field_type(self):
        profile = Profile.objects.get(id=1)
        field_type = profile._meta.get_field(
                                        'email_confirmed').get_internal_type()
        self.assertEquals(field_type,'BooleanField')

    def test_profile_instance_of_profile_class(self):
        profile = Profile.objects.get(id=1)
        self.assertTrue(isinstance(profile, Profile))


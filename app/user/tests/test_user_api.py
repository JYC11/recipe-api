from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """test the publically available user api"""
    def setUp(self):
        self.client = APIClient()
    
    def test_create_valid_user_success(self):
        """test when creating user with valid payload is successful"""
        payload = {
            'email':'test@email.com',
            'password':'testpass123',
            'name':'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)
    
    def test_user_exists(self):
        """test creating a user that already exists"""
        payload = {
            'email':'test@email.com',
            'password':'testpass123',
            'name':'Test name'
        }
        create_user(**payload) #create user

        res = self.client.post(CREATE_USER_URL,payload) #create user again

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short(self):
        """test to see if password is too short"""
        payload = {
            'email':'test@email.com',
            'password':'test',
            'name':'Test name'
        }
        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
        self.assertEqual(res.data['password'][0].code,'min_length')
    
    def test_create_token_for_user(self):
        """test that token is created for user"""
        payload = {
            'email':'test@email.com',
            'password':'testpass123',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL,payload)

        self.assertIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_invalid_credentials(self):
        """test that token is not created if invalid credentials are given"""
        create_user(email="test@email.com",password="testpass123")
        payload = {
            'email':'test@email.com',
            'password':'test',
        }
        res = self.client.post(TOKEN_URL,payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_no_user(self):
        """test that token is not created if user doesn't exist"""
        payload = {
            'email':'test@email.com',
            'password':'testpass123',
        }
        res = self.client.post(TOKEN_URL,payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_missing_field(self):
        """test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email':'one','password':''})
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_retrieve_user_unauthorized(self):
        """test that authentication is required for users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
    """test api requests that require authentication"""
    def setUp(self):
        self.user = create_user(
            email="test@email.com",
            password="testpass123",
            name="Jim Bob"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_profile_success(self):
        """test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name':self.user.name,
            'email':self.user.email
        })
    
    def test_post_me_not_allowed(self):
        """test that post is not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_update_user_profile(self):
        """test updating the user profile for authenticated user"""
        payload = {
            'name':'Bob Jim',
            'password':'newtestpass123',
        }

        res = self.client.patch(ME_URL,payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
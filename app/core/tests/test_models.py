from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from core import models
from unittest.mock import patch

def make_sample_user(email="test@email.com",password="testpass123"):
    """create a sample user"""
    return get_user_model().objects.create_user(email,password)

class Modeltests(TestCase):
    
    def test_create_user_with_email_success(self):
        """test creating user with an email"""
        email = "test@email.com"
        password = "testpass123"
        user = make_sample_user(email,password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_user_email_normalization(self):
        """test that email is normalized upon user creation"""
        email = "test@EMAIL.COM"
        user = make_sample_user(email,"testpass123")

        self.assertEqual(user.email,email.lower())
    
    def test_new_user_invalid_email(self):
        """test creating user with no email results in error"""
        with self.assertRaises(ValueError):
            make_sample_user(None,"testpass123")
    
    def test_unique_email_signup(self):
        user1 = make_sample_user()
        with self.assertRaises(IntegrityError):
            user2 = make_sample_user()
    
    def test_create_new_superuser(self):
        superuser = get_user_model().objects.create_superuser(
            'test@email.com',
            'testpass123'
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
    
    def test_tag_str(self):
        """test the tag string representation"""
        tag = models.Tag.objects.create(
            user=make_sample_user(),
            name="Brunch"
        )

        self.assertEqual(str(tag),tag.name)
    
    def test_ingredient_str(self):
        """test ingredient string representation"""
        tag = models.Ingredient.objects.create(
            user=make_sample_user(),
            name="Egg"
        )
        self.assertEqual(str(tag),tag.name)
    
    def test_recipe_str(self):
        """test recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=make_sample_user(),
            title='Chicken Calzone',
            time_minutes=60,
            price=10.00
        )

        self.assertEqual(str(recipe),recipe.title)
    
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self,mock_uuid):
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None,'myimage.jpg')
        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path,exp_path)
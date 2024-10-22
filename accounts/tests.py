from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from expenses.models import User

class AuthAPITestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.refresh_url = reverse('token_refresh')
        self.user_data = {
            "username": "user1",
            "email": "user1@example.com",
            "password": "user1password",
            "password2": "user1password",
            "mobile": "1234",
            "name": "user1"
        }

    def test_register(self):
        response = self.client.post(self.register_url, self.user_data)
        print("Response data on register:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('message'), 'User registered successfully')
      
    def test_login(self):
        response = self.client.post(self.register_url, self.user_data)
        print("Response data on register:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('message'), 'User registered successfully')

        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data)
        
        print("Response data on login:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
        self.assertIn('access', response.data)  
        self.assertIn('refresh', response.data) 

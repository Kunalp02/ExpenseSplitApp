from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Split, Expense
import json
from expenses.models import User

class ExpenseTestCase(APITestCase):
    def test_add_expense_equal_split(self):
        self.user1 = User.objects.create_user(email='user1@gmail.com', password='password123',  mobile="1234",
            name = "user1")
        self.user2 = User.objects.create_user(email='user2@gmail.com', password='password123', mobile="123456",
            name = "user2")
        self.token_user1 = RefreshToken.for_user(self.user1)

        expense_data = {    
            'title': 'Lunch',
            'total_amount': 400,
            'split_method': 'EQUAL',
            'participants': [1, 2]
        }

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token_user1.access_token}')

        response = self.client.post(reverse('add_expense'), expense_data, format='json')

        print(f"Status Code: {response.status_code}")
        try:
            response_data = response.json()  
            print("Response JSON:")
            print(json.dumps(response_data, indent=4))  
        except ValueError:
            print("Response Text:")
            print(response.content.decode('utf-8'))  

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Split.objects.count(), 2)

        splits = Split.objects.all()
        for split in splits:
            self.assertEqual(split.amount_owed, 200)

        expense = Expense.objects.get(title='Lunch')
        for split in splits:
            self.assertEqual(split.expense, expense)
            self.assertIn(split.user, [self.user1, self.user2])

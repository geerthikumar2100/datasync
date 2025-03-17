from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import User, Account, AccountMember, Destination, Role
from rest_framework.authtoken.models import Token
import uuid

class AuthenticationTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.test_user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.signup_url = reverse('signup')

    def test_user_signup_success(self):
        """Test successful user signup"""
        data = {
            'email': 'newuser@example.com',
            'password': 'newpass123'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_user_signup_duplicate_email(self):
        """Test signup with existing email"""
        data = {
            'email': 'test@example.com',  # Already exists from setUp
            'password': 'anotherpass123'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        """Test successful login"""
        data = {
            'username': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {
            'username': 'test@example.com',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_logout(self):
        """Test user logout"""
        # First create a token
        token = Token.objects.create(user=self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.test_user).exists())

class AccountTests(APITestCase):
    def setUp(self):
        # Create a superuser instead of regular user to have all permissions
        self.user = User.objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Create an account and make the user a member with admin role
        self.account = Account.objects.create(
            id=uuid.uuid4(),
            account_name='Test Account',
            created_by=self.user,
            updated_by=self.user
        )
        # Create admin role if it doesn't exist
        self.admin_role, _ = Role.objects.get_or_create(role_name=Role.ADMIN)
        # Add user as account member with admin role
        AccountMember.objects.create(
            account=self.account,
            user=self.user,
            role=self.admin_role,
            created_by=self.user,
            updated_by=self.user
        )

    def test_create_account(self):
        """Test account creation"""
        data = {
            'account_name': 'New Account',
            'created_by': self.user.id,
            'updated_by': self.user.id
        }
        response = self.client.post(reverse('account-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 2)

    def test_get_account_list(self):
        """Test getting list of accounts"""
        response = self.client.get(reverse('account-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class DestinationTests(APITestCase):
    def setUp(self):
        # Create a superuser instead of regular user
        self.user = User.objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        self.account = Account.objects.create(
            id=uuid.uuid4(),
            account_name='Test Account',
            created_by=self.user,
            updated_by=self.user
        )
        # Create admin role if it doesn't exist
        self.admin_role, _ = Role.objects.get_or_create(role_name=Role.ADMIN)
        # Add user as account member with admin role
        AccountMember.objects.create(
            account=self.account,
            user=self.user,
            role=self.admin_role,
            created_by=self.user,
            updated_by=self.user
        )

    def test_create_destination(self):
        """Test destination creation"""
        data = {
            'account': self.account.id,
            'url': 'https://test.com/webhook',
            'http_method': 'POST',
            'created_by': self.user.id,
            'updated_by': self.user.id
        }
        response = self.client.post(reverse('destination-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Destination.objects.count(), 1)

    def test_invalid_destination_url(self):
        """Test creating destination with invalid URL"""
        data = {
            'account': self.account.id,
            'url': 'invalid-url',
            'http_method': 'POST',
            'created_by': self.user.id,
            'updated_by': self.user.id
        }
        response = self.client.post(reverse('destination-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class EdgeCaseTests(APITestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        self.logout_url = reverse('logout')

    def test_login_empty_credentials(self):
        """Test login with empty credentials"""
        response = self.client.post(self.login_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_invalid_email(self):
        """Test signup with invalid email format"""
        data = {
            'email': 'invalid-email',
            'password': 'pass123'
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_without_token(self):
        """Test logout without authentication"""
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

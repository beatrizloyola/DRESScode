from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Piece, Outfit


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@test.com',
            password='pass123',
        )

    def _piece(self, name=None, category='shirt'):
        return Piece(user=self.user, name=name, category=category)

    def _outfit(self, tags=''):
        return Outfit(user=self.user, name='Look', tags=tags)

    # --- Piece.__str__ ---

    def test_piece_str_with_name(self):
        self.assertEqual(str(self._piece(name='Camiseta Branca')), 'Camiseta Branca')

    def test_piece_str_without_name_contains_category(self):
        self.assertIn('pants', str(self._piece(name=None, category='pants')))

    def test_piece_str_without_name_contains_username(self):
        self.assertIn(self.user.username, str(self._piece(name=None)))

    # --- Outfit.get_tags_list ---

    def test_get_tags_list_normal(self):
        self.assertEqual(self._outfit(tags='casual, festa').get_tags_list(), ['casual', 'festa'])

    def test_get_tags_list_empty_string(self):
        self.assertEqual(self._outfit(tags='').get_tags_list(), [])

    def test_get_tags_list_none(self):
        self.assertEqual(self._outfit(tags=None).get_tags_list(), [])

    def test_get_tags_list_strips_whitespace(self):
        self.assertEqual(self._outfit(tags=' casual , festa ').get_tags_list(), ['casual', 'festa'])

    def test_get_tags_list_single_tag(self):
        self.assertEqual(self._outfit(tags='trabalho').get_tags_list(), ['trabalho'])


class TestAuthViews(TestCase):
    def setUp(self):
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    # --- Signup ---

    def test_signup_success(self):
        response = self.client.post(self.signup_url, {
            'name': 'Maria',
            'email': 'maria@test.com',
            'password': 'senha123',
            'confirm_password': 'senha123',
        })
        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(username='maria@test.com').exists())

    def test_signup_password_mismatch(self):
        response = self.client.post(self.signup_url, {
            'name': 'Maria',
            'email': 'maria@test.com',
            'password': 'senha123',
            'confirm_password': 'diferente',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='maria@test.com').exists())
        messages = list(response.context['messages'])
        self.assertTrue(any('senhas' in str(m).lower() for m in messages))

    def test_signup_duplicate_email(self):
        User.objects.create_user(username='dup@test.com', password='pass123')
        response = self.client.post(self.signup_url, {
            'name': 'Outro',
            'email': 'dup@test.com',
            'password': 'pass123',
            'confirm_password': 'pass123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username='dup@test.com').count(), 1)
        messages = list(response.context['messages'])
        self.assertTrue(any('cadastrado' in str(m).lower() for m in messages))

    # --- Login ---

    def test_login_success(self):
        User.objects.create_user(username='user@test.com', password='pass123')
        response = self.client.post(self.login_url, {
            'email': 'user@test.com',
            'password': 'pass123',
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_wrong_credentials(self):
        response = self.client.post(self.login_url, {
            'email': 'naoexiste@test.com',
            'password': 'errado',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        messages = list(response.context['messages'])
        self.assertTrue(any('incorretos' in str(m).lower() for m in messages))

    # --- Logout ---

    def test_logout_redirects_to_landing(self):
        User.objects.create_user(username='user@test.com', password='pass123')
        self.client.login(username='user@test.com', password='pass123')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, reverse('landing'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

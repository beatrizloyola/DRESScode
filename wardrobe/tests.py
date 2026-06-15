from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
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


def _fake_image():
    return SimpleUploadedFile('shirt.png', b'\x89PNG\r\n', content_type='image/png')


class TestPieceViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._patcher_save = patch(
            'cloudinary_storage.storage.MediaCloudinaryStorage._save',
            return_value='pieces/fake.png',
        )
        cls._patcher_url = patch(
            'cloudinary_storage.storage.MediaCloudinaryStorage.url',
            return_value='https://res.cloudinary.com/fake/image/upload/pieces/fake.png',
        )
        cls._patcher_save.start()
        cls._patcher_url.start()

    @classmethod
    def tearDownClass(cls):
        cls._patcher_save.stop()
        cls._patcher_url.stop()
        super().tearDownClass()

    def setUp(self):
        self.user1 = User.objects.create_user(username='u1@test.com', password='pass123')
        self.user2 = User.objects.create_user(username='u2@test.com', password='pass123')
        self.client.force_login(self.user1)
        self.piece = Piece.objects.create(
            user=self.user1, name='Camiseta', category='shirt', image='pieces/fake.png'
        )

    # --- add_piece ---

    def test_add_piece_success(self):
        response = self.client.post(reverse('add_piece'), {
            'name': 'Nova Camisa',
            'category': 'shirt',
            'image': _fake_image(),
        })
        self.assertRedirects(response, reverse('my_pieces'))
        self.assertTrue(Piece.objects.filter(name='Nova Camisa', user=self.user1).exists())

    def test_add_piece_missing_category(self):
        count_before = Piece.objects.count()
        response = self.client.post(reverse('add_piece'), {
            'name': 'Sem Categoria',
            'image': _fake_image(),
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Piece.objects.count(), count_before)
        messages = list(response.context['messages'])
        self.assertTrue(any('imagem' in str(m).lower() or 'categoria' in str(m).lower() for m in messages))

    def test_add_piece_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('add_piece'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('add_piece')}")

    # --- my_pieces ---

    def test_my_pieces_only_own(self):
        Piece.objects.create(user=self.user2, name='Calça Alheia', category='pants', image='pieces/fake.png')
        response = self.client.get(reverse('my_pieces'))
        self.assertEqual(response.status_code, 200)
        all_pieces = list(response.context['shirts']) + list(response.context['pants']) + list(response.context['shoes'])
        self.assertTrue(all(p.user == self.user1 for p in all_pieces))

    def test_my_pieces_search_by_name(self):
        Piece.objects.create(user=self.user1, name='Calça Jeans', category='pants', image='pieces/fake.png')
        Piece.objects.create(user=self.user1, name='Tênis Branco', category='shoes', image='pieces/fake.png')
        response = self.client.get(reverse('my_pieces'), {'q': 'calça'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_results'], 1)

    # --- edit_piece ---

    def test_edit_piece_owner(self):
        response = self.client.post(reverse('edit_piece', args=[self.piece.id]), {
            'name': 'Camiseta Editada',
            'category': 'pants',
        })
        self.assertRedirects(response, reverse('my_pieces'))
        self.piece.refresh_from_db()
        self.assertEqual(self.piece.name, 'Camiseta Editada')
        self.assertEqual(self.piece.category, 'pants')

    def test_edit_piece_other_user(self):
        self.client.force_login(self.user2)
        response = self.client.post(reverse('edit_piece', args=[self.piece.id]), {
            'name': 'Hack',
            'category': 'shirt',
        })
        self.assertEqual(response.status_code, 404)
        self.piece.refresh_from_db()
        self.assertEqual(self.piece.name, 'Camiseta')

    # --- delete_piece ---

    def test_delete_piece_owner(self):
        response = self.client.post(reverse('delete_piece', args=[self.piece.id]))
        self.assertRedirects(response, reverse('my_pieces'))
        self.assertFalse(Piece.objects.filter(id=self.piece.id).exists())

    def test_delete_piece_other_user(self):
        self.client.force_login(self.user2)
        response = self.client.post(reverse('delete_piece', args=[self.piece.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Piece.objects.filter(id=self.piece.id).exists())

    def test_delete_piece_get_noop(self):
        self.client.get(reverse('delete_piece', args=[self.piece.id]))
        self.assertTrue(Piece.objects.filter(id=self.piece.id).exists())

from django.test import TestCase
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

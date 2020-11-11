from django.test import TestCase
from core.models import Favorite
from authentication.models import CustomUser
from core.models import Suggestion
from rest_framework.test import APIRequestFactory
from core.views.favorite import FavoriteViewSet
from core.views.game import GameViewSet
from core.views.suggestion import SuggestionViewSet


# Create your tests here.
class FavoriteAPI(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(username='test',
                                              email='test@test.com', password='12345678')
        Favorite.objects.create(user=user,
                                slug='the-witcher-3-wild-hunt')

    def test_add_new(self):
        valid_paylod = {
            'username': 'test',
            'slug': 'the-legend-of-zelda-breath-of-the-wild'
        }
        factory = APIRequestFactory()
        request_url = '/favorites/add_favorite'
        view = FavoriteViewSet.as_view({'post': 'add_favorite'})
        request = factory.post(request_url, valid_paylod, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_add_duplicate(self):
        valid_paylod = {
            'username': 'test',
            'slug': 'the-witcher-3-wild-hunt'
        }
        factory = APIRequestFactory()
        request_url = '/favorites/add_favorite'
        view = FavoriteViewSet.as_view({'post': 'add_favorite'})
        request = factory.post(request_url, valid_paylod, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_get_favorites(self):
        valid_paylod = {
            'username': 'test',
        }
        # Extracted from Discovery
        witcher_response = [{'name': 'The Witcher 3: Wild Hunt',
                             'summary': 'The Witcher: Wild Hunt is a story-driven, next-generation open world '
                                        'role-playing game set in a visually stunning fantasy universe full of '
                                        'meaningful choices and impactful consequences. In The Witcher you play as '
                                        'the professional monster hunter, Geralt of Rivia, tasked with finding a child'
                                        ' of prophecy in a vast open world rich with merchant cities, viking pirate '
                                        'islands, dangerous mountain passes, and forgotten caverns to explore.',
                             'cover': {'alpha_channel': False,
                                       'url': '//images.igdb.com/igdb/image/upload/t_thumb/co1wyy.jpg', 'image_id':
                                           'co1wyy', 'animated': False, 'height': 1559, 'id': 89386, 'checksum':
                                           '603ae7ce-f061-4f14-7f9c-7b8708fb3268', 'game': 1942, 'width': 1170},
                             'slug': 'the-witcher-3-wild-hunt'}]

        factory = APIRequestFactory()
        request_url = '/favorites/get_favorite'
        view = FavoriteViewSet.as_view({'post': 'get_favorites'})
        request = factory.post(request_url, valid_paylod, format='json')
        response = view(request)
        self.assertEqual(response.data, witcher_response)
        self.assertEqual(response.status_code, 200)

    def test_remove_favorite(self):
        valid_paylod = {
            'username': 'test',
            'slug': 'the-witcher-3-wild-hunt'
        }
        factory = APIRequestFactory()
        request_url = '/favorites/remove_favorite'
        view = FavoriteViewSet.as_view({'post': 'remove_favorite'})
        request = factory.post(request_url, valid_paylod, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_remove_favorite_fail(self):
        valid_paylod = {
            'username': 'test',
            'slug': 'invalid'
        }
        factory = APIRequestFactory()
        request_url = '/favorites/remove_favorite'
        view = FavoriteViewSet.as_view({'post': 'remove_favorite'})
        request = factory.post(request_url, valid_paylod, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_is_favorite_success(self):
        valid_paylod = {
            'username': 'test',
            'slug': 'the-witcher-3-wild-hunt'
        }
        factory = APIRequestFactory()
        request_url = '/favorites/is_favorite'
        view = FavoriteViewSet.as_view({'post': 'is_favorite'})
        request = factory.post(request_url, valid_paylod, format='json')
        response = view(request)
        self.assertTrue(response.data['is_favorite'])

    def test_is_not_favorite(self):
        valid_paylod = {
            'username': 'test',
            'slug': 'invalid'
        }
        factory = APIRequestFactory()
        request_url = '/favorites/is_favorite'
        view = FavoriteViewSet.as_view({'post': 'is_favorite'})
        request = factory.post(request_url, valid_paylod, format='json')
        response = view(request)
        self.assertFalse(response.data['is_favorite'])


class GameAPI(TestCase):
    def test_retrieve(self):
        slug = 'the-witcher-3-wild-hunt'
        g = GameViewSet()
        response = g.retrieve(request=None, slug=slug)
        self.assertEqual(response.data['slug'], slug)

    def test_reccommendations(self):
        valid_paylod = {
            'tags': ['horses', 'archery']
        }
        factory = APIRequestFactory()
        request_url = '/games/recommendations'
        view = GameViewSet.as_view({'post': 'recommendations'})
        request = factory.post(request_url, valid_paylod, format='json')
        response = view(request)

        # Expected responses found via Discovery
        self.assertEqual(response.data[0]['slug'], 'totally-accurate-battle-simulator')
        self.assertEqual(response.data[len(response.data) - 1]['slug'], 'dragon-age-inquisition')


# TODO: Fix expected suggestion
class SuggestionAPI(TestCase):
    def setUP(self):
        Suggestion.objects.create(name='horses')

    def test_search(self):
        valid_paylod = {
            'search': 'ho'
        }
        factory = APIRequestFactory()
        request_url = '/suggestions/search'
        view = SuggestionViewSet.as_view({'post': 'search'})
        request = factory.post(request_url, valid_paylod, format='json')
        response = view(request)

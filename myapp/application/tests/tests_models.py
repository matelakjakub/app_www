from django.test import TestCase
from rest_framework.test import APITestCase

from ..models import Person, Team, Osoba
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User


class PersonModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Person.objects.create(name='Jan', shirt_size='L')

    def test_first_name_label(self):
        person = Person.objects.get(id=1)
        field_label = person._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_first_name_max_length(self):
        person = Person.objects.get(id=1)
        max_length = person._meta.get_field('name').max_length
        self.assertEqual(max_length, 60)




class TeamModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Team.objects.create(name='Test Team', city='TC')

    def test_team_name_label(self):
        team = Team.objects.get(id=1)
        field_label = team._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_team_name_max_length(self):
        team = Team.objects.get(id=1)
        max_length = team._meta.get_field('name').max_length
        self.assertEqual(max_length, 60)

    def test_team_city_label(self):
        team = Team.objects.get(id=1)
        field_label = team._meta.get_field('city').verbose_name
        self.assertEqual(field_label, 'city')

    def test_team_city_max_length(self):
        team = Team.objects.get(id=1)
        max_length = team._meta.get_field('city').max_length
        self.assertEqual(max_length, 2)


class OsobaListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        User.objects.create_user(username='kuba', password='admin')

    def setUp(self):

        self.client = APIClient()
        self.client.login(username='kuba', password='admin')

    def test_osoba_list_status_code(self):
        # Sprawdź, czy status protokołu HTML dla żądania GET na widoku osoba_list to 200 OK
        response = self.client.get('/osoba_list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class OsobaAPITestCase(APITestCase):
    def setUp(self):
        # Utwórz użytkownika do testów
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_create_osoba_with_token_authentication(self):
        # Utwórz obiekt Osoba przy użyciu uwierzytelnienia Token
        data = {
            'imie': 'John',
            'nazwisko': 'Doe',
            'plec': 1,
            'stanowisko': 1,
            'wlasciciel': self.user.id
        }
        response = self.client.post('/osoba_list/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Osoba.objects.count(), 1)
        self.assertEqual(Osoba.objects.get().imie, 'John')

    def test_create_osoba_with_basic_authentication(self):
        # Utwórz obiekt Osoba przy użyciu uwierzytelnienia Basic
        self.client.logout()  # Wyloguj się, aby zmienić metodę uwierzytelniania
        self.client.login(username='testuser', password='testpassword', HTTP_AUTHORIZATION='Basic base64encodedstring')

        data = {
            'imie': 'Jane',
            'nazwisko': 'Doe',
            'plec': 2,
            'stanowisko': 1,
            'wlasciciel': self.user.id
        }
        response = self.client.post('/osoba_list/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Osoba.objects.count(), 1)
        self.assertEqual(Osoba.objects.get().imie, 'Jane')
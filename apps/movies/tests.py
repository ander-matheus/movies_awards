from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.movies.models import Movie, Producer, Studio


class MovieModelTest(TestCase):
    def setUp(self):
        self.producer = Producer.objects.create(name="Producer Teste")
        self.studio = Studio.objects.create(name="Studio Teste")
        self.movie = Movie.objects.create(
            year=2024, title="Filme de Teste", winner=True
        )
        self.movie.producer.add(self.producer)
        self.movie.studio.add(self.studio)

    def test_movie_create(self):
        self.assertEqual(self.movie.year, 2024)
        self.assertEqual(self.movie.title, "Filme de Teste")
        self.assertTrue(self.movie.winner)
        self.assertIn(self.producer, self.movie.producer.all())
        self.assertIn(self.studio, self.movie.studio.all())

    def test_metodo_str(self):
        self.assertEqual(str(self.movie), "Filme de Teste")


class MovieViewSetTest(APITestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            year=2024, title="Filme para Busca", winner=False
        )

    def movies_list_test(self):
        url = reverse("movie-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Filme para Busca")

    def movies_search_by_title(self):
        url = reverse("movie-list") + "?search=Busca"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            any(item["title"] == "Filme para Busca" for item in response.data)
        )

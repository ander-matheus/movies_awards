from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from .models import Movie, Producer, Studio


class MovieModelTest(TestCase):
    """
    TestCase for the Movie model and its relationships.

    This suite covers:
        - Model field validation and constraints
        - Many-to-many relationships with producers and studios
        - Querying and filtering logic
    """

    def setUp(self):
        """
        Set up test data for Movie, Producer, and Studio models.
        """
        self.producer1 = Producer.objects.create(name="Producer A")
        self.producer2 = Producer.objects.create(name="Producer B")
        self.studio1 = Studio.objects.create(name="Studio X")
        self.studio2 = Studio.objects.create(name="Studio Y")

        self.movie1 = Movie.objects.create(year=2020, title="Movie Alpha", winner=True)
        self.movie1.producer.add(self.producer1, self.producer2)
        self.movie1.studio.add(self.studio1)

        self.movie2 = Movie.objects.create(year=2022, title="Movie Beta", winner=False)
        self.movie2.producer.add(self.producer1)
        self.movie2.studio.add(self.studio2)

    def test_movie_creation_validation(self):
        """
        Test model validation and field constraints.
        """
        with self.assertRaises(Exception):
            Movie.objects.create(year="invalid", title="Test")

        with self.assertRaises(Exception):
            Movie.objects.create(year=2024, title="A" * 256)

    def test_movie_unique_constraint(self):
        """
        Test that movies with the same title but different years can coexist.
        """
        Movie.objects.create(year=2023, title="Movie Alpha")
        self.assertEqual(Movie.objects.filter(title="Movie Alpha").count(), 2)

    def test_movie_query_methods(self):
        """
        Test complex queries involving model relationships.
        """
        winners = Producer.objects.filter(movies__winner=True)
        self.assertEqual(winners.count(), 2)

        studio_x_movies = Movie.objects.filter(studio__name="Studio X")
        self.assertEqual(studio_x_movies.count(), 1)

    def test_movie_year_filtering(self):
        """
        Test filtering movies by year range.
        """
        recent_movies = Movie.objects.filter(year__gte=2022)
        self.assertEqual(recent_movies.count(), 1)


class MovieViewSetTest(APITestCase):
    """
    APITestCase for the MovieViewSet endpoints.

    This suite covers:
        - List and detail endpoints
        - Pagination and search scenarios
        - Award interval endpoint
        - Filtering and invalid HTTP methods
    """

    def setUp(self):
        """
        Set up test data for Movie, Producer, and Studio models.
        """
        self.client = APIClient()
        self.producer = Producer.objects.create(name="Test Producer")
        self.studio = Studio.objects.create(name="Test Studio")

        self.producer2 = Producer.objects.create(name="Test Producer 2")
        self.studio2 = Studio.objects.create(name="Test Studio 2")

        for i in range(15):
            movie = Movie.objects.create(year=2000 + i, title=f"Movie {i}")
            if i % 2 == 0:
                movie.producer.add(self.producer)
                movie.studio.add(self.studio)
            else:
                movie.producer.add(self.producer2)
                movie.studio.add(self.studio2)

        Movie.objects.filter(pk__in=[1, 3, 7, 10]).update(winner=True)

    def test_list_pagination(self):
        """
        Test default DRF pagination on the movie list endpoint.
        """
        url = reverse("movie-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("results" in response.data)
        self.assertEqual(len(response.data["results"]), 10)  # Default page size

    def test_awards_interval_endpoint(self):
        """
        Test the awards interval endpoint with complex data.
        """
        url = reverse("movie-list") + "awards-interval-by-producer/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertEqual(data["min"][0]["interval"], 2)
        self.assertEqual(data["max"][0]["interval"], 4)
        self.assertTrue(
            all(
                field in data["min"][0]
                for field in ["producer", "interval", "previousWin", "followingWin"]
            )
        )

    def test_detail_view_relations(self):
        """
        Test detailed movie view with related studios and producers.
        """
        movie = Movie.objects.first()
        url = reverse("movie-detail", args=[movie.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("studios" in response.data)
        self.assertTrue("producers" in response.data)

    def test_invalid_http_methods(self):
        """
        Test that invalid HTTP methods are not allowed on detail endpoint.
        """
        movie = Movie.objects.first()
        url = reverse("movie-detail", args=[movie.id])
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 405)
        response = self.client.put(url, {})
        self.assertEqual(response.status_code, 405)

    def movies_search_by_title(self):
        url = reverse("movie-list") + "?search=Alpha"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(item["title"] == "Alpha" for item in response.data))

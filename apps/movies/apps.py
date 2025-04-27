import csv
import logging
import os
import re

from django.apps import AppConfig
from django.conf import settings
from django.db import ProgrammingError

logger = logging.getLogger(__name__)


class MoviesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.movies"

    def ready(self):
        self.load_csv_data()

    def load_csv_data(self):
        from .models import Movie

        csv_path = os.path.join(settings.BASE_DIR, "movielist.csv")

        try:
            if not Movie.objects.exists() and os.path.exists(csv_path):
                with open(csv_path, newline="", encoding="utf-8") as csv_file:
                    reader = csv.DictReader(csv_file, delimiter=";")
                    for row in reader:
                        studios = self.get_or_create_studios(row["studios"])
                        producers = self.get_or_create_producers(row["producers"])
                        movie = Movie.objects.create(
                            year=int(row["year"]),
                            title=row["title"],
                            winner=row["winner"] == "yes",
                        )
                        movie.studio.set(studios)
                        movie.producer.set(producers)
                count = Movie.objects.count()
                logger.info(f"Total de {count} filmes carregados.")

        except ProgrammingError as e:
            logger.error(f"Erro ao carregar o CSV para base: {e}")

    def split_names(self, names: str) -> list:
        names_list = re.split(r",\s*|\s+and\s+", names)
        names_list = [name.strip().replace("and", "") for name in names_list]
        return names_list

    def get_or_create_studios(self, studios_names) -> list:
        from .models import Studio

        names_list = self.split_names(studios_names)
        studios = []
        for studio_name in names_list:
            studio, created = Studio.objects.get_or_create(name=studio_name)
            studios.append(studio)
        return studios

    def get_or_create_producers(self, producers_names) -> list:
        from .models import Producer

        names_list = self.split_names(producers_names)
        producers = []
        for producer_name in names_list:
            producer, created = Producer.objects.get_or_create(name=producer_name)
            producers.append(producer)
        return producers

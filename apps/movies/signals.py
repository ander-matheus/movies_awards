import csv
import logging
import os
import re
from typing import List, Type

from django.apps import AppConfig
from django.conf import settings
from django.db import ProgrammingError

from apps.movies.models import Movie, Producer, Studio

logger = logging.getLogger(__name__)


def load_csv_data(sender: Type[AppConfig], **kwargs):

    csv_path = os.path.join(settings.BASE_DIR, "movieslist.csv")

    try:
        if not Movie.objects.exists() and os.path.exists(csv_path):
            with open(csv_path, newline="", encoding="utf-8") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    studios = get_or_create_studios(row["studio"])
                    producers = get_or_create_producers(row["producers"])
                    movie = Movie.objects.create(
                        year=int(row["year"]),
                        name=row["name"],
                        winner=row["winner"] == "yes",
                    )
                    movie.studio.set(studios)
                    movie.producer.set(producers)
            count = Movie.objects.count()
            logger.info(f"Total de {count} filmes carregados!")
    except ProgrammingError as e:
        logger.error(f"Erro ao carregar o CSV para base: {e}")


def split_names(names: str) -> list:
    names_list = re.split(r",\s*|\s+and\s+", names)
    names_list = [name.strip() for name in names_list]
    return names_list


def get_or_create_studios(studios_names) -> List[Studio]:
    names_list = split_names(studios_names)
    studios = []
    for studio_name in names_list:
        studio, created = Studio.objects.get_or_create(name=studio_name)
        studios.append(studio)
    return studios


def get_or_create_producers(producers_names) -> List[Producer]:
    names_list = split_names(producers_names)
    producers = []
    for producer_name in names_list:
        producer, created = Producer.objects.get_or_create(name=producer_name)
        producers.append(producer)
    return producers

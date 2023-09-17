import os
from collections import OrderedDict
from csv import DictReader
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre

ALREDY_LOADED_ERROR_MESSAGE = """
Для загрузки данных из CSV-файла
сначала удалите файл db.sqlite3, чтобы уничтожить ранее созданную БД.
После этого запустите команду `python manage.py migrate`
для создания пустой БД.
"""
IMPORT_MESSAGE = """
Импорт данных в таблицу {}
--------------------------------------------------------------------------"""
PATH_TO_FILES = settings.BASE_DIR / 'static/data/'

# Переменная, связывающая имена csv-файлов с таблицами.
FILES_TO_MODELS = OrderedDict(
    users=get_user_model(),
    category=Category,
    genre=Genre,
    titles=Title,
    genre_title=TitleGenre,
    review=Review,
    comments=Comment
)


class Command(BaseCommand):
    """Создает команду терминала для импорта данных из csv.

    Для запуска импорта:
    python manage.py load_csv_data
    """

    help = 'Загрузка данных из .csv файлов.'

    def handle(self, *args, **options):
        """Переопределение метода класса, выполняющего основные действия."""

        # Проверка того, не существуют ли уже заполненные таблицы
        for model in FILES_TO_MODELS.values():
            if model.objects.exists():
                return ALREDY_LOADED_ERROR_MESSAGE

        # Цикл по csv-файлам, в порядке определеном упорядоченным словарем
        # FILES_TO_MODELS
        for file in FILES_TO_MODELS:
            filename = os.path.join(PATH_TO_FILES, file + '.csv')
            model = FILES_TO_MODELS[file]

            # Определяем, есть ли в модели связанные поля.
            fk_fields = [
                field for field in model._meta.fields if (
                    field.get_internal_type() == 'ForeignKey'
                )
            ]

            # Начинаем чтение файла
            with open(filename, encoding='utf-8') as csvfile:
                print(IMPORT_MESSAGE.format(model.__name__))
                reader = DictReader(csvfile)

                for row in reader:
                    if fk_fields:
                        for field in fk_fields:
                            # Если поле связанной модели есть среди столбцов
                            # csv-файла, то извлекаем объект связанной модели
                            # по id из файла
                            if field.name in reader.fieldnames:
                                row[field.name] = get_object_or_404(
                                    field.related_model,
                                    pk=row[field.name]
                                )
                    model.objects.create(**row)

            print(f'Число импортированных записей: {model.objects.count()}')

        print('Импорт данных завершен.')

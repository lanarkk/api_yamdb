import os
from collections import OrderedDict
from csv import DictReader
from django.conf import settings
from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
# from users.models import User

ALREDY_LOADED_ERROR_MESSAGE = """
Для загрузки данных из CSV-файла
сначала удалите файл db.sqlite3, чтобы уничтожить ранее созданную БД.
После этого запустите команду `python manage.py migrate`
для создания пустой БД.
"""
IMOPRT_MESSAGE = """
Импорт данных в таблицу {}
--------------------------------------------------------------------------"""
PATH_TO_FILES = settings.BASE_DIR / 'static/data/'
FILES_VS_MODELS = OrderedDict(
    category=Category,
    genre=Genre,
    titles=Title,
    genre_title=TitleGenre,
    review=Review,
    comments=Comment
)


def get_csv_field_names(row_names, field_names):
    csv_fields = {}
    for field in field_names:
        matches = list(filter(lambda s: field in s, row_names))
        if len(matches) == 1:
            csv_fields[field] = matches[0]
        else:
            raise KeyError(
                f'В CSV-файле отсутствуе столбец для поля {field}.'
            )
    return csv_fields


class Command(BaseCommand):
    """Создает команду для командной строки для импорта данных из csv."""

    help = 'Загрузка данных из .csv файлов.'

    def handle(self, *args, **options):
        for model in FILES_VS_MODELS.values():
            if model.objects.exists():
                return ALREDY_LOADED_ERROR_MESSAGE

    for file in FILES_VS_MODELS:
        filename = os.path.join(PATH_TO_FILES, file + '.csv')
        model = FILES_VS_MODELS[file]
        fk_fields = [
            field for field in model._meta.fields if (
                field.get_internal_type() == 'ForeignKey'
            )
        ]

        with open(filename, encoding='utf-8') as csvfile:
            print(IMOPRT_MESSAGE.format(model.__name__))
            reader = DictReader(csvfile)
            fields_are_consistent = set(reader.fieldnames).issubset(
                set([field.name for field in model._meta.fields]))

            for row in reader:
                if fk_fields and fields_are_consistent:
                    for field in fk_fields:
                        row[field.name] = get_object_or_404(
                            field.related_model,
                            pk=row[field.name]
                        )
                model.objects.create(**row)

        print(f'Число импортированных записей: {model.objects.count()}')

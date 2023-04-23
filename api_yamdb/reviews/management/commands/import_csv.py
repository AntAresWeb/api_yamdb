import csv

from django.contrib.staticfiles import finders
from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle,
                            Review, Title, User)


class Command(BaseCommand):
    help = 'Заполнение БД данными из csv-файлов'

    def handle(self, *args, **kwargs):
        self.stdout.write('Импорт категорий')
        Category.objects.all().delete()
        with open(finders.find('data/category.csv')) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                category = Category(id=row['id'],
                                    name=row['name'],
                                    slug=row['slug'])
                category.save()
                line_count += 1
        self.stdout.write('Добавлено строк %s' % line_count)

        self.stdout.write('Импорт жанров')
        Genre.objects.all().delete()
        with open(finders.find('data/genre.csv')) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                genre = Genre(id=row['id'],
                              name=row['name'],
                              slug=row['slug'])
                genre.save()
                line_count += 1

        self.stdout.write("Добавлено строк %s" % line_count)

        self.stdout.write('Импорт произведений')
        Title.objects.all().delete()
        with open(finders.find('data/titles.csv')) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                category = Category.objects.get(pk=row['category'])
                title = Title(id=row['id'],
                              name=row['name'],
                              year=row['year'],
                              category=category)
                title.save()
                line_count += 1
        self.stdout.write("Добавлено строк %s" % line_count)

        self.stdout.write('Импорт пользователей')
        User.objects.all().delete()
        with open(finders.find('data/users.csv')) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                user = User(id=row['id'],
                            username=row['username'],
                            email=row['email'],
                            role=row['role'],
                            bio=row['bio'],
                            first_name=row['first_name'],
                            last_name=row['last_name'])
                user.save()
                line_count += 1

        self.stdout.write("Добавлено строк %s" % line_count)

        self.stdout.write('Импорт жанров произведений')
        GenreTitle.objects.all().delete()
        with open(finders.find('data/genre_title.csv')) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                title = Title.objects.get(pk=row['title_id'])
                genre = Genre.objects.get(pk=row['genre_id'])
                genre_title = GenreTitle(id=row['id'],
                                         title=title,
                                         genre=genre)
                genre_title.save()
                line_count += 1

        self.stdout.write("Добавлено строк %s" % line_count)

        self.stdout.write('Импорт обзоров')
        Review.objects.all().delete()
        with open(finders.find('data/review.csv')) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                user = User.objects.get(pk=row['author'])
                title = Title.objects.get(pk=row['title_id'])
                review = Review(id=row['id'],
                                title=title,
                                text=row['text'],
                                author=user,
                                score=row['score'],
                                pub_date=row['pub_date'])
                review.save()
                line_count += 1

        self.stdout.write("Добавлено строк %s" % line_count)

        self.stdout.write('Импорт комментариев')
        Comment.objects.all().delete()
        with open(finders.find('data/comments.csv')) as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                review = Review.objects.get(pk=row['review_id'])
                user = User.objects.get(pk=row['author'])
                comment = Comment(id=row['id'],
                                  review=review,
                                  text=row['text'],
                                  author=user,
                                  pub_date=row['pub_date'])
                comment.save()
                line_count += 1

        self.stdout.write("Добавлено строк %s" % line_count)

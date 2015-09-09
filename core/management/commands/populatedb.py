import random
import glob
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from django.utils import timezone
from faker import Factory as FakerFactory

from core.models import News, Product, AgripoUser, ProductCategory

faker = FakerFactory.create('fr_FR')
faker.seed(1000)

def insert_random_category(silent=False):
    the_category, created = ProductCategory.objects.get_or_create(name=faker.sentence(nb_words=4), )
    if not created and not silent:
        raise IntegrityError()

    return the_category


def insert_random_product(category=None, stock=0, random_image=True, price=0, silent=False):
    if not category:
        category = insert_random_category(silent=silent)

    the_product, created = Product.objects.get_or_create(name=faker.sentence(nb_words=2),
                                                         defaults={'category': category})
    if not created and not silent:
        raise IntegrityError()

    if price == 0:
        price = random.randint(100, 10000)

    the_product.category = category
    the_product.price = price
    the_product.stock = stock

    if random_image:
        # Getting random image
        images = glob.glob("{}/products/*.jpg".format(settings.MEDIA_ROOT))
        if len(images) > 0:
            the_product.image = images[random.randint(0, len(images) - 1)].replace(settings.MEDIA_ROOT, "")
        else:
            print("Warning : There was no image in the products' folder, so the default one was used")

    the_product.save()
    return the_product


def insert_random_categories_and_products(categories_count=5, products_count=5, stock=0, silent=False):
    for i in range(0, categories_count):
        cat = insert_random_category(silent=silent)

        for j in range(0, products_count):
           insert_random_product(cat, stock=stock, silent=silent)


class Command(BaseCommand):
    help = 'Creates some random entries in the database for demo purpose'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--news-count',
            type=int,
            default=10,
            dest="news_count",
            help='Number of news to insert (defaults to 10)')

        parser.add_argument(
            '--categories-count',
            type=int,
            default=4,
            dest="categories_count",
            help="Number of products' categories to insert (defaults to 4)")

        parser.add_argument(
            '--products-count',
            type=int,
            default=5,
            dest="products_count",
            help='Number of products to insert in each category (defaults to 5)')

    def handle(self, *args, **options):
        manager, created = AgripoUser.objects.get_or_create(username="Manager", password="random_password")
        if created:
            manager.add_to_managers()

        for i in range(0, int(options['news_count'])):
            default_data = dict(
                content="\n".join(faker.paragraphs()),
                writer=manager,
                creation_date=timezone.now(),
                publication_date=timezone.now() - timezone.timedelta(i),
            )
            News.objects.get_or_create(title=faker.sentence(), defaults=default_data)

        categories_count = int(options['categories_count'])
        products_count = int(options['products_count'])
        insert_random_categories_and_products(
            categories_count=categories_count, products_count=products_count, stock=10,
            silent=True)

        self.stdout.write('Successfully created {} news and {} products in {} categories'.format(
            options['news_count'], products_count * categories_count, categories_count))

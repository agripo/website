import random
import glob
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Factory as FakerFactory

from core.models import News, Product, AgripoUser, ProductCategory

faker = FakerFactory.create('fr_FR')
faker.seed(1000)

def insert_random_category():
    the_category = ProductCategory(
        name=faker.sentence(nb_words=4),)
    the_category.save()
    return the_category


def insert_random_product(category=None, stock=0, random_image=True):
    if not category:
        category = insert_random_category()

    args = dict(name=faker.sentence(nb_words=2), price=random.randint(100, 10000),
                category=category, stock=stock)

    if random_image:
        # Getting random image
        images = glob.glob("{}/products/*.jpg".format(settings.MEDIA_ROOT))
        if len(images) > 0:
            args['image'] = images[random.randint(0, len(images) - 1)].replace(settings.MEDIA_ROOT, "")
        else:
            print("Warning : There was no image in the products' folder, so the default one was used")

    the_product = Product(**args)
    the_product.save()
    return the_product


def insert_random_categories_and_products(categories_count=5, products_count=5):
    for i in range(0, categories_count):
        cat = insert_random_category()
        for j in range(0, products_count):
            insert_random_product(cat)


class Command(BaseCommand):
    help = 'Creates some random entries in the database for demo purpose'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--news-count',
            type=int,
            default=10,
            dest="news_count",
            help='Number of news to insert (defaults to 10)')

        parser.add_argument('--categories-count',
            type=int,
            default=4,
            dest="categories_count",
            help="Number of products' categories to insert (defaults to 4)")

        parser.add_argument('--products-count',
            type=int,
            default=5,
            dest="products_count",
            help='Number of products to insert in each category (defaults to 5)')

    def handle(self, *args, **options):
        manager, created = AgripoUser.objects.get_or_create(username="Manager", password="random_password")
        if created:
            manager.add_to_managers()

        faker = FakerFactory.create('fr_FR')

        for i in range(0, int(options['news_count'])):
            the_news = News(
                title=faker.sentence(),
                content="\n".join(faker.paragraphs()),
                writer=manager,
                creation_date=timezone.now()
            )
            the_news.publication_date = timezone.now() - timezone.timedelta(i)
            the_news.save()

        categories_count = int(options['categories_count'])
        products_count = int(options['products_count'])
        insert_random_categories_and_products(
            categories_count=categories_count, products_count=products_count)

        self.stdout.write('Successfully created {} news and {} products in {} categories'.format(
            options['news_count'], products_count * categories_count, categories_count))

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Factory as FakerFactory

from core.models import News, AgripoUser

class Command(BaseCommand):
    help = 'Creates some random entries in the database for demo purpose'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--news-count',
            type=int,
            default=10,
            dest="news_count",
            help='Number of news to insert (defaults to 10)')

    def handle(self, *args, **options):
        manager, created = AgripoUser.objects.get_or_create(username="Manager", password="random_password")
        manager.save()
        manager.add_to_managers()

        faker = FakerFactory.create('fr_FR')

        for i in range(0, options['news_count']):
            the_news = News(
                title=faker.sentence(),
                content="\n".join(faker.paragraphs()),
                writer=manager
            )
            the_news.publication_date = timezone.now() - timezone.timedelta(i)
            the_news.save()

        self.stdout.write('Successfully created {} news'.format(options['news_count']))

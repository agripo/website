from django.core.management.base import BaseCommand

from core.backup import backup, get_backup_file


class Command(BaseCommand):
    help = 'Creates a backup.'

    def handle(self, *args, **options):
        backup()
        self.stdout.write('Backup file "{}" created successfully'.format(get_backup_file()))

import os
from django.conf import settings
from django.core.management.base import BaseCommand
from pathlib import Path
from PIL import Image


class Command(BaseCommand):
    help = 'Creates some random entries in the database for demo purpose'

    image_types = [".jpg", ".jpeg", ".png", ".gif"]
    driver_by_ext = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG", ".gif": "GIF"}
    size = 1280, 1024
    resize_base_folder = settings.MEDIA_ROOT

    def handle(self, *args, **options):
        folder = Path(self.resize_base_folder)
        for p in folder.glob('./**/*'):
            if p.is_file():
                if p.suffix.lower() in self.image_types:
                    im = Image.open(str(p.resolve()))
                    width, height = im.size
                    if width > self.size[0] or height > self.size[1]:
                        file = p.resolve()
                        temp_file = self.resize_base_folder + 'tmp_' + p.stem + p.suffix.lower()
                        os.rename(str(file), temp_file)
                        im = Image.open(temp_file)
                        try:
                            im.thumbnail(self.size)
                            im.save(str(file), self.driver_by_ext[p.suffix.lower()])
                        except Exception as e:
                            # There was an error, we put the original file back
                            self.stdout.write('Error resizing image' + temp_file + str(e))
                            os.rename(temp_file, str(file))
                        else:
                            os.unlink(temp_file)

        self.stdout.write('Images resizing finished')
